from rest_framework.serializers import ModelSerializer
from resume.models import Candidate
class CandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'