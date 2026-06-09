from django.db import models

class MergeSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    sheet_name = models.CharField(max_length=255)
    primary_file_name = models.CharField(max_length=255)
    all_files = models.JSONField(default=list)
    selected_columns = models.JSONField(default=list)
    output_file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session #{self.pk} — {self.primary_file_name} ({self.status})"