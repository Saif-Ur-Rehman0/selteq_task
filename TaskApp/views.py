from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from django.db import connection
from django.http import JsonResponse
from TaskApp.tasks import print_tasks

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:4]
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_task(request, task_id):
    user_id = request.user.id
    sql_query = """
        SELECT id, title, duration, created_at, updated_at 
        FROM TaskApp_task 
        WHERE id = %s AND user_id = %s
    """
        
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [task_id, user_id])
        row = cursor.fetchone()  # Get the single result

    if row:
        task_data = {
            "id": row[0],
            "title": row[1],
            "duration": row[2],
            "created_at": row[3],
            "updated_at": row[4]
        }
        return JsonResponse(task_data) 
    else:
        return JsonResponse({"detail": "Task not found."}, status=404)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_title(request, task_id):
    user_id = request.user.id
    
    title = request.data.get('title')
    
    if not title:
        return JsonResponse({"detail": "Title is required."}, status=400)
    
    sql_query = """
        UPDATE TaskApp_task
        SET title = %s
        WHERE id = %s AND user_id = %s
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [title, task_id, user_id])
            cursor.execute("SELECT TOP 1 title FROM TaskApp_task WHERE id = %s AND user_id = %s", [task_id, user_id])
            updated_count = cursor.fetchone()
            if updated_count != None and updated_count[0] == title:
                return JsonResponse({"detail": "Task updated successfully."}, status=200)
            else:
                return JsonResponse({"detail": "Task not found or not owned by user."}, status=404)
    except Exception as e:
        return JsonResponse({"detail": "An unexpected error occurred. Please try again.", "error": str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    user = request.user
    try:
        task = Task.objects.get(id=task_id, user=user)
        task.delete()
        return JsonResponse({"detail": "Task deleted successfully."}, status=200)
    except Task.DoesNotExist:
        return JsonResponse({"detail": "Task not found or not owned by user."}, status=404)


def trigger_print_tasks(request):
    print_tasks.delay()
    return JsonResponse({"detail": "Task is being processed."})