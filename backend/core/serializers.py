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


class GeneratedSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GeneratedSection
        fields = "__all__"


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
