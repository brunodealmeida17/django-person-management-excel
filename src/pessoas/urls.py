from django.urls import path
from .views import PessoaUploadView, PessoaExportView

urlpatterns = [    
    path('upload-excel/', PessoaUploadView.as_view(), name='upload-excel'),
    path('download-planilha/', PessoaExportView.as_view(), name='download-excel'),
    
]