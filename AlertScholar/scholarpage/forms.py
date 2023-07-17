from django import forms
from .models import Estudiante
from .models import Docente

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'