from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('post/<slug:blog_slug>/', views.detail, name='detail'),  
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('loginthougtify/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('myposts/', views.mypost, name='mypost'),
    path('createposts/', views.createpost, name='create'),
    path('editposts/<int:edit_id>/', views.edit, name='edit'),
    path('delete/<int:task_id>/', views.deletepost, name='delete_task'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("aboutus/", views.aboutus, name="about"),
    path("contactus/", views.contactus,name="contact"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
