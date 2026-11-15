"""Teste adicional: o arquivo é lido por completo."""

from helpers import run_cli


def test_reads_all_rows_beyond_200(tmp_path):
    """250 reservas confirmadas de 100.00 BRL / 1 noite: nada pode ser descartado."""
    rows = [{"reservation_id": f"R-{i}"} for i in range(250)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 250
    assert report["summary"]["total_room_nights"] == 250
    assert report["summary"]["total_amount_brl"] == "25000.00"
