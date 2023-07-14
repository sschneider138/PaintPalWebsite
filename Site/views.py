from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, WallDimensionsForm, WallDimensionsFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

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
    # @method_decorator(login_required)
    def get(self, request):
        formset = WallDimensionsFormSet()
        return render(request, 'Site/paintCalculator.html', {'formset': formset})

    # @method_decorator(login_required)
    def post(self, request):
        formset = WallDimensionsFormSet(request.POST)
        if formset.is_valid():
            totalPaintVolume = 0
            for form in formset:
                height = form.cleaned_data['height']
                width = form.cleaned_data['width']

                surfaceArea = width * height
                .0
                # internet searching estimates layer is 0.05mm when dry. Double this for estimated wet thickness 
                # source - https://www.quora.com/If-someone-painted-a-coat-of-paint-on-the-walls-of-their-house-a-hundred-times-would-the-walls-become-thicker
                
                # find volume in m^3
                paintVolume = (surfaceArea * 0.0001)
                
                # find volume in liters
                paintVolume = paintVolume * 1000

                # sum over all walls
                totalPaintVolume += paintVolume

            return render(request, 'Site/result.html', {'paintVolume': totalPaintVolume})

        return render(request, 'Site/paintCalculator.html', {'formset': formset})
