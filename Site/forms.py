from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from django.forms import formset_factory
from .models import Profile
from django import forms
# from django.forms.formsets import formset_factory


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class WallDimensionsForm(forms.Form):
    UNITS_CHOICES = (
        ('usStandard', 'US Standard units (Feet)'),
        ('metric', 'Metric Units (Meters)'),
    )

    unitChoice = forms.ChoiceField(
        choices=UNITS_CHOICES,
        initial=None,
        widget=forms.RadioSelect(attrs={'class': 'unit-selector', 'id': 'unit-choice'})
    )

    def __init__(self, *args, **kwargs):
        self.unitChoice = kwargs.pop('unitChoice', 'Inches')
        super().__init__(*args, **kwargs)

        self.fields['height'] = forms.FloatField(
            label=f'Wall Height',
            min_value=0,
            widget=forms.NumberInput(attrs={'step': '0.1'})  # Adjust the step based on the unit (0.01 for metric)
        )
        self.fields['width'] = forms.FloatField(
            label=f'Wall Width',
            min_value=0,
            widget=forms.NumberInput(attrs={'step': '0.1'})  # Adjust the step based on the unit (0.01 for metric)
        )

WallDimensionsFormSet = formset_factory(WallDimensionsForm, extra=1)