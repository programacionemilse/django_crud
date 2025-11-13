from django.shortcuts import render, redirect,get_object_or_404
#importamos el formulario que django ofrece para el registro y logeo de usuarios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#importamos modelo donde se guardan los usuarios que provee django por defecto
from django.contrib.auth.models import User
#importacion de login y logout que trae django
#authenticate para el inicio de sesion
from django.contrib.auth import login,logout,authenticate
#error de integridad en la base de datos por ejemplo registros duplicados
from django.db import IntegrityError
#importo el formulario que cree
from .forms import crearTareaForm
#importamos el modelo de las tareas para poder usarlo
from .models import Tarea
#para usar fechas
from django.utils import timezone
#importamos decoradores para poder limitar el acceso al inicio de sesion
from django.contrib.auth.decorators import login_required

# Create your views here.
def holaMundo(request):
    return render(request, 'index.html')

def registroUsuario(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form':UserCreationForm})    
    else:
        #para ver los datos que se enviaron desde el formulario
        #print(request.POST)

        if request.POST['password1'] == request.POST['password2']:
            #registro de usuarios
            try:
                #esto crea un objeto usuario no lo guarda en la base de datos.
                usuario = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                usuario.save() #guarda en la BD el usuario nuevo

                #creamos la cookies con el logeo del usuario (una sesion con el usuario)
                login(request,usuario)
                return redirect('tareas')
                
            except IntegrityError:
                return render(request, 'signup.html', {'form':UserCreationForm,'error':"El usuario ingresado ya existe"})
            
        return render(request, 'signup.html', {'form':UserCreationForm, 'error':"Las contraseñas ingresadas no coinciden"})

@login_required
def tareas(request):
    #todas_tareas = Tarea.objects.all() #trae todos los datos de la tabla tareas de la base de datos
    todas_mis_tareas = Tarea.objects.filter(usuario = request.user,fechora_completada__isnull=True)
    #return render(request, 'tareas.html',{'todas_tareas':todas_tareas})
    return render(request, 'tareas.html',{'todas_mis_tareas':todas_mis_tareas})

@login_required
def tareasCompletas(request):
    #todas_tareas = Tarea.objects.all() #trae todos los datos de la tabla tareas de la base de datos
    todas_mis_tareas = Tarea.objects.filter(usuario = request.user,fechora_completada__isnull=False).order_by('-fechora_completada')
    #return render(request, 'tareas.html',{'todas_tareas':todas_tareas})
    return render(request, 'tareas.html',{'todas_mis_tareas':todas_mis_tareas})

@login_required
def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html',{'form':crearTareaForm})
    else:
        try:
            datos_form=crearTareaForm(request.POST)
            nueva_tarea=datos_form.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'crear_tarea.html',{'form':crearTareaForm,'error':"Ingresar  datos validos"})

#Solo filtro por id una tarea para el detalle
def detalleTareaAnterior(request,tarea_id):
    #d_tarea=Tarea.objects.get(pk = tarea_id) esto sino encuentra el servidor se cae
    d_tarea = get_object_or_404(Tarea,pk=tarea_id)
    form = crearTareaForm(instance=d_tarea)
    return render(request, 'detalle_tarea.html',{'d_tarea':d_tarea, 'form':form})

@login_required
def detalleTarea(request,tarea_id):
    if request.method == 'GET':
        d_tarea = get_object_or_404(Tarea,pk=tarea_id, usuario = request.user)
        form = crearTareaForm(instance=d_tarea)
        return render(request, 'detalle_tarea.html',{'d_tarea':d_tarea, 'form':form})
    else:
        try:
            d_tarea = get_object_or_404(Tarea,pk=tarea_id)
            form = crearTareaForm(request.POST, instance=d_tarea)
            form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'detalle_tarea.html',{'d_tarea':d_tarea, 'form':form, 'error':"Error al editar el registro"})

@login_required
def tareaCompleta(request,tarea_id):
    tareaComp = get_object_or_404(Tarea,pk=tarea_id,usuario = request.user)
    if request.method == 'POST':
        tareaComp.fechora_completada = timezone.now()
        tareaComp.save()
        return redirect('tareas')

@login_required
def tareaEliminada(request,tarea_id):
    tareaEliminar = get_object_or_404(Tarea,pk=tarea_id,usuario = request.user)
    if request.method == 'POST':
        tareaEliminar.delete()
        return redirect('tareas')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('index')

def iniciarSesion(request):
    if request.method == 'GET':
        return render(request,'login.html',{'form':AuthenticationForm})   
    else:
        usuario=authenticate(request,username=request.POST['username'],password=request.POST['password'])

        #valido si se pudo encontrar el usuario en los registrados
        if usuario is None:
            return render(request,'login.html',{'form':AuthenticationForm,'error':'Usuario o contraseña incorrecta'})
        else:
            login(request, usuario)
            return redirect('tareas')
