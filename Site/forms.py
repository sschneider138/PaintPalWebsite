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


class EasterEggForm(forms.Form):
    COMPUTATION_CHOICES = (
        ('recursion', 'Recursion Method (slow)'),
        ('dynamic', 'Dynamic Programming Method (fast)'),
    )

    computationChoice = forms.ChoiceField(
        choices=COMPUTATION_CHOICES,
        initial=None,
        label="Select Computation Method",
        widget=forms.RadioSelect(attrs={'class': 'computation-selector', 'id': 'computation-choice'})
    )
    
    def __init__(self, *args, **kwargs):
        self.computationChoice = kwargs.pop('Computation Choice', None)
        super().__init__(*args, **kwargs)

        self.fields['fibNumber'] = forms.IntegerField(
            label = f'Enter Fibonacci Number',
            min_value=0,
        )

class WallDimensionsForm(forms.Form):
    UNITS_CHOICES = (
        ('usStandard', 'US Standard units (Feet)'),
        ('metric', 'Metric Units (Meters)'),
    )

    unitChoice = forms.ChoiceField(
        choices=UNITS_CHOICES,
        initial=None,
        label="Select Unit Choice",
        widget=forms.RadioSelect(attrs={'class': 'unit-selector', 'id': 'unit-choice'})
    )

    def __init__(self, *args, **kwargs):
        self.unitChoice = kwargs.pop('unitChoice', None)
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

        # Additional fields for door and window dimensions
        self.fields['doorHeight'] = forms.FloatField(
            label=f'Door Height',
            min_value=0,
            widget=forms.NumberInput(attrs={'step': '0.1'})  # Adjust the step based on the unit (0.01 for metric)
        )
        self.fields['doorWidth'] = forms.FloatField(
            label=f'Door Width',
            min_value=0,
            widget=forms.NumberInput(attrs={'step': '0.1'})  # Adjust the step based on the unit (0.01 for metric)
        )
        self.fields['windowHeight'] = forms.FloatField(
            label=f'Window Height',
            min_value=0,
            widget=forms.NumberInput(attrs={'step': '0.1'})  # Adjust the step based on the unit (0.01 for metric)
        )
        self.fields['windowWidth'] = forms.FloatField(
            label=f'Window Width',
            min_value=0,
            widget=forms.NumberInput(attrs={'step': '0.1'})  # Adjust the step based on the unit (0.01 for metric)
        )


EasterEggFormSet = formset_factory(EasterEggForm, extra=1)
WallDimensionsFormSet = formset_factory(WallDimensionsForm, extra=1)