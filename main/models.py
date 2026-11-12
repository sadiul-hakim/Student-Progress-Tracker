from django.db import models


# Create your models here.
class Batch(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=150)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=200)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} completed {self.topic}"
