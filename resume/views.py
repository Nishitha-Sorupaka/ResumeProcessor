from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from resume.serializers import CandidateSerializer
from resume.models import Candidate
from pyresparser import ResumeParser
import os
import tempfile
# Create your views here.

class ResumeExtractView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        if resume_file:
            # Ensure file extension is valid
            valid_extensions = ['.pdf', '.docx']
            file_name = resume_file.name
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension not in valid_extensions:
                return Response({"error": "Unsupported file format. Please upload a .pdf or .docx file."}, status=status.HTTP_400_BAD_REQUEST)

            # Save the in-memory file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                for chunk in resume_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                # Use the temp file path with ResumeParser
                data = ResumeParser(temp_file_path).get_extracted_data()
                if data:
                    candidate = Candidate(
                        first_name=data.get('name', ''),
                        email=data.get('email', ''),
                        mobile_number=data.get('mobile_number', '')
                    )
                    candidate.save()
                    serializer = CandidateSerializer(candidate)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Could not extract data from the resume."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Handle any exceptions that occur during parsing
                return Response({"error": f"An error occurred while processing the resume: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                # Clean up the temporary file
                os.remove(temp_file_path)

        return Response({"error": "Resume file not provided"}, status=status.HTTP_400_BAD_REQUEST)


    '''
    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        if resume_file:
            data = ResumeParser(resume_file).get_extracted_data()
            # Assuming 'data' contains first_name, email, and mobile_number
            candidate = Candidate(
                first_name = data.get('first_name',''),
                email = data.get('email',''),
                mobile_number = data.get('mobile_number','')
            )
            candidate.save()
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        return Response({"error":"Resume file not provided"},status=400)

    '''