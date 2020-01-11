# from datetime import datetime
from random import shuffle
from .models import Recipe, Plan, RecipePlan, WeekDays

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict
from django.contrib.auth.models import User
from django.views.generic import CreateView, FormView, ListView
from django.template.response import TemplateResponse
from .forms import LoginForm, UserRegisterForm, ResetPasswordForm

WEEKDAYS = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


class IndexView(View):
    def get(self, request):
        ctx = {}
        # Karuzela na index.html
        recipes = list(Recipe.objects.all())
        shuffle(recipes)
        recipe1 = recipes[0]
        recipe2 = recipes[1]
        recipe3 = recipes[2]
        ctx["recipe1"] = recipe1
        ctx["recipe2"] = recipe2
        ctx["recipe3"] = recipe3

        return render(request, "index.html", ctx)


class DaschboardView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {}
        plans_nr = Plan.objects.all().count()
        ctx["plans_nr"] = plans_nr
        recipes_nr = Recipe.objects.all().count()
        ctx["recipes_nr"] = recipes_nr

        # Ostatni dodany plan i związane z nim dane
        latest_plan = Plan.objects.all().order_by("created").last()
        through = RecipePlan.objects.filter(plan_id=latest_plan.id)

        # sortowanie through według dnia i kolejności posiłków
        ordered_t = through.order_by("order")

        week_dict = {}
        for k in ordered_t:
            if k.day_name in week_dict.keys():
                week_dict[k.day_name] += ((k.meal_name, k.recipe.name, k.recipe.id),)
            else:
                week_dict[k.day_name] = ((k.meal_name, k.recipe.name, k.recipe.id),)

        o_dict = OrderedDict(sorted(week_dict.items(), key=lambda t: t[0]))

        if latest_plan:
            ctx["latest_plan"] = latest_plan
        else:
            ctx["latest_plan"] = "Brak planów w bazie"
        ctx["days"] = o_dict
        ctx["week"] = WEEKDAYS

        return render(request, "dashboard.html", ctx)


class add_recipe(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request, template="app-add-recipe.html", ctx=None):
        # zmieniam tu trochę: dodaję paramentry domyślne po to, aby aby móc wykorzystać tę funkcję
        # w widoku receipe_modify_id, bez przeklejania kodu
        name = request.POST.get("name", False)
        description = request.POST.get("description", False)
        preparation_time = request.POST.get("preparation_time", False)
        instructions = request.POST.get("instructions", False)
        ingredients = request.POST.get("ingredients", False)

        if name and description and preparation_time and instructions and ingredients:
            new_recipe = Recipe()
            new_recipe.name = name
            new_recipe.ingredients = ingredients
            new_recipe.description = description
            new_recipe.instructions = instructions
            new_recipe.preparation_time = int(preparation_time)
            new_recipe.save()
            return redirect("/recipe/list")
        else:
            if not ctx:
                ctx = {}
            message = "Fill all required fields"
            ctx["message"] = message
            return render(request, template, ctx)


class RecipeListView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {}
        recipes = Recipe.objects.all().order_by("-votes", "-created")

        # trochę tu odbiłem od opisu zadania żeby sensownie wyglądało i było weryfikowalne
        if recipes.count() < 51:
            recipes_per_page = 10
        else:
            recipes_per_page = 50

        paginator = Paginator(recipes, recipes_per_page)
        page = request.GET.get("page")
        recipes_paginated = paginator.get_page(page)
        ctx["recipes"] = recipes_paginated
        ctx["paginator"] = paginator
        return render(request, "app-recipes.html", ctx)


class PlanListView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {}
        plans = Plan.objects.all().order_by("name")
        page = request.GET.get("page", 1)

        paginator = Paginator(plans, 4)
        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)

        return render(request, "app-schedules.html", {"plans": plans})


class add_planView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {}

        return render(request, "app-add-schedules.html", ctx)

    def post(self, request):

        name = request.POST.get("name")
        description = request.POST.get("description")

        # walidacja i reakcja na puste pola
        error_messages = []
        if not name:
            error_messages.append("Fill the name fiels.")
        if not description:
            error_messages.append("Fill the description field.")
        if error_messages:
            ctx = {}
            ctx["error_messages"] = error_messages
            return render(request, "app-add-schedules.html", ctx)
        # koniec walidacji

        new_plan_id = Plan.objects.create(name=name, description=description).id

        return redirect(f"/plan/{new_plan_id}/details/")


