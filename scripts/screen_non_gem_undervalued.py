#!/usr/bin/env python3
"""
筛选A股非创业板低估值股票
"""
import akshare as ak
import json
from datetime import datetime

def get_non_gem_stocks():
    """获取非创业板股票列表（主板 + 科创板 + 北交所）"""
    try:
        # 获取全部A股实时行情
        df = ak.stock_zh_a_spot_em()
        if df is None or df.empty:
            return []

        # 筛选非创业板：排除代码以3开头的深交所股票
        # 主板：6xxxxx（沪）, 0xxxxx（深）
        # 科创板：688xxx（沪）
        # 北交所：4xxxxx, 8xxxxx
        # 创业板：300xxx（深）
        df_filtered = df[~df['代码'].str.startswith('30')]  # 排除创业板

        # 排除ST股票
        df_filtered = df_filtered[~df_filtered['名称'].str.contains('ST|\*ST', regex=True)]

        return df_filtered
    except Exception as e:
        print(f"获取股票列表失败: {e}", file=__import__('sys').stderr)
        return []

def screen_undervalued(stocks_df, max_pe=25, max_pb=3, min_roe=10, min_market_cap=50):
    """
    筛选低估值股票

    参数:
        stocks_df: 股票数据DataFrame
        max_pe: 最大PE
        max_pb: 最大PB
        min_roe: 最小ROE
        min_market_cap: 最小市值（亿元）
    """
    results = []

    for _, row in stocks_df.iterrows():
        try:
            symbol = row['代码']
            name = row['名称']
            pe = row.get('市盈率-动态', 999)
            pb = row.get('市净率', 999)
            market_cap = row.get('总市值', 0) / 100000000  # 转换为亿元

            # 基础筛选条件
            if pe <= 0 or pe > max_pe:
                continue
            if pb <= 0 or pb > max_pb:
                continue
            if market_cap < min_market_cap:
                continue

            # 获取财务指标（ROE等）
            try:
                df_fin = ak.stock_financial_abstract_ths(symbol=symbol, indicator="按报告期")
                if df_fin is not None and not df_fin.empty:
                    latest = df_fin.iloc[-1]
                    roe = latest.get("净资产收益率", 0)
                    revenue_growth = latest.get("营业总收入同比增长率", 0)
                    profit_growth = latest.get("净利润同比增长率", 0)

                    # 财务指标筛选
                    if roe < min_roe:
                        continue
                    if revenue_growth is None or revenue_growth < 0:
                        continue
                    if profit_growth is None or profit_growth < 0:
                        continue

                    results.append({
                        '代码': symbol,
                        '名称': name,
                        '最新价': row.get('最新价'),
                        '涨跌幅': row.get('涨跌幅'),
                        '市值(亿)': round(market_cap, 2),
                        'PE_TTM': round(pe, 2),
                        'PB': round(pb, 2),
                        'ROE(%)': round(roe, 2),
                        '营收增长(%)': round(revenue_growth, 2) if revenue_growth else None,
                        '利润增长(%)': round(profit_growth, 2) if profit_growth else None,
                        '换手率(%)': row.get('换手率'),
                    })
            except:
                # 获取财务指标失败，跳过
                continue

        except Exception as e:
            continue

    return results

def main():
    print("正在获取A股数据...", file=__import__('sys').stderr)

    # 获取非创业板股票
    stocks_df = get_non_gem_stocks()
    print(f"获取到 {len(stocks_df)} 只非创业板股票", file=__import__('sys').stderr)

    # 筛选低估值股票
    # 筛选条件：PE<25, PB<3, ROE>10%, 市值>50亿
    results = screen_undervalued(stocks_df, max_pe=25, max_pb=3, min_roe=10, min_market_cap=50)

    # 按ROE降序排列
    results.sort(key=lambda x: x['ROE(%)'], reverse=True)

    # 取前20只
    top_results = results[:20]

    output = {
        '筛选时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '筛选条件': {
            '市场': '非创业板（主板+科创板+北交所）',
            '最大PE': 25,
            '最大PB': 3,
            '最小ROE': '10%',
            '最小市值': '50亿',
        },
        '筛选结果数量': len(top_results),
        '股票列表': top_results
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
