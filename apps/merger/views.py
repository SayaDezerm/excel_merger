from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from .models import MergeSession
from .serializers import MergeSessionSerializer
import pandas as pd
import json
    
def MergeView(request):
    return render(request, 'merger/html/index.html')


class UploadFolderView(APIView):
    def post(self, request):
        files = request.FILES.getlist("files")
        return services.upload_service(*files)


class GetSheetsView(APIView):
    def post(self, request):
        file = request.FILES.get("primary_file")

        if not file:
            return Response({"error": "No files."}, status=status.HTTP_400_BAD_REQUEST)

        xl = pd.ExcelFile(file)
        return Response({"sheets": xl.sheet_names}, status=status.HTTP_200_OK)


class GetColumnsView(APIView):
    def post(self, request):
        file = request.FILES.get("primary_file")
        sheet_name = request.data.get("sheet_name")
        return services.get_columns_service(file, sheet_name)


class MergeProcessView(APIView):
    def post(self, request):
        files = request.FILES.getlist("files")
        sheet_name = request.data.get("sheet_name")
        selected_columns = request.data.get("selected_columns")
        primary_file_name = request.data.get("primary_file_name")
        output_file = request.FILES.get("output_file")

        session = MergeSession.objects.create(
            sheet_name=sheet_name,
            primary_file_name=primary_file_name,
            output_file_name=output_file.name,
            all_files=[f.name for f in files],
            selected_columns=json.loads(selected_columns),
            status='pending'
        )

        response = services.merge_service(
            sheet_name, selected_columns, primary_file_name, output_file, *files
        )

        if hasattr(response, 'status_code') and response.status_code == 200:
            session.status = 'success'
        else:
            session.status = 'failed'
            try:
                session.error_message = response.data.get('error', '')
            except Exception:
                pass

        session.save()
        return response


class MergeHistoryView(APIView):
    def get(self, request):
        sessions = MergeSession.objects.order_by('-created_at')
        serializer = MergeSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)