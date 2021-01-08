from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from django_tests_mini_platform.settings import DEFAULT_TESTS_ORDERING, \
    TESTS_ORDERINGS
from tests.forms import SignUpForm, CreateTestForm
from tests.models import Test, TestsUser


class UserLogin(LoginView):
    """ login """
    template_name = 'login.html'
    next_page = reverse_lazy('tests:tests')
    success_url = reverse_lazy('tests:tests')


class Register(CreateView):
    """ Sign UP """
    form_class = SignUpForm
    success_url = reverse_lazy('tests:login')
    template_name = "register.html"


@method_decorator(login_required, name='dispatch')
class UserLogout(LogoutView):
    """ Logout """
    next_page = reverse_lazy('tests:tests')
    success_url = reverse_lazy('tests:tests')
    redirect_field_name = 'next'


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = TestsUser
    template_name = 'user_profile.html'


@method_decorator(login_required, name='dispatch')
class TestsView(ListView):
    """
    List of tests
    """
    model = Test
    paginate_by = 10
    template_name = 'tests.html'

    queryset = Test.objects.all() \
        .annotate(num_q=Count('test_questions')) \
        .filter(num_q__gte=4)

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


@method_decorator(login_required, name='dispatch')
class MyTestsView(TestsView):
    """
    List of active user tests
    """
    def get_queryset(self):
        return Test.objects.filter(author=self.request.user)


@method_decorator(login_required, name='dispatch')
class CreateTestView(CreateView):
    """
        Create test
    """
    form_class = CreateTestForm
    template_name = 'test_create.html'

    def get_success_url(self):
        obj = self.kwargs['obj']
        obj.save()
        return reverse('tests:edit_test', kwargs={'pk': obj})


@method_decorator(login_required, name='dispatch')
class TestUpdateView(UpdateView):
    form_class = CreateTestForm
    template_name = 'test_edit.html'

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context

# class Custom500View(View):
#     def dispatch(self, request, *args, **kwargs):
#         return render(request, '500.html', {}, status=500)
#
#
# class Custom404View(View):
#     def dispatch(self, request, *args, **kwargs):
#         return render(request, '404.html', {}, status=404)
