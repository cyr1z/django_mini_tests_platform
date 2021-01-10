from django.urls import path

from tests.views import UserLogin, UserLogout, Register, TestsView, \
    TestUpdateView, CreateTestView, UserDetailView, MyTestsView, \
    QuestionCreateView, DeleteQuestionView, TestDetailView, CommentCreateView, \
    TestPassView, TestCheckView

app_name = 'tests'
urlpatterns = [
    path('accounts/login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('accounts/register/', Register.as_view(), name="register"),
    path('profile/<int:pk>/', UserDetailView.as_view(), name="profile"),
    path('comment/', CommentCreateView.as_view(), name="comment"),
    path('', TestsView.as_view(), name="tests"),
    path('mytests/', MyTestsView.as_view(), name="my_tests"),
    path('test_edit/<int:pk>/', TestUpdateView.as_view(), name="test_edit"),
    path('create_test/', CreateTestView.as_view(), name="create_test"),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('test_pass/<int:pk>/', TestPassView.as_view(), name='test_pass'),
    path('test_check/', TestCheckView.as_view(), name="test_check"),
    path('add_question/', QuestionCreateView.as_view(), name="add_question"),
    path('delete_question/<int:pk>/', DeleteQuestionView.as_view(),
         name='delete_question'),

]
