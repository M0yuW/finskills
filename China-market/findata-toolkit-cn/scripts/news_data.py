#!/usr/bin/env python3
"""
A-Share Market News & Sentiment Data Fetcher
=============================================
Fetch A-share announcements, stock news flow, market wires, hot-rank
(retail sentiment proxy), margin balances, and share-lifting calendar
using AKShare (no API key required).

Usage:
    python news_data.py 600519 --news            # Per-stock news flow
    python news_data.py 600519 --lifting         # Per-stock lifting queue
    python news_data.py --announcements          # Market announcements (today)
    python news_data.py --announcements --date 20260623 --type 重大事项
    python news_data.py --market-news            # Market-wide wires (CLS电报)
    python news_data.py --hot-rank               # Hot-rank (sentiment proxy)
    python news_data.py --margin                 # Margin detail (latest trading day)

All output is JSON to stdout; errors to stderr. Network/interface
failures degrade gracefully to {"error": ..., "note": ...} so the
calling agent can fall back to web_search.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, error_exit


def _normalize_symbol(symbol: str) -> str:
    """Normalize A-share symbol to 6-digit format."""
    sym = symbol.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    return sym.zfill(6)


def _today_yyyymmdd() -> str:
    return datetime.now().strftime("%Y%m%d")


def _rows(df, limit: int) -> list:
    """Convert a DataFrame to a list of row dicts, capped at `limit`."""
    if df is None or df.empty:
        return []
    return df.head(limit).to_dict(orient="records")


# ---------------------------------------------------------------------------
# Per-stock news flow
# ---------------------------------------------------------------------------

def fetch_stock_news(symbol: str, limit: int = 20) -> dict:
    """Per-stock news flow (东方财富个股新闻)."""
    import akshare as ak
    sym = _normalize_symbol(symbol)
    try:
        df = ak.stock_news_em(symbol=sym)
    except Exception as e:
        return {"symbol": sym, "news": [], "error": str(e),
                "note": "stock_news_em failed; fall back to web_search"}
    items = []
    for r in _rows(df, limit):
        items.append({
            "title": r.get("新闻标题", ""),
            "content": r.get("新闻内容", ""),
            "publish_time": str(r.get("发布时间", "")),
            "source": r.get("文章来源", ""),
            "url": r.get("新闻链接", ""),
            "keyword": r.get("关键词", ""),
        })
    return {"symbol": sym, "as_of": _today_yyyymmdd(),
            "count": len(items), "news": items}


# ---------------------------------------------------------------------------
# Market announcements (公告)
# ---------------------------------------------------------------------------

# AKShare stock_notice_report supported categories.
ANNOUNCEMENT_TYPES = (
    "全部", "重大事项", "财务报告", "融资公告",
    "风险提示", "资产重组", "信息变更", "持股变动",
)


def fetch_announcements(date: str | None = None,
                        notice_type: str = "全部",
                        limit: int = 60) -> dict:
    """Market-wide announcements for a given day (沪深京公告)."""
    import akshare as ak
    d = date or _today_yyyymmdd()
    if notice_type not in ANNOUNCEMENT_TYPES:
        notice_type = "全部"
    try:
        df = ak.stock_notice_report(symbol=notice_type, date=d)
    except Exception as e:
        return {"date": d, "type": notice_type, "announcements": [],
                "error": str(e),
                "note": "stock_notice_report failed; fall back to web_search"}
    items = []
    for r in _rows(df, limit):
        items.append({
            "symbol": str(r.get("代码", "")).strip(),
            "name": r.get("名称", ""),
            "title": r.get("公告标题", ""),
            "type": r.get("公告类型", ""),
            "date": str(r.get("公告日期", "")),
            "url": r.get("网址", ""),
        })
    return {"date": d, "type": notice_type,
            "count": len(items), "announcements": items}


# ---------------------------------------------------------------------------
# Market-wide news wires (财联社电报)
# ---------------------------------------------------------------------------

def fetch_market_news(limit: int = 40) -> dict:
    """Market-wide news wires. Tries 东财全球财经快讯 then CLS (财联社电报).

    东财 (em) is fast and reliable; CLS is richer but can be slow/blocked,
    so it is the fallback rather than the primary.
    """
    import akshare as ak
    errors = []
    for label, fn in (("em", lambda: ak.stock_info_global_em()),
                      ("cls", lambda: ak.stock_info_global_cls(symbol="全部"))):
        try:
            df = fn()
        except Exception as e:
            errors.append(f"{label}: {e}")
            continue
        items = []
        for r in _rows(df, limit):
            items.append({
                "title": r.get("标题", "") or r.get("摘要", ""),
                "content": r.get("内容", "") or r.get("摘要", ""),
                "publish_time": str(r.get("发布时间", "")
                                    or r.get("发布日期", "")),
                "url": r.get("链接", "") or r.get("网址", ""),
            })
        if items:
            return {"as_of": _today_yyyymmdd(), "source": label,
                    "count": len(items), "wires": items}
    return {"wires": [], "error": "; ".join(errors),
            "note": "all market-news interfaces failed; fall back to web_search"}


# ---------------------------------------------------------------------------
# Hot-rank (retail sentiment proxy)
# ---------------------------------------------------------------------------

def fetch_hot_rank(limit: int = 30) -> dict:
    """东方财富人气榜 — retail attention/sentiment proxy.

    The EM hot-rank endpoint frequently drops the first connection, so
    retry a few times with a short backoff before degrading.
    """
    import time
    import akshare as ak
    last_err = None
    df = None
    for attempt in range(3):
        try:
            df = ak.stock_hot_rank_em()
            break
        except Exception as e:
            last_err = str(e)
            time.sleep(1.0 + attempt)
    if df is None:
        return {"hot_rank": [], "error": last_err,
                "note": "stock_hot_rank_em failed after retries; fall back to web_search"}
    items = []
    for r in _rows(df, limit):
        items.append({
            "rank": r.get("当前排名", ""),
            "symbol": str(r.get("代码", "")).strip().replace("SH", "").replace("SZ", ""),
            "name": r.get("股票名称", ""),
            "price": r.get("最新价", ""),
            "change_pct": r.get("涨跌幅", ""),
        })
    return {"as_of": _today_yyyymmdd(), "count": len(items), "hot_rank": items}


# ---------------------------------------------------------------------------
# Share-lifting calendar (限售解禁)
# ---------------------------------------------------------------------------

def fetch_lifting(symbol: str, limit: int = 20) -> dict:
    """Per-stock restricted-share lifting queue (限售解禁批次)."""
    import akshare as ak
    sym = _normalize_symbol(symbol)
    try:
        df = ak.stock_restricted_release_queue_em(symbol=sym)
    except Exception as e:
        return {"symbol": sym, "lifting": [], "error": str(e),
                "note": "stock_restricted_release_queue_em failed; fall back to web_search"}
    items = []
    for r in _rows(df, limit):
        items.append({k: (str(v) if isinstance(v, datetime) else v)
                      for k, v in r.items()})
    return {"symbol": sym, "as_of": _today_yyyymmdd(),
            "count": len(items), "lifting": items}


# ---------------------------------------------------------------------------
# Margin detail (融资融券)
# ---------------------------------------------------------------------------

def fetch_margin(date: str | None = None, limit: int = 50) -> dict:
    """Margin trading detail for the latest available trading day.

    Tries the requested/most-recent date, walking back up to 7 days to
    skip non-trading days.
    """
    import akshare as ak
    base = datetime.strptime(date, "%Y%m%d") if date else datetime.now()
    last_err = None
    for back in range(0, 8):
        d = (base - timedelta(days=back)).strftime("%Y%m%d")
        sse_rows, szse_rows = [], []
        try:
            sse_rows = _rows(ak.stock_margin_detail_sse(date=d), limit)
        except Exception as e:
            last_err = f"sse {d}: {e}"
        try:
            szse_rows = _rows(ak.stock_margin_detail_szse(date=d), limit)
        except Exception as e:
            last_err = f"szse {d}: {e}"
        if sse_rows or szse_rows:
            return {"date": d, "sse_count": len(sse_rows),
                    "szse_count": len(szse_rows),
                    "sse": sse_rows, "szse": szse_rows}
    return {"margin": [], "error": last_err,
            "note": "no margin data in last 8 days; fall back to web_search"}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="A-Share News & Sentiment Data Fetcher (AKShare, no API key)"
    )
    parser.add_argument("symbols", nargs="*", help="A-share stock code(s)")
    parser.add_argument("--news", action="store_true",
                        help="Per-stock news flow")
    parser.add_argument("--lifting", action="store_true",
                        help="Per-stock restricted-share lifting queue")
    parser.add_argument("--announcements", action="store_true",
                        help="Market-wide announcements for a day")
    parser.add_argument("--market-news", action="store_true",
                        help="Market-wide news wires (CLS/东财快讯)")
    parser.add_argument("--hot-rank", action="store_true",
                        help="Hot-rank (retail sentiment proxy)")
    parser.add_argument("--margin", action="store_true",
                        help="Margin trading detail (latest trading day)")
    parser.add_argument("--date", default=None,
                        help="Date YYYYMMDD (announcements/margin)")
    parser.add_argument("--type", default="全部",
                        dest="notice_type",
                        help="Announcement category (默认 全部)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max rows to return")
    args = parser.parse_args()

    def lim(default):
        return args.limit if args.limit else default

    try:
        if args.announcements:
            data = fetch_announcements(date=args.date,
                                       notice_type=args.notice_type,
                                       limit=lim(60))
        elif args.market_news:
            data = fetch_market_news(limit=lim(40))
        elif args.hot_rank:
            data = fetch_hot_rank(limit=lim(30))
        elif args.margin:
            data = fetch_margin(date=args.date, limit=lim(50))
        elif args.news:
            if not args.symbols:
                error_exit("--news requires a stock symbol")
            data = fetch_stock_news(args.symbols[0], limit=lim(20))
        elif args.lifting:
            if not args.symbols:
                error_exit("--lifting requires a stock symbol")
            data = fetch_lifting(args.symbols[0], limit=lim(20))
        else:
            error_exit("Specify one of: --news/--lifting (with symbol), "
                       "--announcements/--market-news/--hot-rank/--margin")
            return

        output_json(data)

    except ImportError:
        error_exit("akshare is required. Install: pip install akshare")
    except Exception as e:
        error_exit(f"Error fetching data: {e}")


if __name__ == "__main__":
    main()
