"""Testes adicionais: câmbio exato em Decimal."""

from helpers import run_cli


def test_eur_conversion_is_exact(tmp_path):
    """150.00 EUR * 5.88 = 882.00 BRL."""
    report = run_cli(tmp_path, [{"reservation_id": "R-1", "currency": "EUR", "amount": "150.00"}])
    assert report["summary"]["total_amount_brl"] == "882.00"


def test_sum_is_exact_before_rounding(tmp_path):
    """3 x 0.10 USD * 5.42 = 1.626 -> 1.63 (half-up só no fim); float perderia precisão."""
    rows = [{"reservation_id": f"R-{i}", "currency": "USD", "amount": "0.10"} for i in range(3)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_amount_brl"] == "1.63"
