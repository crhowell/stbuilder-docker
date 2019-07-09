from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views import generic
from django.shortcuts import (get_object_or_404, reverse,
                              HttpResponseRedirect, Http404)
from django.contrib.auth import get_user_model

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin
from dal import autocomplete
from notifications.signals import notify

from core.mixins import IsOwnerMixin
from . import forms
from . import models
from projects.models import Position

STATUS_CHOICES = {
    'new': None,
    'accepted': True,
    'rejected': False
}

User = get_user_model()


class ShowProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.TemplateView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    prefetch_related = [
        'my_projects', 'profile_skills',
        'user__projects__positions', 'user__projects']

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['skills'] = context['profile'].skills.all()
        context['p_projects'] = context['profile'].user.projects.all()
        context['u_projects'] = context['profile'].my_projects.all()
        return context

    def get(self, request, **kwargs):
        slug = self.kwargs.get('slug')
        if slug:
            profile = get_object_or_404(models.UserProfile, slug=slug)
        else:
            profile = self.request.user.profile

        kwargs['profile'] = profile
        return super().get(request, **kwargs)


class EditProfile(LoginRequiredMixin, IsOwnerMixin,
                  PrefetchRelatedMixin, generic.UpdateView):
    model = models.UserProfile
    form_class = forms.UserProfileForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    prefetch_related = ['my_projects', 'profile_skills']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['s_formset'] = forms.SkillInlineFormSet(
            queryset=models.Skill.objects.filter(
                profile_skills=context['profile']
            ),
            prefix='skill_formset'
        )
        context['p_formset'] = forms.UserProjectInlineFormSet(
            queryset=models.UserProject.objects.filter(
                profile=context['profile']
            ),
            prefix='project_formset'
        )
        return context

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            models.UserProfile,
            user=self.request.user
        )
        if obj.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = forms.UserProfileForm(
            self.request.POST, request.FILES, instance=profile)
        s_formset = forms.SkillInlineFormSet(
            self.request.POST,
            queryset=models.Skill.objects.filter(
                profile_skills=profile
            ),
            prefix='skill_formset'
        )
        p_formset = forms.UserProjectInlineFormSet(
            self.request.POST,
            queryset=models.UserProject.objects.filter(
                profile=profile
            ),
            prefix='project_formset'
        )

        if form.is_valid():
            profile = form.save(commit=False)
            if s_formset.is_valid() and p_formset.is_valid():
                skills = s_formset.save()
                projects = p_formset.save(commit=False)

                for skill in skills:
                    profile.skills.add(skill)
                profile.save()

                for project in projects:
                    project.profile = profile
                    project.save()

                return HttpResponseRedirect(reverse('profiles:my_profile'))

        return HttpResponseRedirect(reverse('profiles:my_profile',
                                            {'form': form, 's_formset': s_formset}))

    def get_success_url(self):
        return reverse_lazy('profiles:show_profile', kwargs={'slug': self.object.slug})


class UserApplications(LoginRequiredMixin,
                       PrefetchRelatedMixin, generic.ListView):
    model = models.UserApplication
    template_name = 'applications.html'
    context_object_name = 'application_list'
    prefetch_related = ['applicant__projects',
                        'applicant__projects__positions']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_term = self.request.GET.get('status') or 'all'
        proj_term = self.request.GET.get('proj') or 'all'
        need_term = self.request.GET.get('need') or 'all'

        if proj_term and proj_term != 'all':
            queryset = queryset.filter(
                project__title=proj_term
            )
        if need_term and need_term != 'all':
            queryset = queryset.filter(
                position__name=need_term
            )
        if status_term and status_term != 'all':
            if status_term in STATUS_CHOICES.keys():
                queryset = queryset.filter(
                    is_accepted=STATUS_CHOICES[status_term]
                )

        return queryset.filter(project__creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.request.user.projects.all()
        context['status'] = self.request.GET.get('status') or 'all'
        context['proj'] = self.request.GET.get('proj') or 'all'
        context['need'] = self.request.GET.get('need') or 'all'
        return context


class UserApplicationStatus(LoginRequiredMixin, generic.TemplateView):

    def get(self, request, *args, **kwargs):
        position_id = self.kwargs.get('position')
        position = Position.objects.filter(pk=position_id).first()
        if position.project.creator == self.request.user:
            applicant_pk = self.kwargs.get('applicant')
            applicant = get_object_or_404(User, pk=applicant_pk)
            status = self.kwargs.get('status')
            if status == 'approve' or status == 'deny':
                if position and applicant:
                    bstatus = True if status == 'approve' else False
                    application = models.UserApplication.objects.filter(
                        position=position, applicant=applicant
                    ).update(is_accepted=bstatus)

                    if status == 'approve':
                        msg_status = 'approved'
                    else:
                        msg_status = 'denied'

                    notify.send(
                        applicant,
                        recipient=applicant,
                        verb='Your application for {} as {} was {}'.format(
                            position.project.title, position.name, msg_status
                        ),
                        description=''
                    )
                    return HttpResponseRedirect(reverse('profiles:my_applications'))
        return HttpResponseRedirect(reverse('profiles:my_applications'))


class UserNotifications(LoginRequiredMixin, PrefetchRelatedMixin, generic.TemplateView):
    template_name = 'notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unreads'] = self.request.user.notifications.unread()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)