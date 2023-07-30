from decimal import ROUND_HALF_UP
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, WallDimensionsFormSet, EasterEggFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calculations.PaintCalculations import *
from calculations.EasterEgg import *

class HomeView(View):
    def get(self, request):
        return render(request, "Site/home.html", {"title": "Home"})
       
class UsageView(View):
    def get(self, request):
        return render(request, "Site/usage.html", {"title": "Usage"})

class EasterEgg(View):
    def get(self, request):
        # Pass 'computationChoice' argument to forms in the formset during formset initialization
        formset = EasterEggFormSet()
        return render(request, "Site/easterEgg.html", {'formset': formset})

    def post(self, request):
        formset = EasterEggFormSet(request.POST)
        if formset.is_valid():
            selectedCalculationMethod = formset[0].cleaned_data['computationChoice']
            print(f'selected computation method = {selectedCalculationMethod}')

            for form in formset:
                fibNum = form.cleaned_data['fibNumber']

                if selectedCalculationMethod == 'recursion':
                    ans, method = FibonacciCalculator(fibNum).recursiveFuncStart()
                else:
                    ans, method = FibonacciCalculator(fibNum).dynamicFib()

                return render(request, 'Site/easterEggResult.html', {'easterEggAns': ans, 'easterEggMethod': method})

        return render(request, 'Site/easterEgg.html', {'formset': formset})


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
        profile = request.user.profile
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=profile if profile else None)
        context = {
            'userUpdateForm': userUpdateForm,
            'profileUpdateForm': profileUpdateForm
        }
        return render(request, 'Site/profile.html', context)

    def post(self, request):
        profile = request.user.profile
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profileUpdateForm = ProfileUpdateForm(request.POST, request.FILES, instance=profile if profile else None)
        if userUpdateForm.is_valid() and profileUpdateForm.is_valid():
            userUpdateForm.save()
            profile = profileUpdateForm.save()

            # Get the dimensions entered by the user
            height = profileUpdateForm.cleaned_data['height']
            width = profileUpdateForm.cleaned_data['width']
            unit = profileUpdateForm.cleaned_data['unit']

            # Calculate paint required and update the profile
            paint_calculator = PaintCalculations(height, width, unit)
            paint_volume, units = paint_calculator.calculatePaintRequired(profile)
            profile.save()

            messages.success(request, f'Your account information has been updated!')
            return redirect('profile')

        context = {
            'userUpdateForm': userUpdateForm,
            'profileUpdateForm': profileUpdateForm
        }
        return render(request, 'Site/profile.html', context)
    
    def post(self, request):
        # check if the reset button was pressed
        if 'resetPaintUsed' in request.POST:
            # get the user's profile associated with the current user
            profile = request.user.profile
            # reset the paint usage fields
            profile.resetPaintUsed()
            messages.success(request, f'Paint usage has been reset for your next project.')
            return redirect('profile')
        elif 'undoResetPaintUsed' in request.POST:
            profile = request.user.profile
            profile.undoResetPaintUsed()
            messages.success(request, f'Paint usage reset has been undone.')
            return redirect('profile')



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
            selectedUnit = formset.cleaned_data[0].get('unitChoice')
            totalPaintVolume = 0
            
            for form in formset:
                wallHeight = form.cleaned_data['height']
                wallWidth = form.cleaned_data['width']
                windowHeight = form.cleaned_data['windowHeight']
                windowWidth = form.cleaned_data['windowWidth']
                doorHeight = form.cleaned_data['doorHeight']
                doorWidth = form.cleaned_data['doorWidth']
                profile = request.user.profile
                if windowHeight > wallHeight or windowWidth > wallWidth:
                    messages.warning(request, f"Window dimensions cannot be larger than wall dimensions.")
                    return redirect('paintCalculator')
                elif doorHeight > wallHeight or doorWidth > wallWidth:
                    messages.warning(request, f"Door dimensions cannot be larger than wall dimensions.")
                    return redirect('paintCalculator')

                # find paint required for the wall
                paintCalculator = PaintCalculations(wallHeight, wallWidth, selectedUnit, profile, windowHeight, windowWidth, doorHeight, doorWidth)
                paintVolume, units = paintCalculator.calculatePaintRequired()

                # deduct areas of unpainted windows and doors
                if windowHeight >= 0 and windowWidth >= 0:
                    windowArea = paintCalculator.calculateWindowArea(windowHeight, windowWidth)
                    paintVolume -= windowArea

                if doorHeight >= 0 and doorWidth >= 0:
                    doorArea = paintCalculator.calculateDoorArea(doorHeight, doorWidth)
                    paintVolume -= doorArea

                totalPaintVolume += paintVolume
                if totalPaintVolume < 0:
                    messages.warning(request, f"Your dimensions have returned a negative value. This is likely due to a window or door being larger than the wall. Please retry your calculation.")
                    return redirect('paintCalculator')
                

            # round the paint volume to two decimal places
            totalPaintVolume = totalPaintVolume.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # update the user's profile with the calculated paint used
            if selectedUnit == 'metric':
                request.user.profile.paintUsedLiters += totalPaintVolume
            else:
                request.user.profile.paintUsedGallons += totalPaintVolume
            request.user.profile.save()

            # pass magnitude and units as context for the following page
            return render(request, 'Site/result.html', {'paintVolume': totalPaintVolume, 'units': units})

        return render(request, 'Site/paintCalculator.html', {'formset': formset})