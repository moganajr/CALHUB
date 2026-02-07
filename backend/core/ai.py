from __future__ import annotations

from core import models


def generate_structured_section(
    proposal: models.Proposal,
    section_name: str,
    responses: list[models.StudentResponse],
) -> str:
    response_text = "\n".join(f"- {response.response_text.strip()}" for response in responses if response.response_text)
    if not response_text:
        return ""
    return (
        f"{section_name}\n"
        "The following points were structured from student responses without adding new claims:\n"
        f"{response_text}\n"
        "Connections reflect only explicitly stated relationships."
    )
