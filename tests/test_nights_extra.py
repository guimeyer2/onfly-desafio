"""Testes adicionais: noites de quarto."""

from helpers import run_cli


def test_nights_across_year_boundary(tmp_path):
    """31/12 -> 02/01 são 2 noites."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": "R-1", "checkin_date": "2024-12-31", "checkout_date": "2025-01-02"}],
    )
    assert report["summary"]["total_room_nights"] == 2
    assert report["by_month"][0]["month"] == "2024-12"


def test_nights_across_month_boundary_with_multiple_rooms(tmp_path):
    """28/01 -> 02/02 com 2 quartos = 5 noites * 2 = 10."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": "R-1", "checkin_date": "2025-01-28", "checkout_date": "2025-02-02", "rooms": "2"}],
    )
    assert report["summary"]["total_room_nights"] == 10
