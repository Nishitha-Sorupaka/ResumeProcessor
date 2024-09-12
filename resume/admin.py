from django.contrib import admin
from resume.models import Candidate
# Register your models here.
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['first_name','email','mobile_number']
admin.site.register(Candidate,CandidateAdmin)

