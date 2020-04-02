from django.urls import path

from . import views

urlpatterns = [
    path('client/login',views.login,name='login'),
    path('client/movies',views.getMovies,name='getMovies'),
    path('generate_password/<str:password>',views.makePassword,name='makePassword')
]
