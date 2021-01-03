from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from django_tests_mini_platform.settings import DEFAULT_TESTS_ORDERING, \
    TESTS_ORDERINGS
from tests.forms import SignUpForm
from tests.models import Test


class UserLogin(LoginView):
    """ login """
    template_name = 'login.html'
    success_url = "/"


class Register(CreateView):
    """ Sign UP """
    form_class = SignUpForm
    success_url = "/login/"
    template_name = "register.html"


@method_decorator(login_required, name='dispatch')
class UserLogout(LogoutView):
    """ Logout """
    next_page = "/"
    success_url = "/"
    redirect_field_name = 'next'


@method_decorator(login_required, name='dispatch')
class TestsView(ListView):
    """
    List of sessions
    """
    model = Test
    paginate_by = 10
    template_name = 'tests.html'

    queryset = Test.objects.all()

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', DEFAULT_TESTS_ORDERING)
        # validate ordering
        if ordering not in TESTS_ORDERINGS:
            ordering = DEFAULT_TESTS_ORDERING
        return ordering

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context
