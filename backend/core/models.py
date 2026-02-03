from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class DegreeLevel(models.TextChoices):
    BSC = "BSC", "BSc"
    MSC = "MSC", "MSc"
    PHD = "PHD", "PhD"


class ProposalStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    IN_REVIEW = "IN_REVIEW", "In Review"
    REVISION_REQUIRED = "REVISION_REQUIRED", "Revision Required"
    APPROVED = "APPROVED", "Approved"


class AcademicProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=8, choices=DegreeLevel.choices)
    research_interests = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.user} ({self.degree_level})"


class Proposal(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="proposals")
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=ProposalStatus.choices, default=ProposalStatus.DRAFT)
    degree_level = models.CharField(max_length=8, choices=DegreeLevel.choices)
    problem_statement = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class ProposalSection(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    completeness_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completeness_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=70)
    is_locked = models.BooleanField(default=True)

    class Meta:
        unique_together = ("proposal", "name")
        ordering = ["order"]


class Question(models.Model):
    section = models.ForeignKey(ProposalSection, on_delete=models.CASCADE, related_name="questions")
    prompt = models.TextField()
    help_text = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_questions")
    is_required = models.BooleanField(default=True)
    critical_for_alignment = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]


class StudentResponse(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("proposal", "question")


class ResearchObjective(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="objectives")
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class ResearchQuestion(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="research_questions")
    text = models.TextField()
    objective = models.ForeignKey(ResearchObjective, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class Hypothesis(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="hypotheses")
    text = models.TextField()
    research_question = models.ForeignKey(ResearchQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class MethodologyComponent(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="methodology_components")
    component_type = models.CharField(max_length=120)
    description = models.TextField()
    justification = models.TextField()
    degree_level = models.CharField(max_length=8, choices=DegreeLevel.choices)


class GeneratedSection(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="generated_sections")
    section_name = models.CharField(max_length=120)
    content = models.TextField()
    ai_generated = models.BooleanField(default=True)
    ai_contribution_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    source_response_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        if self.ai_generated and not self.source_response_ids:
            raise ValidationError("AI-generated sections must reference source response IDs.")
        if self.ai_contribution_percentage < 0 or self.ai_contribution_percentage > 100:
            raise ValidationError("AI contribution percentage must be between 0 and 100.")


class AITransparencyLog(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="ai_logs")
    generated_section = models.ForeignKey(GeneratedSection, on_delete=models.CASCADE, related_name="ai_logs")
    model_name = models.CharField(max_length=120)
    prompt = models.TextField()
    input_response_ids = models.JSONField(default=list)
    output_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class QualityScore(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="quality_scores")
    category = models.CharField(max_length=120)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    explanation = models.TextField()
    algorithm_version = models.CharField(max_length=50)
    computed_at = models.DateTimeField(auto_now_add=True)


class DefenseReadinessIndex(models.Model):
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name="defense_readiness")
    score = models.DecimalField(max_digits=5, decimal_places=2)
    rationale = models.TextField()
    computed_at = models.DateTimeField(auto_now_add=True)


class SupervisorReview(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supervisor_reviews")
    status = models.CharField(max_length=32, choices=ProposalStatus.choices)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ProposalVersion(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    snapshot = models.JSONField(default=dict)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("proposal", "version_number")


class ExportRecord(models.Model):
    EXPORT_TYPES = (
        ("DOCX", "DOCX"),
        ("PDF", "PDF"),
    )

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="exports")
    export_type = models.CharField(max_length=10, choices=EXPORT_TYPES)
    file_path = models.CharField(max_length=255)
    ai_contribution_statement = models.TextField()
    quality_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class AlignmentCheck(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="alignment_checks")
    check_type = models.CharField(max_length=120)
    status = models.CharField(max_length=20)
    details = models.TextField()
    blocking_issue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
