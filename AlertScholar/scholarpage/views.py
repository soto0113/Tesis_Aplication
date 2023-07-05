from django.shortcuts import render, redirect
from .models import Estudiante
from .forms import EstudianteForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from django.shortcuts import render


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

def carga_excel(request):
    if request.method == 'POST':
        file = request.FILES['excel_file']
        df = pd.read_excel(file)
        columns = df.columns.tolist()

        X = df[columns]
        y = df['Grade']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

        # Bosques Aleatorios
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        r2_rf = r2_score(y_test, y_pred_rf)

        results = X_test.copy()
        results['Grade (Real)'] = y_test
        results['Grade prediccion (Bosques Aleatorios)'] = y_pred_rf

        results = results.rename(columns={'Workshop 1_10%': 'Workshop__1_10', 'Exam 1_ 20%': 'Exam_1_20', 'CollaborativeActivity_10%': 'CollaborativeActivity_10', 'Grade (Real)': 'Grade__Real', 'Grade prediccion (Bosques Aleatorios)': 'Grade__prediccion__Bosques__Aleatorios'})  
        results = results.reset_index(drop=True)

        return render(request, 'regresion_bosques_aleatorios.html', {'columns': columns, 'results': results, 'r2_rf': r2_rf})

    return render(request, 'carga_excel.html')


def regresion_bosques_aleatoriosddd(request):
    
        file = request.FILES['excel_file']
        df = pd.read_excel(file)
        columns = ['Students', 'Workshop 1_10%', 'CollaborativeActivity_10%', 'Exam 1_ 20%']

        X = df[columns]
        y = df['Grade']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

        # Bosques Aleatorios
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        r2_rf = r2_score(y_test, y_pred_rf)

        results = X_test.copy()
        results['Grade (Real)'] = y_test
        results['Grade precision (Bosques Aleatorios)'] = y_pred_rf

        results = results.rename(columns={'Workshop 1_10%': 'Workshop__1_10', 'Exam 1_ 20%': 'Exam_1_20', 'CollaborativeActivity_10%': 'CollaborativeActivity_10', 'Grade (Real)': 'Grade__Real', 'Grade precision (Bosques Aleatorios)': 'Grade__precision__Bosques__Aleatorios'})  
        results = results.reset_index(drop=True)

        return render(request, 'regresion_bosques_aleatorios.html', {'results': results, 'r2_rf': r2_rf})



def regresion_bosques_aleatorios(request):
    url = 'https://raw.githubusercontent.com/cgiohidalgo/repositoryclass/main/datatest/data_stutent_predict_EN.csv'
    data = pd.read_csv(url, sep=';')

    columns = ['Students', 'Workshop 1_10%', 'CollaborativeActivity_10%', 'Exam 1_ 20%']

    X = data[columns]
    y = data['Grade']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    # Bosques Aleatorios
    rf_model = RandomForestRegressor()
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    r2_rf = r2_score(y_test, y_pred_rf)

    results = X_test.copy()
    results['Grade (Real)'] = y_test
    results['Grade precision (Bosques Aleatorios)'] = y_pred_rf

    results = results.rename(columns={'Workshop 1_10%': 'Workshop__1_10', 'Exam 1_ 20%': 'Exam_1_20', 'CollaborativeActivity_10%': 'CollaborativeActivity_10', 'Grade (Real)': 'Grade__Real', 'Grade precision (Bosques Aleatorios)': 'Grade__precision__Bosques__Aleatorios'})  
    results = results.reset_index(drop=True)


    return render(request, 'regresion_bosques_aleatorios.html', {'results': results, 'r2_rf': r2_rf})
