from django.shortcuts import get_object_or_404, redirect, render

from .models import Batch, Student, Topic


# Create your views here.
def progress_page(request):
    return render(request, "main/progress.html")


def batch_page(request):
    batches = Batch.objects.all()
    context = {"batches": batches}

    return render(request, "main/batch/batch.html", context)


def save_batch_page(request, b_id):

    if b_id:
        batch = Batch.objects.get(id=b_id)
        context = {"batch": batch}
        return render(request, "main/batch/save_batch.html", context)

    return render(request, "main/batch/save_batch.html")


def save_batch(request):
    if request.method == "POST":
        name = request.POST.get("name")
        id = request.POST.get("id")

        if id:
            batch = Batch.objects.get(id=id)
            batch.name = name
            batch.save()
        else:
            batch = Batch(name=name)
            batch.save()
        return redirect("batch_page")


def delete_batch(request, b_id):
    batch = get_object_or_404(Batch, id=b_id)
    if batch:
        batch.delete()

    return redirect("batch_page")


def topic_page(request):
    topics = Topic.objects.all()
    context = {"topics": topics}

    return render(request, "main/topic/topic.html", context)


def save_topic_page(request, t_id):

    if t_id:
        topic = Topic.objects.get(id=t_id)
        context = {"topic": topic}
        return render(request, "main/topic/save_topic.html", context)

    return render(request, "main/topic/save_topic.html")


def save_topic(request):
    if request.method == "POST":
        name = request.POST.get("name")
        id = request.POST.get("id")

        if id:
            topic = Topic.objects.get(id=id)
            topic.name = name
            topic.save()
        else:
            topic = Topic(name=name)
            topic.save()
        return redirect("topic_page")


def delete_topic(request, t_id):
    topic = get_object_or_404(Topic, id=t_id)
    if topic:
        topic.delete()

    return redirect("topic_page")


def student_page(request, b_id):
    students = Student.objects.filter(batch=b_id)
    context = {"students": students, "b_id": b_id}

    return render(request, "main/student/student.html", context)


def save_student_page(request, b_id, s_id):

    if s_id:
        student = Student.objects.get(id=s_id)
        context = {"student": student, "b_id": b_id}
        return render(request, "main/student/save_student.html", context)

    context = {"b_id": b_id}
    return render(request, "main/student/save_student.html", context)


def save_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        b_id = request.POST.get("b_id")
        s_id = request.POST.get("s_id")

        batch = Batch.objects.get(id=b_id)
        if s_id:
            student = Student.objects.get(id=s_id)
            student.name = name
            student.save()
        else:
            student = Student(name=name, batch=batch)
            student.save()
        return redirect("student_page", b_id=b_id)


def delete_student(request, id, b_id):
    student = get_object_or_404(Student, id=id)
    if student:
        student.delete()

    return redirect("student_page", b_id=b_id)
