from django.urls import path
from resume.views import ResumeExtractView

urlpatterns = [
    path('api/extract_resume/',ResumeExtractView.as_view(),name='extract_resume'),
]