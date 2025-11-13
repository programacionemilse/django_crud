"""
URL configuration for Proyecto_CRUD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Tareas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.holaMundo,name='index'),
    path('registrarse/',views.registroUsuario,name='registrarse'),
    path('cerrarSesion/',views.cerrarSesion,name='cerrarSesion'),
    path('login/',views.iniciarSesion,name='login'),
    path('tareas/',views.tareas,name='tareas'),
    path('tareas_completas/',views.tareasCompletas,name='tareas_completas'),
    path('tareas/crear/',views.crear_tarea,name='crear_tarea'),
    path('tareas/detalle/<int:tarea_id>/',views.detalleTarea,name='detalleTarea'),
    path('tareas/detalle/<int:tarea_id>/completa/',views.tareaCompleta,name='tareaCompleta'),
    path('tareas/detalle/<int:tarea_id>/eliminar/',views.tareaEliminada,name='eliminarTarea'),    
]
