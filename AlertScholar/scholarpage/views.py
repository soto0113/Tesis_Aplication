from django.shortcuts import render, redirect
from .models import Estudiante
from .forms import EstudianteForm
from .models import Docente
from .forms import DocenteForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from django.shortcuts import render
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle

# Directorio donde se encuentra el archivo modelo.pickle
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modelo.pickle')

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

def view_docente(request):
    docentes = Docente.objects.all()
    return render(request, 'view_docente.html', {'docentes': docentes})

@login_required
def create_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DocenteForm()
    return render(request, 'create_docente.html', {'form': form})

@login_required
def delete_docente(request, id):
    docente = Docente.objects.get(id=id)
    if request.method == 'POST':
        docente.delete()
        messages.success(request, 'El docente ha sido eliminado exitosamente.')
        return redirect('/')
    return render(request, 'delete_docente.html', {'docente': docente})

@login_required
def edit_docente(request, id):
    docente = Docente.objects.get(id=id)
    form = DocenteForm(request.POST or None, instance=docente)
    if form.is_valid() and request.POST:
        form.save()
        return redirect('/')
    return render(request, 'edit_docente.html', {'forms': form})

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

@login_required
def carga_excel(request):
    if request.method == 'POST':
        file = request.FILES['excel_file']
        df = pd.read_excel(file)
        columns = df.columns.tolist()
        desired_columns = ['Students', 'Workshop 1_10%', 'Exam 1_ 20%', 'CollaborativeActivity_10%']
        X = df[desired_columns]
        y = df['Grade']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Bosques Aleatorios
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        r2_rf = r2_score(y_test, y_pred_rf)
        mae = mean_absolute_error(y_test, y_pred_rf)
        mape = mean_absolute_percentage_error(y_test, y_pred_rf)
        rmse = mean_squared_error(y_test, y_pred_rf, squared=False)

        results = X_test.copy()
        results['Grade (Real)'] = y_test
        results['Grade prediccion (Bosques Aleatorios)'] = y_pred_rf

        results = results.rename(columns={'Workshop 1_10%': 'Workshop__1_10', 'Exam 1_ 20%': 'Exam_1_20', 'CollaborativeActivity_10%': 'CollaborativeActivity_10', 'Grade (Real)': 'Grade__Real', 'Grade prediccion (Bosques Aleatorios)': 'Grade__prediccion__Bosques__Aleatorios'})  
        results = results.reset_index(drop=True)

        # Calcular los estadísticos del curso
        course_stats = {
            'media': np.mean(y),
            'mediana': np.median(y),
            'moda': df['Grade'].mode()[0],
            'desviacion_estandar': np.std(y)
        }

        # Crear la gráfica de dispersión
        plt.scatter(results['Grade__prediccion__Bosques__Aleatorios'], results['Grade__prediccion__Bosques__Aleatorios'], color='green', label='Predicción')
        plt.scatter(results['Grade__Real'], results['Grade__Real'], color='red', label='Real')

        # Agregar los valores estadísticos a la gráfica
        plt.scatter(course_stats['media'], course_stats['media'], color='blue', label='Media')
        plt.scatter(course_stats['mediana'], course_stats['mediana'], color='purple', label='Mediana')
        plt.scatter(course_stats['moda'], course_stats['moda'], color='orange', label='Moda')
        plt.scatter(course_stats['desviacion_estandar'], course_stats['desviacion_estandar'], color='yellow', label='Desviación Estándar')

        # Configurar la leyenda y los ejes
        plt.legend()
        plt.xlabel('Valor Real')
        plt.ylabel('Valor Predicho')

        # Guardar la gráfica como una imagen
        plt.savefig('scholarpage/static/scatter_plot.png')

        return render(request, 'regresion_bosques_aleatorios.html', {'columns': columns, 'results': results, 'r2_rf': r2_rf, 'mae': mae, 'mape': mape, 'rmse': rmse})

    return render(request, 'carga_excel.html')

@login_required
def carga_excel2(request):
    if request.method == 'POST':
        file = request.FILES['excel_file']
        data = pd.read_excel(file)

        # Seleccionar las columnas relevantes
        columns = ['Workshop 1_10%', 'CollaborativeActivity_10%', 'Exam 1_ 20%', 'Grade']
        data = data[columns]

        # Eliminar filas con valores faltantes
        data = data.dropna()

        # Separar características (X) y variable objetivo (y)
        X = data[['Workshop 1_10%', 'CollaborativeActivity_10%', 'Exam 1_ 20%']]
        y = data['Grade']

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Crear y entrenar el modelo Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Realizar predicciones en el conjunto de prueba
        y_pred = model.predict(X_test)

        # Calcular el error cuadrático medio (MSE)
        mse = mean_squared_error(y_test, y_pred)
        print('Error cuadrático medio:', mse)

        # Mostrar las características y la nota final en el conjunto de prueba
        results = X_test.copy()
        results['Nota'] = y_test
        results['Prediccion'] = y_pred
        results = results.rename(columns={'Workshop 1_10%': 'Workshop__1_10', 'Exam 1_ 20%': 'Exam_1_20', 'CollaborativeActivity_10%': 'CollaborativeActivity_10', 'Grade (Real)': 'Grade__Real', 'Grade prediccion (Bosques Aleatorios)': 'Grade__prediccion__Bosques__Aleatorios'})  
        results = results.reset_index(drop=True)
        print(results)
        
        return render(request, 'result.html', {'columns': columns, 'results': results})

    return render(request, 'carga_excel2.html')