from django.contrib import admin

from .models import Batch, Student, Topic

# Register your models here.
admin.site.register(Batch)
admin.site.register(Topic)
admin.site.register(Student)
