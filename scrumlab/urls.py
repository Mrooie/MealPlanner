from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from jedzonko.views import (
    IndexView,
    DaschboardView,
    add_recipe,
    RecipeListView,
    add_planView,
    PlanListView,
    plan_add_recipeView,
    recipe_id,
    plan_id,
    recipe_modify_id,
    LoginView,
    UserRegisterView,
    LogoutView,
    UserPage,
    ResetPasswordView,
    remove_plan,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", DaschboardView.as_view(), name="Dashboard"),
    path("", IndexView.as_view()),
    path("recipe/list/", RecipeListView.as_view(), name="recipe_list"),
    path("recipe/add/", add_recipe.as_view(), name="recipe_add"),
    path("plan/list", PlanListView.as_view(), name="plan_list"),
    path("plan/add/", add_planView.as_view(), name="plan_add"),
    path("plan/add-recipe/", plan_add_recipeView.as_view(), name="plan_add_recipe"),
    url(r"^recipe/(?P<id>\d+)", recipe_id, name="recipe_id"),
    url(r"^plan/(?P<id>\d+)", plan_id, name="plan_id"),
    url(
        r"^recipe/modify/(?P<id>\d+)",
        recipe_modify_id.as_view(),
        name="recipe_modify_id",
    ),
    url(r"^login", LoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("reset/", ResetPasswordView.as_view(), name="reset"),
    url(r"^logout", LogoutView.as_view(), name="logout"),
    url(r"^user", UserPage.as_view(), name="datapage"),
    url(r"^remove/(?P<id>\d+)", remove_plan.as_view(), name="remove"),
]
