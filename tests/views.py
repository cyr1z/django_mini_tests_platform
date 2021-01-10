from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, \
    DetailView, DeleteView

from django_tests_mini_platform.settings import DEFAULT_TESTS_ORDERING, \
    TESTS_ORDERINGS, MINIMUM_QUESTIONS, HOME_URL_LITERAL, TEST_EDIT_LITERAL
from tests.forms import SignUpForm, CreateTestForm, CreateQuestionForm, \
    CreateCommentForm, TestPassForm, SearchBoxForm
from tests.models import Test, TestsUser, Question, Comment, PassedTests


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

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        test_pass_records = PassedTests.objects.filter(tests_user=self.object)

        context.update({'test_pass_records': test_pass_records})
        return context


@method_decorator(login_required, name='dispatch')
class TestsView(ListView):
    """
    List of tests
    """
    model = Test
    paginate_by = 10
    template_name = 'tests.html'

    queryset = Test.objects.all()
    base_filter = Q(draft=False)

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', DEFAULT_TESTS_ORDERING)
        # validate ordering
        if ordering not in TESTS_ORDERINGS:
            ordering = DEFAULT_TESTS_ORDERING
        return ordering

    def get_queryset(self):
        search = self.request.GET.get('q')
        passed = self.request.GET.get('passed')
        # query = Q(author=self.request.user)
        query = self.base_filter
        if search:
            query &= Q(title__icontains=search)
        # if passed and passed in ['passed', 'unmatched']:
        #     query &= Q(user_who_passed_test__contains=self.request.user)
        return self.queryset.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': SearchBoxForm,
        })
        return context



@method_decorator(login_required, name='dispatch')
class MyTestsView(TestsView):
    """
    List of active user tests
    """

    def get_queryset(self):
        self.base_filter = Q(author=self.request.user)
        return super().get_queryset()



@method_decorator(login_required, name='dispatch')
class TestDetailView(DetailView):
    """
    Test detail page
    """
    model = Test
    template_name = 'test_detail.html'

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        users_who_passed_test = self.object.users_who_passed_test.all()
        score_block = self.request.user in users_who_passed_test

        if score_block:
            user_test_record = PassedTests.objects.get(
                tests_user=self.request.user,
                passed_test=self.object
            )
            context.update({
                'right_answers_count': user_test_record.right_answers_count,
                'percentage': user_test_record.percentage,
                'question_count': user_test_record.question_count,

            })

        comment_form = CreateCommentForm(self.request.POST or None)
        comment_form.fields['text'].widget.attrs.update(
            {'class': 'form-control mr-3'})
        context.update({
            'add_comment_form': comment_form,
            'score_block': score_block
        })
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


@method_decorator(login_required, name='dispatch')
class TestPassView(DetailView):
    """
    Test page
    """
    model = Test
    template_name = 'test_pass.html'

    # Add  to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        questions = self.object.test_questions.all()
        test_form = TestPassForm(questions=questions)

        context.update({'test_form': test_form})
        return context


@method_decorator(login_required, name='dispatch')
class TestCheckView(CreateView):
    """
    Test check and create PassedTests relationship
    """
    form_class = TestPassForm

    def get_success_url(self):
        test_id = self.request.POST.get('test_id')
        return reverse('tests:test_detail', kwargs={'pk': test_id})

    def post(self, *args, **kwargs):
        test_id = self.request.POST.get('test_id')
        test = Test.objects.get(id=test_id)
        question = test.test_questions.filter(test=test)
        post_dict = self.request.POST.dict()
        answers = {int(k): int(v) for k, v in post_dict.items() if k.isdigit()}

        right_answers_count = 0
        for k, v in answers.items():
            if v == question.get(id=k).right_answer:
                right_answers_count += 1

        through_defaults = {
            'right_answers_count': right_answers_count,
            'question_count': question.count(),
        }

        if test in self.request.user.tests.all():
            self.request.user.tests.remove(test)

        self.request.user.tests.add(test, through_defaults=through_defaults)

        return HttpResponseRedirect(self.get_success_url())
