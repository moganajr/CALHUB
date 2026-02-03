from rest_framework import viewsets

from core import models
from core import serializers


class AcademicProfileViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicProfile.objects.all()
    serializer_class = serializers.AcademicProfileSerializer


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = models.Proposal.objects.all()
    serializer_class = serializers.ProposalSerializer


class ProposalSectionViewSet(viewsets.ModelViewSet):
    queryset = models.ProposalSection.objects.all()
    serializer_class = serializers.ProposalSectionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class StudentResponseViewSet(viewsets.ModelViewSet):
    queryset = models.StudentResponse.objects.all()
    serializer_class = serializers.StudentResponseSerializer


class ResearchObjectiveViewSet(viewsets.ModelViewSet):
    queryset = models.ResearchObjective.objects.all()
    serializer_class = serializers.ResearchObjectiveSerializer


class ResearchQuestionViewSet(viewsets.ModelViewSet):
    queryset = models.ResearchQuestion.objects.all()
    serializer_class = serializers.ResearchQuestionSerializer


class HypothesisViewSet(viewsets.ModelViewSet):
    queryset = models.Hypothesis.objects.all()
    serializer_class = serializers.HypothesisSerializer


class MethodologyComponentViewSet(viewsets.ModelViewSet):
    queryset = models.MethodologyComponent.objects.all()
    serializer_class = serializers.MethodologyComponentSerializer


class GeneratedSectionViewSet(viewsets.ModelViewSet):
    queryset = models.GeneratedSection.objects.all()
    serializer_class = serializers.GeneratedSectionSerializer


class AITransparencyLogViewSet(viewsets.ModelViewSet):
    queryset = models.AITransparencyLog.objects.all()
    serializer_class = serializers.AITransparencyLogSerializer


class QualityScoreViewSet(viewsets.ModelViewSet):
    queryset = models.QualityScore.objects.all()
    serializer_class = serializers.QualityScoreSerializer


class DefenseReadinessIndexViewSet(viewsets.ModelViewSet):
    queryset = models.DefenseReadinessIndex.objects.all()
    serializer_class = serializers.DefenseReadinessIndexSerializer


class SupervisorReviewViewSet(viewsets.ModelViewSet):
    queryset = models.SupervisorReview.objects.all()
    serializer_class = serializers.SupervisorReviewSerializer


class ProposalVersionViewSet(viewsets.ModelViewSet):
    queryset = models.ProposalVersion.objects.all()
    serializer_class = serializers.ProposalVersionSerializer


class ExportRecordViewSet(viewsets.ModelViewSet):
    queryset = models.ExportRecord.objects.all()
    serializer_class = serializers.ExportRecordSerializer


class AlignmentCheckViewSet(viewsets.ModelViewSet):
    queryset = models.AlignmentCheck.objects.all()
    serializer_class = serializers.AlignmentCheckSerializer
