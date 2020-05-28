
from django.urls import path
from bugtrackerapp import views

urlpatterns = [
    path('home/', views.index, name='homepage'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('addticket/', views.add_ticket, name='addticket'),
    path('ticket/<int:id>/', views.ticket_detail, name='ticket'),
    path('user/<int:id>/', views.user_view, name='user'),
    path('edit/<int:id>', views.edit_ticket_view, name='edit')
]