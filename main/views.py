from django.shortcuts import get_object_or_404, redirect, render

from .models import Batch, Student, StudentProgress, Topic


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
    topics = Topic.objects.order_by("order")
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
        order = request.POST.get("order")
        id = request.POST.get("id")

        if id:
            topic = Topic.objects.get(id=id)
            topic.name = name
            topic.order = order
            topic.save()
        else:
            topic = Topic(name=name, order=order)
            topic.save()
        return redirect("topic_page")


def delete_topic(request, t_id):
    topic = get_object_or_404(Topic, id=t_id)
    if topic:
        topic.delete()

    return redirect("topic_page")


def student_page(request, b_id):
    batch = Batch.objects.get(id=b_id)
    students = Student.objects.filter(batch=batch)
    context = {"students": students, "batch": batch}

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


def student_progress_page(request, s_id):

    student = get_object_or_404(Student.objects.select_related("batch"), id=s_id)
    completed_topic_ids = set(
        StudentProgress.objects.filter(student=student).values_list(
            "topic_id", flat=True
        )
    )

    topics = list(Topic.objects.order_by("order").values("id", "name"))
    for topic in topics:
        topic["completed"] = topic["id"] in completed_topic_ids

    context = {"topics": topics, "student": student, "b_id": student.batch.id}
    return render(request, "main/student/student_progress.html", context)


def toggle_progress(request):
    if request.method == "POST":
        s_id = request.POST.get("s_id")
        t_id = request.POST.get("t_id")

        student = Student.objects.get(id=s_id)
        topic = Topic.objects.get(id=t_id)

        old_progress = StudentProgress.objects.filter(student=student, topic=topic)
        if old_progress:
            old_progress.delete()
        else:
            StudentProgress(student=student, topic=topic).save()

        return redirect("student_progress_page", s_id)


def batch_progress(request, b_id):
    batch = Batch.objects.get(id=b_id)
    students = Student.objects.filter(batch=batch)
    student_ids = students.values_list("id", flat=True)

    all_progress = StudentProgress.objects.filter(
        student_id__in=student_ids
    ).select_related("topic")

    completed_map = {}
    for progress in all_progress:
        if progress.student_id not in completed_map:
            completed_map[progress.student_id] = set()
        completed_map[progress.student_id].add(progress.topic_id)

    print(completed_map)

    # Get all topics ONCE
    topics = list(Topic.objects.order_by("order").values("id", "name"))

    student_progress = {}
    for student in students:
        completed_ids = completed_map.get(student.id, set())

        student_topics = []
        for topic in topics:
            topic_copy = topic.copy()
            topic_copy["completed"] = topic_copy["id"] in completed_ids
            student_topics.append(topic_copy)

        if len(topics) > 0:
            percentage = (len(completed_ids) / len(topics)) * 100
        else:
            percentage = 0
        percentage = round(percentage)

        student_progress[student.id] = {
            "student": student,
            "topics": student_topics,
            "percentage": percentage,
        }

    context = {"student_progress": student_progress, "batch": batch}
    return render(request, "main/progress.html", context)
