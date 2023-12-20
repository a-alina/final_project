from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include

urlpatterns = [
    path("", views.main, name="main"),
    path("choose_file", views.choose_file, name="choose_file"),
    path("quiz/<str:param1>/<int:param2>/", views.quiz, name="quiz"),
    path("test/<str:param1>/<int:param2>/", views.test, name="test"),
    path("list_of_quizes", views.list_of_quizes, name="list_of_quizes"),
    path("files", views.files, name="files"),
    path("sign_up", views.sign_up, name="sign_up"),
    path('' , include('django.contrib.auth.urls') , name = 'login'),
    

   

]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
