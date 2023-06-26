from django.shortcuts import render, redirect
from .models import Estudiante
from .forms import EstudianteForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def base(request):
    return render(request, 'base.html')

def view_estudiante(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'view_estudiante.html', {'estudiantes': estudiantes})

@login_required
def create_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EstudianteForm()
    return render(request, 'create_estudiante.html', {'forms': form})

@login_required
def delete_estudiante(request, id):
    estudiante = Estudiante.objects.get(id=id)
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, 'El estudiante ha sido eliminado exitosamente.')
        return redirect('/')
    return render(request, 'delete_estudiante.html', {'estudiante': estudiante})

@login_required
def edit_estudiante(request, id):
    estudiante = Estudiante.objects.get(id=id)
    forms = EstudianteForm(request.POST or None, instance=estudiante)
    if forms.is_valid() and request.POST:
        forms.save()
        return redirect('/')
    return render(request, 'edit_estudiante.html', {'forms': forms})

def login_estudiante(request):
    if request.method == 'POST':
        # Obtener el usuario y la contraseña del formulario
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        # Si el usuario es autenticado correctamente, iniciar sesión y redirigir al usuario a la página de inicio
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # Si la autenticación falla, mostrar un mensaje de error
            messages.error(request, 'El usuario o la contraseña son incorrectos.')
    else:
        # Si el método no es POST, mostrar un mensaje de información
        messages.info(request, 'Por favor inicia sesión.')
    
    # Renderizar el formulario de inicio de sesión
    return render(request, 'login_estudiante.html')

@login_required
def logout_estudiante(request):
    logout(request)
    return redirect('/')