from django.urls import path

from .views import ListaPendientes, DetalleTareas, CrearTarea, ActualizarTarea, EliminarTarea, Logueo, Registro
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', Logueo.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', Registro.as_view(), name='register'),
    path('', ListaPendientes.as_view(), name='pendientes'),
    path('tarea/<int:pk>', DetalleTareas.as_view(), name='tarea'),
    path('crear-tarea', CrearTarea.as_view(), name='crear-tarea'),
    path('editar-tarea/<int:pk>', ActualizarTarea.as_view(), name='editar-tarea'),
    path('eliminar-tarea/<int:pk>', EliminarTarea.as_view(), name='eliminar-tarea'),
]
