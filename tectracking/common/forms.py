from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class UserCreationForm(DefaultUserCreationForm):
    first_name = forms.RegexField(label=_('First name'), max_length=30, regex=r'^\w+$',
                                  help_text=_('Required. 30 characters or fewer. Only letters.'),
                                  error_messages={'invalid': _('First name may only contain letters.')})
    last_name = forms.RegexField(label=_('First name'), max_length=30, regex=r'^\w+$', required=False,
                                  help_text=_('Required. 30 characters or fewer. Only letters.'),
                                  error_messages={'invalid': _('Last name may only contain letters.')})
    email = forms.EmailField(label=_('Email'),
                             help_text=_('Required. Must be a valid e-mail address.'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
