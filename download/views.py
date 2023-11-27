from django.shortcuts import render
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import generics
from utility.models import MonthlyReport
from .auths import DownloadAuthentication
from api.user.permissions import CanAccessMonthlyReport

# Create your views here.

class MonthlyReportView(generics.RetrieveAPIView):
    """
    Download monthly report whose id is specified by `<pk>`.
    """
    swagger_schema = None
    authentication_classes = (DownloadAuthentication,)
    queryset = MonthlyReport.objects.all()

    def get_permissions(self):
        return (CanAccessMonthlyReport(id=self.kwargs['pk']),)
    
    def get(self, request, *args, **kwargs):
        view = request.query_params.get('view', None)
        attachment = view != '1'
        monthly_report = self.get_object()
        try:
            if attachment:
                return FileResponse(monthly_report.upload, as_attachment=True, filename=monthly_report.file_name)
            else:
                return FileResponse(monthly_report.upload)
        except OSError as e:
            return Response('File not found', 404)
