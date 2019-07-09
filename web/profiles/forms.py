from django import forms

from core.forms import FormSetMedia
from . import models


class SkillForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Skill',
            'class': ''
        })
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        skill, created = models.Skill.objects.get_or_create(
            name=instance.name)
        return skill

    class Meta:
        model = models.Skill
        fields = ('name',)


class UserProjectForm(FormSetMedia):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Project Name',
            'class': ''
        })
    )
    url = forms.CharField(
        widget=forms.URLInput(attrs={
            'placeholder': 'Project URL',
            'class': ''
        })
    )

    class Meta:
        model = models.UserProject
        fields = ('name', 'url')


class UserProfileForm(FormSetMedia):
    first_name = forms.CharField(
     widget=forms.TextInput(attrs={
         'placeholder': 'First name',
         'class': ''
     })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': ''
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about yourself...',
            'class': ''
        })

    )
    avatar = forms.ImageField(
        label='Avatar',
        required=False,
        widget=forms.FileInput(attrs={
            'class': ''
        })
    )

    class Meta:
        model = models.UserProfile
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'skills']


SkillInlineFormSet = forms.modelformset_factory(
    models.Skill,
    form=SkillForm,
    fields=('name',),
    extra=1,
    min_num=0,
    max_num=10
)


UserProjectInlineFormSet = forms.modelformset_factory(
    models.UserProject,
    form=UserProjectForm,
    extra=1,
    min_num=0,
    max_num=10
)
