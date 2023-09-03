from django.db import models
from django.contrib.auth.hashers import make_password

class Estudiante(models.Model):
    foto = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    codigo = models.CharField(max_length=11)
    password = models.CharField(max_length=128)
    correo = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        # Hashear la contraseña antes de guardarla
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        

class Docente(models.Model):
    foto = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=11)
    curso = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    correo = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        # Hashear la contraseña antes de guardarla
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
'''
    def __str__(self):
        fila = self.nombre + " "+ self.apellido
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()
''' 
class meta ():
    estud = TabError
    

    # def save(self, *args, **kwargs):
    #     # Si la instancia ya existe, borre su imagen anterior
    #     try:
    #         this = Estudiante.objects.get(id=self.id)
    #         if this.foto != self.foto:
    #             this.foto.delete()
    #     except Estudiante.DoesNotExist:
    #         pass

    #     # Agregue un sufijo aleatorio al nombre del archivo de imagen
    #     ext = os.path.splitext(self.foto.name)[1]
    #     self.foto.name = 'imagenes/' + str(uuid.uuid4()) + ext

    #     # Guarde la instancia
    #     super(Estudiante, self).save(*args, **kwargs)