class plan_add_recipeView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {}
        all_recipes = Recipe.objects.all()
        all_plans = Plan.objects.all()
        weekdays_tuple = [(tag.name, tag.value) for tag in WeekDays]
        ctx["WeekDays"] = weekdays_tuple
        ctx["all_recipes"] = all_recipes
        ctx["all_plans"] = all_plans
        return render(request, "app-schedules-meal-recipe.html", ctx)

    def post(self, request):
        meal_name = request.POST.get("meal_name")
        chosen_recipe = request.POST.get("chosen_recipe")
        chosen_plan = request.POST.get("chosen_plan")
        chosen_day = request.POST.get("chosen_day")
        meal_nr = request.POST.get("meal_nr")

        if meal_name and chosen_recipe and chosen_plan and chosen_day and meal_nr:
            recipe_to_add = Recipe.objects.filter(name=chosen_recipe)
            plan_to_add = Plan.objects.filter(name=chosen_plan)
            new_item = RecipePlan()
            new_item.meal_name = meal_name
            new_item.recipe = recipe_to_add[0]
            new_item.plan = plan_to_add[0]
            new_item.day_name = chosen_day
            new_item.order = meal_nr
            new_item.save()
            return redirect(f"/plan/{plan_to_add[0].pk}")
        else:
            ctx = {}
            message = "Fill all required fields!"
            ctx["message"] = message
            all_recipes = Recipe.objects.all()
            all_plans = Plan.objects.all()
            weekdays_tuple = [(tag.name, tag.value) for tag in WeekDays]
            ctx["WeekDays"] = weekdays_tuple
            ctx["all_recipes"] = all_recipes
            ctx["all_plans"] = all_plans
            return render(request, "app-schedules-meal-recipe.html", ctx)


def recipe_id(request, id):

    if request.method == "GET":
        ctx = {}
        ctx["recipe"] = Recipe.objects.get(pk=id)
        return render(request, "app-recipe-details.html", ctx)
    elif request.method == "POST":
        recipe = Recipe.objects.get(pk=int(request.POST.get("recipe_id")))

        votes = recipe.votes
        if request.POST.get("like"):
            votes += 1
        elif request.POST.get("dislike"):
            votes += -1
        recipe.votes = votes
        recipe.save()
        ctx = {}
        ctx["recipe"] = Recipe.objects.get(pk=id)
        return render(request, "app-recipe-details.html", ctx)


def plan_id(request, id):

    ctx = {}
    wybrany_plan = Plan.objects.get(pk=id)
    ctx["plan"] = wybrany_plan
    RP_wybrane = RecipePlan.objects.filter(plan_id=wybrany_plan.id)

    ordered_p = RP_wybrane.order_by("order")

    week_dict = {}
    for k in ordered_p:
        if k.day_name in week_dict.keys():
            week_dict[k.day_name] += ((k.meal_name, k.recipe.name, k.recipe.id),)
        else:
            week_dict[k.day_name] = ((k.meal_name, k.recipe.name, k.recipe.id),)

    o_dict = OrderedDict(sorted(week_dict.items(), key=lambda t: t[0]))

    ctx["days"] = o_dict
    ctx["week"] = WEEKDAYS

    return render(request, "app-details-schedules.html", ctx)


class remove_plan(LoginRequiredMixin, View):
    def get(self, request, id):
        ctx = {}
        wybrany_plan = Plan.objects.get(pk=id)
        ctx["plan"] = wybrany_plan
        return render(request, "remover.html", ctx)

    def post(self, request, id):
        usuwany = Plan.objects.get(pk=id)
        usuwany.delete()
        return redirect("plan_list")


class recipe_modify_id(LoginRequiredMixin, View):
    def get(self, request, id):

        try:
            recipe = Recipe.objects.get(pk=id)
        except Recipe.DoesNotExist:
            return render(request, "app-error-recipe.html")
        else:
            ctx = {}
            ctx["recipe"] = recipe
            return render(request, "app-edit-recipe.html", ctx)

    def post(self, request, id):
        ctx = {}
        ctx["recipe"] = Recipe.objects.get(pk=id)
        return add_recipe.post(self, request, "app-edit-recipe.html", ctx)


class LoginView(FormView):
    form_class = LoginForm
    success_url = "/main"
    template_name = "login.html"

    def form_valid(self, form: LoginForm):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)

        if user is None:
            form.add_error(None, "Invalid username or password")
            return super().form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        ctx = {"form": form}
        return render(request, "register.html", ctx)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            if password == confirm_password:
                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                messages.success(request, "Success! Now you can sign in!")
                return redirect("/main")
            else:
                form.add_error("confirm_password", "Passwords not the same")

        return render(request, "register.html", ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Signed out successfully")
        return redirect("/main")


class ResetPasswordView(LoginRequiredMixin, View):

    def get(self, request):
        form = ResetPasswordForm()
        ctx = {"form": form}
        return render(request, "reset.html", ctx)

    def post(self, request):
        user = get_object_or_404(User, id=request.session['_auth_user_id'])
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, "Password changed")
                return redirect("/main")
            else:
                form.add_error(None, "Passwords are not the same")

        ctx = {"form": form}
        return render(request, "reset.html", ctx)


class UserPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user.html")
