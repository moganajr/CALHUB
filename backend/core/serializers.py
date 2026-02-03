from django.db import models as django_models
from rest_framework import serializers

from core import models


class AcademicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcademicProfile
        fields = "__all__"


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        fields = "__all__"


class ProposalSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProposalSection
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"


class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentResponse
        fields = "__all__"

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.question.section.update_completeness()
        instance.question.section.save(update_fields=["completeness_score", "is_locked"])
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.question.section.update_completeness()
        instance.question.section.save(update_fields=["completeness_score", "is_locked"])
        return instance


class ResearchObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResearchObjective
        fields = "__all__"


class ResearchQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResearchQuestion
        fields = "__all__"


class HypothesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hypothesis
        fields = "__all__"


class MethodologyComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MethodologyComponent
        fields = "__all__"


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variable
        fields = "__all__"


class AnalysisPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnalysisPlan
        fields = "__all__"


class GeneratedSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GeneratedSection
        fields = "__all__"

    def validate(self, attrs):
        proposal = attrs.get("proposal")
        source_response_ids = attrs.get("source_response_ids", [])
        if proposal and proposal.sections.filter(
            completeness_score__lt=django_models.F("completeness_threshold")
        ).exists():
            raise serializers.ValidationError(
                "All proposal sections must meet completeness thresholds before generation."
            )
        if proposal and proposal.alignment_checks.filter(blocking_issue=True).exists():
            raise serializers.ValidationError(
                "Blocking alignment issues must be resolved before generation."
            )
        if attrs.get("ai_generated", True):
            if not source_response_ids:
                raise serializers.ValidationError("AI-generated sections require source response IDs.")
            missing = set(source_response_ids) - set(
                models.StudentResponse.objects.filter(proposal=proposal).values_list("id", flat=True)
            )
            if missing:
                raise serializers.ValidationError("Source response IDs must exist for the proposal.")
        return attrs


class AITransparencyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AITransparencyLog
        fields = "__all__"


class QualityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QualityScore
        fields = "__all__"


class DefenseReadinessIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DefenseReadinessIndex
        fields = "__all__"


class SupervisorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupervisorReview
        fields = "__all__"


class ProposalVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProposalVersion
        fields = "__all__"


class ExportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExportRecord
        fields = "__all__"


class AlignmentCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlignmentCheck
        fields = "__all__"


class SupervisorPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupervisorPrompt
        fields = "__all__"
