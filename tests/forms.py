from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.forms.widgets import RadioSelect

from tests.models import TestsUser, Test, Question, Comment


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.')
    date_of_birth = forms.DateField()

    class Meta:
        model = TestsUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'password1',
            'password2',
            'avatar',
            'about',
        ]


class CreateTestForm(ModelForm):
    class Meta:
        model = Test
        fields = [
            'title',
            'description',
        ]


class CreateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            'text',
            'answer_one',
            'answer_two',
            'answer_three',
            'answer_four',
            'right_answer',
        ]


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]


class TestPassForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super(TestPassForm, self).__init__(*args, **kwargs)
        for question in questions:

            choice_list = (
                (1, question.answer_one),
                (2, question.answer_two),
                (3, question.answer_three),
                (4, question.answer_four),
            )
            self.fields[question.id] = forms.ChoiceField(
                choices=choice_list,
                widget=RadioSelect,
                label=question.text
            )


class SearchBoxForm(forms.Form):
    q = forms.CharField()

