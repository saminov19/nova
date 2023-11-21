from django.urls import path
from app.views import create_google_doc

urlpatterns = [
    path('create_document/', create_google_doc, name='create_google_doc'),
]


