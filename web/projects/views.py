from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse, Http404
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from notifications.signals import notify

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from core.mixins import IsOwnerMixin
from . import forms
from . import models
from profiles.models import UserApplication


class ProjectListView(PrefetchRelatedMixin, generic.ListView):
    model = models.Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    prefetch_related = ['positions', 'positions__skills']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_needs'] = models.Position.objects.filter(
            project__in=context['projects']
        ).exclude(applications__is_accepted=True)

        context['skill_needs'] = models.Skill.objects.filter(
            related_skills__in=context['project_needs']
        ).distinct()
        context['curr_filter'] = self.request.GET.get('filter')
        context['curr_term'] = self.request.GET.get('s')
        context['curr_skill'] = self.request.GET.get('skill')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('s')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        filter_term = self.request.GET.get('filter')
        if filter_term:
            queryset = queryset.filter(
                Q(positions__name=filter_term)
            )

        skill_term = self.request.GET.get('skill')
        if skill_term:
            queryset = queryset.filter(
                positions__skills__name=skill_term
            ).distinct()

        return queryset


class ProjectDetailView(LoginRequiredMixin, PrefetchRelatedMixin, generic.DetailView):
    model = models.Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    prefetch_related = ['creator__profile', 'positions', 'positions__applications']

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['profile'] = context['project'].creator.profile
        context['positions'] = models.Position.objects.filter(
            project=context['project']).exclude(applications__is_accepted=True)
        context['applied_for'] = models.Position.objects.filter(
            project=context['project'],
            applications__applicant=self.request.user)
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'project_create.html'
    success_url = reverse_lazy('projects:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['p_formset'] = forms.PositionInlineFormSet(
            queryset=models.Position.objects.none(),
            prefix='p_formset'
        )
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ProjectCreateForm(self.request.POST)
        p_formset = forms.PositionInlineFormSet(
            self.request.POST,
            queryset=models.Position.objects.none(),
            prefix='p_formset'
        )

        if form.is_valid():
            project = form.save(commit=False)
            project.creator = self.request.user
            project.save()
            if p_formset.is_valid():
                positions = p_formset.save(commit=False)
                for position in positions:
                    position.project = project
                    position.save()
                p_formset.save_m2m()
        return HttpResponseRedirect(reverse('projects:project_list'))


class ProjectEditView(LoginRequiredMixin, IsOwnerMixin, generic.UpdateView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'project_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['p_formset'] = forms.PositionInlineFormSet(
            queryset=models.Position.objects.filter(project=context['project']),
            prefix='p_formset'
        )
        return context


class ProjectDeleteView(LoginRequiredMixin, IsOwnerMixin, generic.DeleteView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    context_object_name = 'project'
    template_name = 'project_delete.html'
    success_url = reverse_lazy('projects:project_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.creator == self.request.user:
            raise Http404
        return obj


class PositionApplyView(LoginRequiredMixin, generic.TemplateView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        pos_pk = self.kwargs.get('position')
        project = get_object_or_404(models.Project, pk=pk)
        position = get_object_or_404(models.Position, pk=pos_pk)
        application = UserApplication.objects.filter(
            position=position,
            applicant=self.request.user
        )

        if application.exists():
            return HttpResponseRedirect(reverse(
                   'projects:project_detail', kwargs={'pk': pk}))

        UserApplication.objects.create(
            applicant=self.request.user,
            project=project,
            position=position
        )

        notify.send(
            self.request.user,
            recipient=self.request.user,
            verb='YOU submitted an application for {} as {}.'.format(
              project.title, position.name
            ),
            description=''
        )
        notify.send(
            project.creator,
            recipient=project.creator,
            verb='{} submitted an application for {} as {}'.format(
                self.request.user, project.title, position.name,
            ),
            description=''
        )
        return HttpResponseRedirect(reverse(
            'projects:project_list'))
