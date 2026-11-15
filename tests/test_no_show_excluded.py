"""Teste adicional: NO_SHOW não é faturável."""

from helpers import run_cli


def test_no_show_excluded_from_all_aggregates(tmp_path):
    """NO_SHOW conta no total e por status, mas fica fora de noites, valores, by_month e top_hotels."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "100.00"},
            {
                "reservation_id": "R-2",
                "hotel_id": "H02",
                "status": "NO_SHOW",
                "amount": "999.00",
                "checkin_date": "2025-03-01",
                "checkout_date": "2025-03-02",
            },
        ],
    )
    assert report["summary"]["total_reservations"] == 2
    assert report["summary"]["no_show_reservations"] == 1
    assert report["summary"]["total_room_nights"] == 1
    assert report["summary"]["total_amount_brl"] == "100.00"
    assert [m["month"] for m in report["by_month"]] == ["2025-01"]
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01"]
