from django.urls import path

from tests.views import UserLogin, UserLogout, Register, TestsView, \
    TestUpdateView, CreateTestView, UserDetailView, MyTestsView, \
    QuestionCreateView, DeleteQuestionView

# handler for 404 error and 500 error
# handler404 = Custom404View.as_view()
# handler500 = Custom500View.as_view()

app_name = 'tests'
urlpatterns = [
    path('', TestsView.as_view(), name="tests"),
    path('mytests/', MyTestsView.as_view(), name="my_tests"),
    path('test_edit/<int:pk>/', TestUpdateView.as_view(), name="test_edit"),
    path('create_test/', CreateTestView.as_view(), name="create_test"),
    path('add_question/', QuestionCreateView.as_view(), name="add_question"),
    path('delete_question/<int:pk>/', DeleteQuestionView.as_view(), name='delete_question'),
    path('accounts/login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('accounts/register/', Register.as_view(), name="register"),
    path('profile/<int:pk>/', UserDetailView.as_view(), name="profile"),

]
