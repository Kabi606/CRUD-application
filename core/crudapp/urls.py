from django.urls import path
from django.contrib.auth import views as auth_views
from crudapp import views


urlpatterns = [  
    #DRF Url
    path('', views.home),
    path('userinfo/', views.UserInfo),
    path('userinfo/<int:pk>', views.PerInfo),
    path('usercreate/', views.UserCreate),

    #Function based view
    path('infocreate/', views.infocreate),
    path('infocreate/<int:pk>', views.infocreate),

    #Class based view
    path('courseinfo/', views.courseinfo.as_view()),
    path('courseinfo/<int:pk>', views.courseinfo.as_view()),

    #Mixin view
    path('ailist/',views.ailist.as_view()),
    path('ailist/<int:pk>', views.aiid.as_view()),
    path('ailistcreate/', views.ailistcreate.as_view()),
    path('ailistupdate/<int:pk>', views.ailistupdate.as_view()),
    path('ailistdelete/<int:pk>', views.ailistdelete.as_view()),

    #Alternative Mixin view
    path('coursecreate/', views.coursecreate.as_view()),
    path('courseid/<int:pk>', views.courseid.as_view()),

    #LIstcreateAPiview, RetriveUpdateDestroyApiview
    path('info/', views.info.as_view()),
    path('info/<int:pk>/', views.infoid.as_view()),

]
