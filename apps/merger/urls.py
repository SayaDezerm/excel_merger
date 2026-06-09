from django.urls import path
from . import views

urlpatterns = [
    path('', views.MergeView, name='merge'),
    path('api/upload/', views.UploadFolderView.as_view()),
    path('api/sheets/', views.GetSheetsView.as_view()),
    path('api/columns/', views.GetColumnsView.as_view()),
    path('api/merge/', views.MergeProcessView.as_view()),
    path('api/history/', views.MergeHistoryView.as_view()),
]