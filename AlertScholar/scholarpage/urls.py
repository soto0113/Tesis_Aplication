from django.urls import path
from .views import view_estudiante, create_estudiante, delete_estudiante, edit_estudiante, base, carga_excel, carga_excel2, view_docente, create_docente, edit_docente, delete_docente#, nueva_prediccion
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', base, name='base'),
    #path('login_estudiante', login_estudiante, name="login_estudiante"),
    path('view_estudiante/', view_estudiante, name="estudiantes"),
    path('new_estudiante/', create_estudiante, name="create_estudiante"),
    path('delete_estudiante/<int:id>', delete_estudiante, name="delete_estudiante"),
    path('edit_estudiante/<int:id>', edit_estudiante, name="edit_estudiante"),
    path('view_docente/', view_docente, name='docentes'),
    path('create_docente/', create_docente, name='create_docente'),
    path('edit_docente/<int:id>/', edit_docente, name='edit_docente'),
    path('delete_docente/<int:id>/', delete_docente, name='delete_docente'),
    path('carga_excel', carga_excel, name='carga_excel'),
    path('carga_excel2', carga_excel2, name='carga_excel2'),
  #  path('nueva_prediccion/', nueva_prediccion, name='nueva_prediccion'),
   # path('logout/', logout_estudiante, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)