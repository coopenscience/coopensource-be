
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserView, LogoutView, CompleteUserView, UserExistsView, ProjectView, populatedb, RecommendProjectsView


router = DefaultRouter()
router.register(r'projects', ProjectView)
urlpatterns = [
    path('populatedb', populatedb.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user/<int:id>/exists', UserExistsView.as_view()),
    path('complete_user', CompleteUserView.as_view()),
    path('', include(router.urls)),
    path('recommended_projects/<int:id>/', RecommendProjectsView.as_view(), name='recommend_projects'),
]
