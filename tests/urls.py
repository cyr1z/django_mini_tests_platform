from django.urls import path

from tests.views import UserLogin, UserLogout, Register, TestsView

app_name = 'tests'
urlpatterns = [
    path('', TestsView.as_view(), name="tests"),
    path('accounts/login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('accounts/register/', Register.as_view(), name="register"),

]
