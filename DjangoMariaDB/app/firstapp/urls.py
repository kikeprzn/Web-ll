from django.urls import path

from . import views

urlpatterns = [

    path('', views.home),
    path('products/', views.products, name = "products"),
    path('customer/', views.customer, name = "customer"),
    path('todo/', views.todoList, name = "todoList"),
    
    path('client/login',views.login,name='login'),
    path('client/movies',views.getMovies,name='getMovies'),
    path('generate_password/<str:password>',views.makePassword,name='makePassword')
    
]
