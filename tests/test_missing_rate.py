"""Teste adicional: moeda sem taxa é entrada inválida (código 2)."""

import csv
import os
import subprocess
import sys

from helpers import BASE, COLUMNS, PROJECT_ROOT, SRC_DIR


def test_currency_without_rate_exits_with_code_2(tmp_path):
    input_path = tmp_path / "reservas.csv"
    rates_path = tmp_path / "rates.csv"
    with input_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerow({**BASE, "currency": "GBP"})
    rates_path.write_text("currency,rate_to_brl\nBRL,1.000000\n", encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    process = subprocess.run(
        [sys.executable, "-m", "onfly_report", "--input", str(input_path), "--rates", str(rates_path),
         "--output", str(tmp_path / "report.json")],
        cwd=str(PROJECT_ROOT), env=env, capture_output=True, text=True, timeout=60,
    )
    assert process.returncode == 2, process.stderr
    assert "GBP" in process.stderr
