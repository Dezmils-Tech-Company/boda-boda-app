from app.services.report_service import build_simple_pdf


def test_build_simple_pdf_returns_pdf_bytes():
    pdf_bytes = build_simple_pdf(
        title="Welfare Summary",
        content_lines=["Member: Jane", "Amount: 2000", "Status: Approved"],
    )

    assert pdf_bytes.startswith(b"%PDF")
    assert b"Welfare Summary" in pdf_bytes
