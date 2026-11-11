from django.urls import path

from . import views

urlpatterns = [
    path("", views.batch_page, name="batch_page"),
    path("save_batch_page/<int:b_id>/", views.save_batch_page, name="save_batch_page"),
    path("save_batch", views.save_batch, name="save_batch"),
    path("delete_batch/<int:b_id>/", views.delete_batch, name="delete_batch"),
    # Topic
    path("topics/", views.topic_page, name="topic_page"),
    path("save_topic_page/<int:t_id>/", views.save_topic_page, name="save_topic_page"),
    path("save_topic", views.save_topic, name="save_topic"),
    path("delete_topic/<int:t_id>/", views.delete_topic, name="delete_topic"),
    # Student
    path("students/<int:b_id>", views.student_page, name="student_page"),
    path(
        "save_student_page/<int:b_id>/<int:s_id>/",
        views.save_student_page,
        name="save_student_page",
    ),
    path("save_student/", views.save_student, name="save_student"),
    path(
        "delete_student/<int:id>/<int:b_id>/",
        views.delete_student,
        name="delete_student",
    ),
]
