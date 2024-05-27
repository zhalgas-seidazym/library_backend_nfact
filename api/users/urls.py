from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('auth/', views.register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.logout, name='logout'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', views.send_verification_url, name='send_verification_url'),
    path('verify/email/', views.verify_email, name='verify_email'),
    path('profile/', views.UserViewSet.as_view({"get": "retrieve", "put": "update", "post": "destroy"}),
         name='profile'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('<str:email>/', views.GetUserProfileView.as_view({"get": "retrieve"}), name='get_user_profile'),
    path('<str:email>/books/', views.GetUserBooksView.as_view({"get": "list"}), name='user-books'),
]
