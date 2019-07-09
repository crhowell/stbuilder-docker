from django import forms


class FormSetMedia(forms.ModelForm):
    class Media:
        js = (
            'js/jquery.formset.js',
        )
