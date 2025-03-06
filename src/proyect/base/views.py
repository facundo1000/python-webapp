from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .models import Tareas


class Logueo(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pendientes')

class Registro(FormView):
    template_name = 'base/RegisterForm.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request,usuario)
        return super(Registro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('pendientes')
        return super(Registro, self).get(*args, **kwargs)


class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tareas
    context_object_name = 'tareas'
    template_name = 'base/tareaList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completa=False).count()

        # Filtro de busqueda de tareas
        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
            context['valor_buscado'] = valor_buscado
        return context

class DetalleTareas(LoginRequiredMixin, DetailView):
    model = Tareas
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tareas
    template_name = 'base/formTarea.html'
    fields = ['titulo', 'descripcion', 'completa']
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)


class ActualizarTarea(LoginRequiredMixin, UpdateView):
    model = Tareas
    template_name = 'base/formTarea.html'
    fields = ['titulo', 'descripcion', 'completa']
    success_url = reverse_lazy('pendientes')


class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tareas
    context_object_name = 'tarea'
    template_name = 'base/DeleteTareaView.html'
    success_url = reverse_lazy('pendientes')
