from django.contrib import admin

from .models import Batch, Student, StudentProgress, Topic

admin.site.site_title = "Progress Tracker Dashboard"
admin.site.site_header = "Progress Tracker Dashboard"
admin.sites.index_title = "Progress Tracker Dashboard"

# Register your models here.
admin.site.register(Batch)
admin.site.register(Topic)
admin.site.register(Student)
admin.site.register(StudentProgress)
