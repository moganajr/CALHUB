from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from core import models


def compute_alignment_checks(proposal: models.Proposal) -> list[models.AlignmentCheck]:
    checks: list[models.AlignmentCheck] = []
    checks.extend(_check_problem_objectives(proposal))
    checks.extend(_check_objectives_questions(proposal))
    checks.extend(_check_questions_methodology(proposal))
    checks.extend(_check_methodology_analysis(proposal))
    return checks


def compute_quality_scores(proposal: models.Proposal) -> list[models.QualityScore]:
    scores: list[models.QualityScore] = []
    scores.append(_score_problem_clarity(proposal))
    scores.append(_score_objective_alignment(proposal))
    scores.append(_score_method_suitability(proposal))
    scores.append(_score_evidence_adequacy(proposal))
    scores.append(_score_ethical_compliance(proposal))
    return scores


def compute_defense_readiness(proposal: models.Proposal, scores: list[models.QualityScore]) -> dict:
    if not scores:
        average_score = Decimal("0")
    else:
        average_score = sum(score.score for score in scores) / Decimal(len(scores))
    return {
        "proposal": proposal,
        "score": average_score,
        "rationale": "Aggregated from quality metrics with equal weights.",
    }


@transaction.atomic
def refresh_governance_metrics(proposal: models.Proposal) -> None:
    proposal.alignment_checks.all().delete()
    models.AlignmentCheck.objects.bulk_create(compute_alignment_checks(proposal))

    proposal.quality_scores.all().delete()
    scores = compute_quality_scores(proposal)
    models.QualityScore.objects.bulk_create(scores)

    models.DefenseReadinessIndex.objects.filter(proposal=proposal).delete()
    models.DefenseReadinessIndex.objects.create(**compute_defense_readiness(proposal, scores))


def generate_supervisor_prompts(proposal: models.Proposal) -> list[models.SupervisorPrompt]:
    prompts: list[models.SupervisorPrompt] = []
    if not proposal.problem_statement:
        prompts.append(
            models.SupervisorPrompt(
                proposal=proposal,
                prompt_text="Where is the empirical gap articulated in the problem statement?",
                severity="BLOCKING",
            )
        )
    if proposal.methodology_components.filter(is_quantitative=True).exists() and not proposal.variables.exists():
        prompts.append(
            models.SupervisorPrompt(
                proposal=proposal,
                prompt_text="How are the quantitative variables operationalized and measured?",
                severity="BLOCKING",
            )
        )
    if not proposal.methodology_components.exists():
        prompts.append(
            models.SupervisorPrompt(
                proposal=proposal,
                prompt_text="Why is the chosen research design appropriate for the questions posed?",
                severity="WARNING",
            )
        )
    return prompts


def _check_problem_objectives(proposal: models.Proposal) -> list[models.AlignmentCheck]:
    if proposal.problem_statement and proposal.objectives.exists():
        return [
            models.AlignmentCheck(
                proposal=proposal,
                check_type="Problem-Objectives",
                status="PASS",
                details="Problem statement is linked to at least one research objective.",
                blocking_issue=False,
            )
        ]
    return [
        models.AlignmentCheck(
            proposal=proposal,
            check_type="Problem-Objectives",
            status="BLOCK",
            details="Problem statement or objectives are missing.",
            blocking_issue=True,
        )
    ]


def _check_objectives_questions(proposal: models.Proposal) -> list[models.AlignmentCheck]:
    if not proposal.objectives.exists():
        return [
            models.AlignmentCheck(
                proposal=proposal,
                check_type="Objectives-Questions",
                status="BLOCK",
                details="Objectives are missing so alignment to questions cannot be verified.",
                blocking_issue=True,
            )
        ]
    total_questions = proposal.research_questions.count()
    aligned_questions = proposal.research_questions.filter(objective__isnull=False).count()
    if total_questions > 0 and aligned_questions == total_questions:
        return [
            models.AlignmentCheck(
                proposal=proposal,
                check_type="Objectives-Questions",
                status="PASS",
                details="All research questions map to objectives.",
                blocking_issue=False,
            )
        ]
    return [
        models.AlignmentCheck(
            proposal=proposal,
            check_type="Objectives-Questions",
            status="BLOCK",
            details="Some research questions are not mapped to objectives.",
            blocking_issue=True,
        )
    ]


