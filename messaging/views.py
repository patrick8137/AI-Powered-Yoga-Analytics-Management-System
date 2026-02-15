from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message, BroadcastMessage
from instructors.models import InstructorStudent


@login_required
def inbox(request):
    user = request.user
    users = User.objects.none()
    if user.is_superuser:
        users = User.objects.exclude(id=user.id)

    elif hasattr(user, 'studentprofile'):
        student = user.studentprofile
        mapping = InstructorStudent.objects.filter(student=student).first()

        admins = User.objects.filter(is_superuser=True)

        if mapping:
            users = User.objects.filter(id=mapping.instructor.user.id) | admins
        else:
            users = admins

    elif hasattr(user, 'instructorprofile'):
        instructor = user.instructorprofile

        students = User.objects.filter(
            studentprofile__instructorstudent__instructor=instructor
        )
        admins = User.objects.filter(is_superuser=True)
        users = students | admins

    users = users.distinct()
    broadcasts = BroadcastMessage.objects.order_by('-created_at')

    return render(
        request,
        'messaging/inbox.html',
        {
            'users': users,
            'broadcasts': broadcasts,
        }
    )

@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

    return render(
        request,
        'messaging/chat.html',
        {
            'other_user': other_user,
            'messages': messages
        }
    )

