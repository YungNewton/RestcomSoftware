from rest_framework.response import Response
from rest_framework.views import APIView
from celery.result import AsyncResult
from celery import current_app

class CancelBulkEmailView(APIView):
    def post(self, request):
        task_id = request.data.get("task_id")
        if not task_id:
            return Response({"error": "task_id required"}, status=400)

        try:
            current_app.control.revoke(task_id, terminate=True)
            return Response({"message": "Task cancelled."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CheckTaskStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        return Response({
            "state": result.state,
            "info": result.info  # Can include {"success": 5, "failure": 0}
        })