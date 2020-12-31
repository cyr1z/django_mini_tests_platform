from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import DateField
from django.utils import timezone


class TestsUser(AbstractUser):
    """
    Customised Django User Model
    Add about, avatar and date_of_birth
    """
    about = models.CharField(max_length=4096)
    date_of_birth = DateField()
    avatar = models.ImageField(
        verbose_name='avatar',
        upload_to='avatars',
        default='media/default_avatar.png',
        null=True,
        blank=True,
    )
    tests = models.ManyToManyField(
        'Test',
        through='PassedTests',
        related_name='users_who_passed_test'
    )

    @property
    def full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.full_name


class Test(models.Model):
    """
    Test
    """
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        TestsUser,
        related_name='authors_tests',
        on_delete=models.CASCADE
    )

    @property
    def question_count(self):
        return self.tests_questions.count()

    @property
    def pass_count(self):
        return self.users_who_passed_test.count()

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['created_at', 'title']

    def __str__(self):
        return f'test: "{self.title}"'


class PassedTests(models.Model):
    tests_user = models.ForeignKey(TestsUser, on_delete=models.CASCADE)
    passed_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    right_answers_count = models.PositiveIntegerField()
    question_count = models.PositiveIntegerField()
    pass_date_time = models.DateTimeField(default=timezone.now)

    @property
    def precent(self):
        return round((self.right_answers_count * 100 / self.question_count), 2)

    class Meta:
        ordering = ['pass_date_time']
        verbose_name = "Passed test"
        verbose_name_plural = "Passed tests"

    def __str__(self):
        return f'test: "{self.passed_test.title}" -' \
               f' {self.tests_user.full_name}:  ' \
               f'{self.right_answers_count} right / {self.precent}%'


class Question(models.Model):
    class RightAnswer(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4

    text = models.CharField(max_length=460)
    answer_one = models.CharField(max_length=460)
    answer_two = models.CharField(max_length=460)
    answer_three = models.CharField(max_length=460)
    answer_four = models.CharField(max_length=460)
    right_answer = models.IntegerField(choices=RightAnswer.choices)
    picture = models.ImageField(
        verbose_name='picture',
        upload_to='pictures',
        null=True,
        blank=True,
    )
    test = models.ForeignKey(
        Test,
        related_name='tests_questions',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['test', 'text']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'{self.test.title} -> {self.text[:25]}...'


class Comment(models.Model):
    text = models.CharField(max_length=460)
    created_at = models.DateTimeField(default=timezone.now)
    test = models.ForeignKey(
        Test,
        related_name='tests_comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        TestsUser,
        related_name='users_comments',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.user.full_name} to {self.test.title}: {self.text}'
