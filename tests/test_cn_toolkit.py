import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CN_SCRIPT_DIR = ROOT / "China-market" / "findata-toolkit-cn" / "scripts"


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class CNToolkitSmokeTests(unittest.TestCase):
    @unittest.skipUnless(sys.version_info >= (3, 10), "Requires Python 3.10+")
    def test_cli_help_for_cn_scripts(self):
        scripts = ["stock_data.py", "macro_data.py"]
        for script in scripts:
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, str(CN_SCRIPT_DIR / script), "--help"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(
                    0,
                    result.returncode,
                    msg=f"--help failed for {script}: {result.stderr}",
                )

    def test_cn_screen_stocks_output_schema(self):
        if sys.version_info < (3, 10):
            self.skipTest("Requires Python 3.10+")
        module = _load_module("cn_stock_data", CN_SCRIPT_DIR / "stock_data.py")

        def fake_metrics(symbol, quote_lookup=None):
            if symbol == "600001":
                return {
                    "symbol": "600001",
                    "valuation": {"pe_ttm": 15.0, "pb": 2.0},
                    "profitability": {"roe": 12.0},
                    "leverage": {"debt_to_asset_ratio": 40.0},
                    "data_quality_flags": ["financial_abstract_unavailable: test"],
                }
            return {
                "symbol": "000002",
                "valuation": {"pe_ttm": 45.0, "pb": 6.0},
                "profitability": {"roe": 6.0},
                "leverage": {"debt_to_asset_ratio": 75.0},
            }

        with patch.object(module, "_build_quote_lookup", return_value={"600001": {}, "000002": {}}), patch.object(
            module, "fetch_financial_metrics", side_effect=fake_metrics
        ):
            result = module.screen_stocks(["600001", "000002"])

        expected_top_keys = {
            "filters_applied",
            "data_quality",
            "total_screened",
            "passed",
            "failed",
            "results",
            "rejected",
        }
        self.assertTrue(expected_top_keys.issubset(set(result.keys())))
        self.assertIn("issues", result["data_quality"])
        self.assertEqual(2, result["total_screened"])


if __name__ == "__main__":
    unittest.main()
