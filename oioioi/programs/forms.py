from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from oioioi.programs.models import ContestCompiler


class ContestCompilerInlineForm(forms.ModelForm):
    COMPILER_CHOICES = [
        ('', 'Choose language first'),
    ]

    def __init__(self, *args, **kwargs):
        super(ContestCompilerInlineForm, self).__init__(*args, **kwargs)
        self.LANGUAGE_CHOICES = [
            ('', 'Choose language'),
        ]
        for language in getattr(settings, "SUBMITTABLE_EXTENSIONS", {}):
            self.LANGUAGE_CHOICES.append((language, language))

        FINAL_COMPILER_CHOICES = self.COMPILER_CHOICES
        if kwargs.get('instance'):
            instance = kwargs.get('instance')
            available_compilers = getattr(settings, 'AVAILABLE_COMPILERS', {})
            compilers_for_lang = available_compilers.get(instance.language)
            # we can't just add all the compilers_for_lang, because first one
            # is the default option, so it has to be current compiler
            FINAL_COMPILER_CHOICES = [(instance.compiler, instance.compiler)]
            for compiler in compilers_for_lang:
                if compiler != instance.compiler:
                    FINAL_COMPILER_CHOICES.append((compiler, compiler))
        self.fields['compiler'].widget=forms.Select(
                choices=FINAL_COMPILER_CHOICES)
        self.fields['language'] = forms.ChoiceField(
                choices=self.LANGUAGE_CHOICES)
        self.fields['language'].widget.attrs.update(
                {'data-compilerchoicesurl' : reverse('get_compiler_hints')})

    class Media(object):
        js = ('common/choose_compiler.js',)
