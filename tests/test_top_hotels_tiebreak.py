"""Teste adicional: desempate do ranking de hotéis."""

from helpers import run_cli


def test_top_hotels_tie_broken_by_hotel_id_ascending(tmp_path):
    """Mesmo total_brl: hotel_id ascendente, mantendo total decrescente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "amount": "500.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "amount": "900.00"},
            {"reservation_id": "R-4", "hotel_id": "H04", "amount": "100.00"},
        ],
        top=3,
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H02", "H01", "H03"]
