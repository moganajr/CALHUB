from pathlib import Path

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models
from core import serializers
from core import ai
from core import exports
from core import services


class AcademicProfileViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicProfile.objects.all()
    serializer_class = serializers.AcademicProfileSerializer


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = models.Proposal.objects.all()
    serializer_class = serializers.ProposalSerializer

    @action(detail=True, methods=["post"])
    def refresh_governance(self, request, pk=None):
        proposal = self.get_object()
        services.refresh_governance_metrics(proposal)
        return Response({"status": "refreshed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def generate_supervisor_prompts(self, request, pk=None):
        proposal = self.get_object()
        proposal.supervisor_prompts.all().delete()
        prompts = services.generate_supervisor_prompts(proposal)
        models.SupervisorPrompt.objects.bulk_create(prompts)
        return Response({"created": len(prompts)}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def generate_section(self, request, pk=None):
        proposal = self.get_object()
        section_name = request.data.get("section_name")
        response_ids = request.data.get("response_ids", [])
        model_name = request.data.get("model_name", "structuring-only")
        contribution = request.data.get("ai_contribution_percentage", 0)
        responses = list(models.StudentResponse.objects.filter(proposal=proposal, id__in=response_ids))
        content = ai.generate_structured_section(proposal, section_name, responses)
        generated_data = {
            "proposal": proposal.id,
            "section_name": section_name,
            "content": content,
            "ai_generated": True,
            "ai_contribution_percentage": contribution,
            "source_response_ids": response_ids,
        }
        serializer = serializers.GeneratedSectionSerializer(data=generated_data)
        serializer.is_valid(raise_exception=True)
        generated_section = serializer.save()
        models.AITransparencyLog.objects.create(
            proposal=proposal,
            generated_section=generated_section,
            model_name=model_name,
            prompt="Structured from student responses only.",
            input_response_ids=response_ids,
            output_summary="Structured section with no new claims.",
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def export(self, request, pk=None):
        proposal = self.get_object()
        export_type = request.data.get("export_type", "DOCX")
        output_dir = request.data.get("output_dir", "exports")
        record = exports.export_proposal(proposal, export_type, output_dir=Path(output_dir))
        return Response(serializers.ExportRecordSerializer(record).data, status=status.HTTP_201_CREATED)


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


class VariableViewSet(viewsets.ModelViewSet):
    queryset = models.Variable.objects.all()
    serializer_class = serializers.VariableSerializer


class AnalysisPlanViewSet(viewsets.ModelViewSet):
    queryset = models.AnalysisPlan.objects.all()
    serializer_class = serializers.AnalysisPlanSerializer


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


class SupervisorPromptViewSet(viewsets.ModelViewSet):
    queryset = models.SupervisorPrompt.objects.all()
    serializer_class = serializers.SupervisorPromptSerializer
