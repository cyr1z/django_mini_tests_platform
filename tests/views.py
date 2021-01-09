from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView,\
    DetailView, DeleteView

from django_tests_mini_platform.settings import DEFAULT_TESTS_ORDERING, \
    TESTS_ORDERINGS, MINIMUM_QUESTIONS, HOME_URL_LITERAL, TEST_EDIT_LITERAL
from tests.forms import SignUpForm, CreateTestForm, CreateQuestionForm, \
    CreateCommentForm
from tests.models import Test, TestsUser, Question, Comment


class UserLogin(LoginView):
    """ login """
    template_name = 'login.html'
    next_page = reverse_lazy(HOME_URL_LITERAL)
    success_url = reverse_lazy(HOME_URL_LITERAL)


class Register(CreateView):
    """ Sign UP """
    form_class = SignUpForm
    success_url = reverse_lazy('tests:login')
    template_name = "register.html"


@method_decorator(login_required, name='dispatch')
class UserLogout(LogoutView):
    """ Logout """
    next_page = reverse_lazy(HOME_URL_LITERAL)
    success_url = reverse_lazy(HOME_URL_LITERAL)
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


@method_decorator(login_required, name='dispatch')
class MyTestsView(TestsView):
    """
    List of active user tests
    """

    def get_queryset(self):
        return Test.objects.filter(author=self.request.user)


@method_decorator(login_required, name='dispatch')
class TestDetailView(DetailView):
    """
    Test page
    """
    model = Test
    template_name = 'test_detail.html'

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        comment_form = CreateCommentForm(self.request.POST or None)
        comment_form.fields['text'].widget.attrs.update(
            {'class': 'form-control mr-3'})
        context.update({'add_comment_form': comment_form})
        return context


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
        if question_count < MINIMUM_QUESTIONS and not test.draft:
            alert_msg = f"this test doesnt have {MINIMUM_QUESTIONS} questions"
            messages.error(self.request, alert_msg)
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
        return reverse(TEST_EDIT_LITERAL, kwargs={'pk': obj_id})

    def form_valid(self, form):
        test = form.save(commit=False)
        test.author = self.request.user
        form.instance.author = self.request.user
        form.save()
        return super(CreateTestView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class QuestionCreateView(CreateView):
    """
    Create question
    """
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
        return reverse(TEST_EDIT_LITERAL, kwargs={'pk': test_id})


@method_decorator(login_required, name='dispatch')
class DeleteQuestionView(DeleteView):
    """
    Delete question
    """
    model = Question

    def get_success_url(self):
        test_id = self.request.POST.get('test_id')
        return reverse(TEST_EDIT_LITERAL, kwargs={'pk': test_id})


@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    """
    Create comment
    """
    form_class = CreateCommentForm
    model = Comment

    def form_valid(self, form):
        comment = form.save(commit=False)
        test_id = self.request.POST.get('test_id')
        test = Test.objects.get(id=test_id)
        comment.test = test
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form=form)

    def get_success_url(self):
        test_id = self.request.POST.get('test_id')
        return reverse('tests:test_detail', kwargs={'pk': test_id})
