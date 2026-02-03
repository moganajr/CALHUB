from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register("profiles", views.AcademicProfileViewSet)
router.register("proposals", views.ProposalViewSet)
router.register("sections", views.ProposalSectionViewSet)
router.register("questions", views.QuestionViewSet)
router.register("responses", views.StudentResponseViewSet)
router.register("objectives", views.ResearchObjectiveViewSet)
router.register("research-questions", views.ResearchQuestionViewSet)
router.register("hypotheses", views.HypothesisViewSet)
router.register("methodology", views.MethodologyComponentViewSet)
router.register("generated-sections", views.GeneratedSectionViewSet)
router.register("ai-logs", views.AITransparencyLogViewSet)
router.register("quality-scores", views.QualityScoreViewSet)
router.register("dri", views.DefenseReadinessIndexViewSet)
router.register("reviews", views.SupervisorReviewViewSet)
router.register("versions", views.ProposalVersionViewSet)
router.register("exports", views.ExportRecordViewSet)
router.register("alignment-checks", views.AlignmentCheckViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
