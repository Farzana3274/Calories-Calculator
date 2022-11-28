from django.urls import path
from.import views

urlpatterns = [
    path('', views.loginUser, name='loginUser'),
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.register, name='register'),
    path('calculator/', views.calculator, name='calculator'), 
    path('home/', views.home, name='home'),
    path('update/', views.EditBMR, name='EditBMR'),
    path('search/', views.SearchByDate, name='search'),
    path('graph/', views.graph, name='graph'),
    path('logout/', views.logoutUser, name='logoutUser'),
    
]
