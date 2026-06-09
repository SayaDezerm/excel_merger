from rest_framework import serializers
from .models import MergeSession

class MergeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MergeSession
        fields = ['id', 'created_at', 'sheet_name', 'primary_file_name', 'output_file_name', 'status', 'error_message']