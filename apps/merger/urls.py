from django.urls import path
from . import views

urlpatterns = [
    path('', views.MergeView, name="merger"),
    path('api/upload/', views.UploadFolderView.as_view(), name="upload-folder"),
    path('api/sheets/', views.GetSheetsView.as_view(), name="get-sheets"),
    path('api/columns/', views.GetColumnsView.as_view(), name="get-columns"),
    path('api/merge/', views.MergeProcessView.as_view(), name="merge-process"),
]