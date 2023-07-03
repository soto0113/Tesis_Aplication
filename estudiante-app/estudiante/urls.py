from django.urls import path
from .views import view_estudiante, create_estudiante, delete_estudiante, edit_estudiante, base, login_estudiante,logout_estudiante, carga_excel
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', base, name='base'),
    path('login_estudiante', login_estudiante, name="login_estudiante"),
    path('view_estudiante', view_estudiante, name="estudiantes"),
    path('new_estudiante/', create_estudiante, name="create_estudiante"),
    path('delete_estudiante/<int:id>', delete_estudiante, name="delete_estudiante"),
    path('edit_estudiante/<int:id>', edit_estudiante, name="edit_estudiante"),
    path('carga_excel', carga_excel, name='carga_excel'),
    path('logout/', logout_estudiante, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)