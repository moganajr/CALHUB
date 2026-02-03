from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademicProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("institution", models.CharField(max_length=255)),
                ("department", models.CharField(max_length=255)),
                ("degree_level", models.CharField(choices=[("BSC", "BSc"), ("MSC", "MSc"), ("PHD", "PhD")], max_length=8)),
                ("research_interests", models.TextField(blank=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Proposal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("status", models.CharField(choices=[("DRAFT", "Draft"), ("IN_REVIEW", "In Review"), ("REVISION_REQUIRED", "Revision Required"), ("APPROVED", "Approved")], default="DRAFT", max_length=32)),
                ("degree_level", models.CharField(choices=[("BSC", "BSc"), ("MSC", "MSc"), ("PHD", "PhD")], max_length=8)),
                ("problem_statement", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="proposals", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ProposalSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("order", models.PositiveIntegerField(default=0)),
                ("completeness_score", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("completeness_threshold", models.DecimalField(decimal_places=2, default=70, max_digits=5)),
                ("is_locked", models.BooleanField(default=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sections", to="core.proposal")),
            ],
            options={"ordering": ["order"], "unique_together": {("proposal", "name")}},
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("prompt", models.TextField()),
                ("help_text", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_required", models.BooleanField(default=True)),
                ("critical_for_alignment", models.BooleanField(default=False)),
                ("parent", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="sub_questions", to="core.question")),
                ("section", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="core.proposalsection")),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="StudentResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("response_text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="core.proposal")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="core.question")),
            ],
            options={"unique_together": {("proposal", "question")}},
        ),
        migrations.CreateModel(
            name="ResearchObjective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="objectives", to="core.proposal")),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="ResearchQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
                ("objective", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.researchobjective")),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="research_questions", to="core.proposal")),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Hypothesis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="hypotheses", to="core.proposal")),
                ("research_question", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.researchquestion")),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="MethodologyComponent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("component_type", models.CharField(max_length=120)),
                ("description", models.TextField()),
                ("justification", models.TextField()),
                ("degree_level", models.CharField(choices=[("BSC", "BSc"), ("MSC", "MSc"), ("PHD", "PhD")], max_length=8)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="methodology_components", to="core.proposal")),
            ],
        ),
        migrations.CreateModel(
            name="GeneratedSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("section_name", models.CharField(max_length=120)),
                ("content", models.TextField()),
                ("ai_generated", models.BooleanField(default=True)),
                ("ai_contribution_percentage", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("source_response_ids", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="generated_sections", to="core.proposal")),
            ],
        ),
        migrations.CreateModel(
            name="AITransparencyLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("model_name", models.CharField(max_length=120)),
                ("prompt", models.TextField()),
                ("input_response_ids", models.JSONField(default=list)),
                ("output_summary", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("generated_section", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_logs", to="core.generatedsection")),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_logs", to="core.proposal")),
            ],
        ),
        migrations.CreateModel(
            name="QualityScore",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("category", models.CharField(max_length=120)),
                ("score", models.DecimalField(decimal_places=2, max_digits=5)),
                ("explanation", models.TextField()),
                ("algorithm_version", models.CharField(max_length=50)),
                ("computed_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quality_scores", to="core.proposal")),
            ],
        ),
        migrations.CreateModel(
            name="DefenseReadinessIndex",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.DecimalField(decimal_places=2, max_digits=5)),
                ("rationale", models.TextField()),
                ("computed_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="defense_readiness", to="core.proposal")),
            ],
        ),
        migrations.CreateModel(
            name="SupervisorReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("DRAFT", "Draft"), ("IN_REVIEW", "In Review"), ("REVISION_REQUIRED", "Revision Required"), ("APPROVED", "Approved")], max_length=32)),
                ("comments", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="core.proposal")),
                ("reviewer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="supervisor_reviews", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ProposalVersion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("version_number", models.PositiveIntegerField()),
                ("snapshot", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="core.proposal")),
            ],
            options={"unique_together": {("proposal", "version_number")}},
        ),
        migrations.CreateModel(
            name="ExportRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("export_type", models.CharField(choices=[("DOCX", "DOCX"), ("PDF", "PDF")], max_length=10)),
                ("file_path", models.CharField(max_length=255)),
                ("ai_contribution_statement", models.TextField()),
                ("quality_summary", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exports", to="core.proposal")),
            ],
        ),
        migrations.CreateModel(
            name="AlignmentCheck",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("check_type", models.CharField(max_length=120)),
                ("status", models.CharField(max_length=20)),
                ("details", models.TextField()),
                ("blocking_issue", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="alignment_checks", to="core.proposal")),
            ],
        ),
    ]
