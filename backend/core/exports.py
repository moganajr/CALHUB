from __future__ import annotations

from pathlib import Path

from core import models


def export_proposal(proposal: models.Proposal, export_type: str, output_dir: Path) -> models.ExportRecord:
    if export_type not in {"DOCX", "PDF"}:
        raise ValueError("Unsupported export type.")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"proposal_{proposal.id}.{export_type.lower()}"
    output_path = output_dir / filename
    content = _build_export_content(proposal)
    if export_type == "DOCX":
        _write_docx(output_path, content)
    else:
        _write_pdf(output_path, content)
    return models.ExportRecord.objects.create(
        proposal=proposal,
        export_type=export_type,
        file_path=str(output_path),
        ai_contribution_statement=_ai_statement(proposal),
        quality_summary=_quality_summary(proposal),
    )


def _build_export_content(proposal: models.Proposal) -> list[str]:
    content = [
        proposal.title,
        proposal.problem_statement or "",
    ]
    for section in proposal.generated_sections.all():
        content.append(section.section_name)
        content.append(section.content)
    return content


def _write_docx(path: Path, content: list[str]) -> None:
    from docx import Document

    document = Document()
    for line in content:
        document.add_paragraph(line)
    document.save(path)


def _write_pdf(path: Path, content: list[str]) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    pdf = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 72
    for line in content:
        pdf.drawString(72, y, line)
        y -= 14
        if y < 72:
            pdf.showPage()
            y = height - 72
    pdf.save()


def _ai_statement(proposal: models.Proposal) -> str:
    max_contribution = proposal.generated_sections.order_by("-ai_contribution_percentage").first()
    if not max_contribution:
        return "No AI-generated content included."
    return "AI-assisted structuring used with full traceability to student responses."


def _quality_summary(proposal: models.Proposal) -> str:
    scores = proposal.quality_scores.all()
    if not scores:
        return "Quality scores pending computation."
    lines = [f"{score.category}: {score.score}%" for score in scores]
    return "\n".join(lines)
