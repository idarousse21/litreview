from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import View
from . import forms


class LoginPageView(View):
    form_class = forms.LoginForm
    template_name = "authentication/login.html"

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )

    def post(self, request):
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("flux")
            else:
                message = "Identifiants invalides."
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )


def logout_user(request):
    logout(request)
    return redirect("login")


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_URL)
    return render(request, "authentication/signup.html", context={"form": form})