def _check_questions_methodology(proposal: models.Proposal) -> list[models.AlignmentCheck]:
    if proposal.research_questions.exists() and proposal.methodology_components.exists():
        return [
            models.AlignmentCheck(
                proposal=proposal,
                check_type="Questions-Methodology",
                status="PASS",
                details="Methodology components exist for the research questions.",
                blocking_issue=False,
            )
        ]
    return [
        models.AlignmentCheck(
            proposal=proposal,
            check_type="Questions-Methodology",
            status="BLOCK",
            details="Methodology components are missing for the research questions.",
            blocking_issue=True,
        )
    ]


def _check_methodology_analysis(proposal: models.Proposal) -> list[models.AlignmentCheck]:
    if proposal.methodology_components.exists() and proposal.analysis_plans.exists():
        return [
            models.AlignmentCheck(
                proposal=proposal,
                check_type="Methodology-Analysis",
                status="PASS",
                details="Analysis plans are defined for the methodology.",
                blocking_issue=False,
            )
        ]
    return [
        models.AlignmentCheck(
            proposal=proposal,
            check_type="Methodology-Analysis",
            status="BLOCK",
            details="Analysis plans are missing for the methodology.",
            blocking_issue=True,
        )
    ]


def _score_problem_clarity(proposal: models.Proposal) -> models.QualityScore:
    length_score = min(len(proposal.problem_statement or "") / 2, 100)
    score = Decimal(str(length_score))
    return models.QualityScore(
        proposal=proposal,
        category="Problem Clarity Score",
        score=score,
        explanation="Scaled by problem statement length, capped at 100.",
        algorithm_version="1.0",
    )


def _score_objective_alignment(proposal: models.Proposal) -> models.QualityScore:
    total_questions = proposal.research_questions.count()
    aligned_questions = proposal.research_questions.filter(objective__isnull=False).count()
    score = Decimal("0")
    if total_questions:
        score = Decimal(str((aligned_questions / total_questions) * 100))
    return models.QualityScore(
        proposal=proposal,
        category="Objective–Question Alignment Score",
        score=score,
        explanation="Percentage of research questions mapped to objectives.",
        algorithm_version="1.0",
    )


def _score_method_suitability(proposal: models.Proposal) -> models.QualityScore:
    total_methods = proposal.methodology_components.count()
    justified_methods = proposal.methodology_components.exclude(justification="").count()
    score = Decimal("0")
    if total_methods:
        score = Decimal(str((justified_methods / total_methods) * 100))
    return models.QualityScore(
        proposal=proposal,
        category="Method Suitability Score",
        score=score,
        explanation="Percentage of methodology components with explicit justification.",
        algorithm_version="1.0",
    )


def _score_evidence_adequacy(proposal: models.Proposal) -> models.QualityScore:
    total_required_questions = models.Question.objects.filter(section__proposal=proposal, is_required=True).count()
    answered_required = models.StudentResponse.objects.filter(
        proposal=proposal,
        question__is_required=True,
    ).exclude(response_text="").count()
    score = Decimal("0")
    if total_required_questions:
        score = Decimal(str((answered_required / total_required_questions) * 100))
    return models.QualityScore(
        proposal=proposal,
        category="Evidence Adequacy Score",
        score=score,
        explanation="Percentage of required questions answered by the student.",
        algorithm_version="1.0",
    )


def _score_ethical_compliance(proposal: models.Proposal) -> models.QualityScore:
    ethics_questions = models.Question.objects.filter(section__proposal=proposal, prompt__icontains="ethic")
    answered_ethics = models.StudentResponse.objects.filter(
        proposal=proposal,
        question__in=ethics_questions,
    ).exclude(response_text="").count()
    score = Decimal("0")
    if ethics_questions.exists():
        score = Decimal(str((answered_ethics / ethics_questions.count()) * 100))
    return models.QualityScore(
        proposal=proposal,
        category="Ethical Compliance Score",
        score=score,
        explanation="Percentage of ethics-related prompts answered.",
        algorithm_version="1.0",
    )
