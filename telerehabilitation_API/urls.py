"""telerehabilitation_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from telerehabilitation_API.authentication.views import UserViewSet, PatientViewSet
from telerehabilitation_API.authentication.views.admin_view_set import AdminViewSet
from telerehabilitation_API.authentication.views.therapist_view_set import TherapistViewSet
from telerehabilitation_API.therapy.views import TherapyViewSet
from telerehabilitation_API.therapy.views.exercise_result_view_set import ExerciseResultViewSet, \
   ExerciseResultResultsViewSet, ExerciseResultConceptViewSet
from telerehabilitation_API.therapy.views.exercise_view_set import ExerciseViewSet
from telerehabilitation_API.therapy.views.routine_view_set import RoutineViewSet
from telerehabilitation_API.therapy.views.scheduled_training_diff_view_set import ScheduledTrainingDiffViewSet
from telerehabilitation_API.therapy.views.scheduled_training_view_set import ScheduledTrainingViewSet
from telerehabilitation_API.therapy.views.skeleton_view_set import SkeletonViewSet
from telerehabilitation_API.therapy.views.therapist_patients_view_set import TherapistPatientsViewSet
from telerehabilitation_API.therapy.views.training_view_set import TrainingViewSet, TrainingEndViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Telerehabilitation API",
      default_version='v1',
      description="Telerehabilitation API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="csantosr@unal.edu.co"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'auth/users', UserViewSet)
router.register(r'therapies', TherapyViewSet)
router.register(r'routines', RoutineViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'skeleton', SkeletonViewSet)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   path('', include(router.urls)),
   path('patients', PatientViewSet.as_view()),
   path('therapists', TherapistViewSet.as_view()),
   path('admins', AdminViewSet.as_view()),
   path('scheduled_training', ScheduledTrainingViewSet.as_view()),
   path('scheduled_training/diffs', ScheduledTrainingDiffViewSet.as_view()),
   path('therapist_patient', TherapistPatientsViewSet.as_view()),
   path('training', TrainingViewSet.as_view()),
   path('training/end', TrainingEndViewSet.as_view()),
   path('exercise_results', ExerciseResultViewSet.as_view()),
   path('exercise_results/<int:exercise_result_id>/results', ExerciseResultResultsViewSet.as_view()),
   path('exercise_results/<int:exercise_result_id>/concept', ExerciseResultConceptViewSet.as_view()),
]
