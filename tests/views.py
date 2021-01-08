from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from django_tests_mini_platform.settings import DEFAULT_TESTS_ORDERING, \
    TESTS_ORDERINGS
from tests.forms import SignUpForm, CreateTestForm, CreateQuestionForm
from tests.models import Test, TestsUser, Question


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

    queryset = Test.objects.filter(draft=False)

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', DEFAULT_TESTS_ORDERING)
        # validate ordering
        if ordering not in TESTS_ORDERINGS:
            ordering = DEFAULT_TESTS_ORDERING
        return ordering

    # Add  to context
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     return context


@method_decorator(login_required, name='dispatch')
class MyTestsView(TestsView):
    """
    List of active user tests
    """
    def get_queryset(self):
        return Test.objects.filter(author=self.request.user)


@method_decorator(login_required, name='dispatch')
class TestUpdateView(UpdateView):
    """
    Update session. Only for administrators.
    """
    model = Test
    template_name = 'test_edit.html'
    success_url = reverse_lazy('tests:my_tests')
    fields = ['title', 'description', 'created_at', 'draft']

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        test = self.object
        test.author = self.request.user
        question_count = Question.objects.filter(test=test).count()
        if question_count < 4 and not test.draft:
            messages.error(self.request, "this test doesnt have 4 questions")
            return HttpResponseRedirect(
                self.request.META.get('HTTP_REFERER'))

        return super().form_valid(form)

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'add_question_form': CreateQuestionForm})
        return context


@method_decorator(login_required, name='dispatch')
class CreateTestView(CreateView):
    """
        Create test
    """
    form_class = CreateTestForm
    template_name = 'test_edit.html'

    def get_success_url(self):
        obj_id = self.object.id
        return reverse('tests:test_edit', kwargs={'pk': obj_id})

    def form_valid(self, form):
        test = form.save(commit=False)
        test.author = self.request.user
        form.instance.author = self.request.user
        form.save()
        return super(CreateTestView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class QuestionCreateView(CreateView):
    form_class = CreateQuestionForm
    model = Question

    def form_valid(self, form):
        question = form.save(commit=False)
        test_id = self.request.POST.get('test_id')
        test = Test.objects.get(id=test_id)
        question.test = test
        question.save()
        return super().form_valid(form=form)

    def get_success_url(self):
        test_id = self.request.POST.get('test_id')
        return reverse('tests:test_edit', kwargs={'pk': test_id})

