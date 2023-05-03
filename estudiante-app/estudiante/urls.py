from django.urls import path
from .views import view_estudiante, create_estudiante, delete_estudiante, edit_estudiante

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', view_estudiante, name="estudiantes"),
    path('new_estudiante/', create_estudiante, name="create_estudiante"),
    path('delete_estudiante/<int:id>', delete_estudiante, name="delete_estudiante"),
    path('edit_estudiante/<int:id>', edit_estudiante, name="edit_estudiante"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)