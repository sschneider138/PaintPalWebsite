from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, WallDimensionsForm, WallDimensionsFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calculations.PaintCalculations import *

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, "Site/home.html", {"title": "Home"})
   
    
class AboutView(View):
    def get(self, request):
        return render(request, "Site/about.html", {"title": "About"})


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'Site/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
        return render(request, 'Site/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = self.request.user.profile
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=profile if profile else None)
        context = {
            'userUpdateForm': userUpdateForm,
            'profileUpdateForm': profileUpdateForm
        }
        return render(request, 'Site/profile.html', context)

    def post(self, request):
        profile = self.request.user.profile
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profileUpdateForm = ProfileUpdateForm(request.POST, request.FILES, instance=profile if profile else None)
        if userUpdateForm.is_valid() and profileUpdateForm.is_valid():
            userUpdateForm.save()
            profileUpdateForm.save()
            messages.success(request, f'Your account information has been updated!')
            return redirect('profile')
        context = {
            'userUpdateForm': userUpdateForm,
            'profileUpdateForm': profileUpdateForm
        }
        return render(request, 'Site/profile.html', context)

class PaintCalculatorView(View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, f"You must have a registered account to access this feature.")
            return redirect('register')

        formset = WallDimensionsFormSet()
        return render(request, 'Site/paintCalculator.html', {'formset': formset})

    @method_decorator(login_required)
    def post(self, request):
        formset = WallDimensionsFormSet(request.POST)
        if formset.is_valid():
            selectedUnit = formset[0].cleaned_data['unitChoice']  # Get the selected unit from the first form in the formset
            print(f"Selected unit: {selectedUnit}")
            totalPaintVolume = 0
            for form in formset:
                height = form.cleaned_data['height']
                width = form.cleaned_data['width']

                # sum over all walls by grabbing number from returned array. the first element [0] is the volume mangitude
                totalPaintVolume += PaintCalculations(height, width, selectedUnit).calculatePaintRequired()[0]

                # grab the units associated with the calculation. this is stored as the second element [1] in the returned array
                units = PaintCalculations(height, width, selectedUnit).calculatePaintRequired()[1]

            # pass magnitude arr[0] and units arr[1] in as context for following page
            return render(request, 'Site/result.html', {'paintVolume': totalPaintVolume, 'units' : units})

        return render(request, 'Site/paintCalculator.html', {'formset': formset})
