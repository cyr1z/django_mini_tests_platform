from django.contrib import admin

# Register your models here.
# from django.utils.safestring import mark_safe

from .models import Test, TestsUser, PassedTests, Question, Comment


class TestsInline(admin.StackedInline):
    model = PassedTests
    fk_name = 'tests_user'
    extra = 0
    readonly_fields = ['passed_test', 'right_answers_count',
                       'question_count', 'pass_date_time', ]


@admin.register(TestsUser)
class TestsUserAdmin(admin.ModelAdmin):
    search_fields = ("last_name__startswith", "first_name__startswith",
                     "username__startswith", "email",)
    list_display = ("full_name", "username", "email",
                    "date_of_birth_format", "is_staff")
    inlines = [TestsInline,]


admin.site.register(Test)
admin.site.register(PassedTests)
admin.site.register(Question)
admin.site.register(Comment)
