import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
US_SCRIPT_DIR = ROOT / "US-market" / "findata-toolkit" / "scripts"


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class USToolkitSmokeTests(unittest.TestCase):
    @unittest.skipUnless(sys.version_info >= (3, 10), "Requires Python 3.10+")
    def test_cli_help_for_all_us_scripts(self):
        scripts = [
            "stock_data.py",
            "sec_edgar.py",
            "financial_calc.py",
            "portfolio_analytics.py",
            "factor_screener.py",
            "macro_data.py",
        ]

        for script in scripts:
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, str(US_SCRIPT_DIR / script), "--help"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(
                    0,
                    result.returncode,
                    msg=f"--help failed for {script}: {result.stderr}",
                )

    def test_us_screen_stocks_output_schema(self):
        if sys.version_info < (3, 10):
            self.skipTest("Requires Python 3.10+")
        module = _load_module("us_stock_data", US_SCRIPT_DIR / "stock_data.py")

        mocked_metrics = {
            "AAA": {
                "symbol": "AAA",
                "sector": "Technology",
                "valuation": {"pe_trailing": 12.0},
                "growth": {"revenue_growth_yoy": 0.12, "earnings_growth_yoy": 0.10},
                "leverage": {"debt_to_equity": 50.0},
                "cash_flow": {"free_cash_flow": 1000000},
                "profitability": {"roic": 0.20},
                "analyst_consensus": {"upside_pct": 0.35},
            },
            "BBB": {
                "symbol": "BBB",
                "sector": "Technology",
                "valuation": {"pe_trailing": 24.0},
                "growth": {"revenue_growth_yoy": 0.05, "earnings_growth_yoy": 0.03},
                "leverage": {"debt_to_equity": 150.0},
                "cash_flow": {"free_cash_flow": 500000},
                "profitability": {"roic": 0.10},
                "analyst_consensus": {"upside_pct": 0.15},
            },
        }

        with patch.object(module, "fetch_financial_metrics", side_effect=lambda s: mocked_metrics[s]):
            result = module.screen_stocks(
                ["AAA", "BBB"],
                filters={"min_upside": 0.2},
            )

        expected_top_keys = {
            "filters_applied",
            "methodology",
            "sector_benchmarks",
            "total_screened",
            "passed",
            "failed",
            "results",
            "rejected",
        }
        self.assertTrue(expected_top_keys.issubset(set(result.keys())))
        self.assertEqual(2, result["total_screened"])


if __name__ == "__main__":
    unittest.main()
