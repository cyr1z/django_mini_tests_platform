from django.contrib import admin

# Register your models here.
# from django.utils.safestring import mark_safe

from .models import Test, TestsUser, PassedTests, Question, Comment


admin.site.register(Test)
admin.site.register(TestsUser)
admin.site.register(PassedTests)
admin.site.register(Question)
admin.site.register(Comment)
