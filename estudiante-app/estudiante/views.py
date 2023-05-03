from django.shortcuts import render, redirect
from .models import Estudiante
from .forms import EstudianteForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# Create your views here.

def view_estudiante(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'view_estudiante.html', {'estudiantes': estudiantes})

def create_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EstudianteForm()
    return render(request, 'create_estudiante.html', {'forms': form})

def delete_estudiante(request, id):
    estudiante = Estudiante.objects.get(id=id)
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, 'El estudiante ha sido eliminado exitosamente.')
        return redirect('/')
    return render(request, 'delete_estudiante.html', {'estudiante': estudiante})

def edit_estudiante(request, id):
    estudiante = Estudiante.objects.get(id=id)
    forms = EstudianteForm(request.POST or None, instance=estudiante)
    if forms.is_valid() and request.POST:
        forms.save()
        return redirect('/')
    return render(request, 'edit_estudiante.html', {'forms': forms})


# def edit_estudiante(request, id):
#     estudiante = Estudiante.objects.get(id=id)
#     if request.method == 'POST':
#         forms = EstudianteForm(request.POST, request.FILES, instance=estudiante)
#         if forms.is_valid():
#             # Eliminar imagen anterior
#             if estudiante.foto:
#                 default_storage.delete(estudiante.foto.name)
#             # Guardar nueva imagen
#             foto = forms.cleaned_data.get('foto')
#             if foto:
#                 filename = f'{estudiante.codigo}/{foto.name}'
#                 path = default_storage.save(f'imagenes/{filename}', ContentFile(foto.read()))
#                 estudiante.foto.name = path
#             # Guardar otros datos del formulario
#             estudiante.nombre = forms.cleaned_data.get('nombre')
#             estudiante.apellido = forms.cleaned_data.get('apellido')
#             estudiante.codigo = forms.cleaned_data.get('codigo')
#             estudiante.correo = forms.cleaned_data.get('correo')
#             estudiante.save()
#             messages.success(request, 'El estudiante ha sido actualizado exitosamente.')
#             return redirect('/')
#     else:
#         forms = EstudianteForm(instance=estudiante)
#     return render(request, 'edit_estudiante.html', {'forms': forms})