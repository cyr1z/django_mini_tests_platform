from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from tests.models import TestsUser, Test, Question


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

    class Meta:
        model = TestsUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            #'date_of_birth',
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
