
from django.urls import path
from bugtrackerapp import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('addticket/', views.add_ticket, name='addticket'),
    path('ticket/<int:id>/', views.ticket_detail, name='ticket'),
    path('in_progress/<int:id>/', views.mark_in_progress, name='in_progress'),
    path('completed/<int:id>/', views.mark_completed, name='completed'),
    path('invalid/<int:id>/', views.mark_invalid, name='invalid'),
    path('user/<int:id>/', views.user_view, name='user'),
    path('edit/<int:id>', views.edit_ticket_view, name='edit')
]