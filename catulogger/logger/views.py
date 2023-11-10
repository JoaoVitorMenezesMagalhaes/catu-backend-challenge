from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from django.db.models import Count
from django.db.models.functions import TruncDate

# import Response
from rest_framework.response import Response

# importing models
from .models import Log

# importing status
from rest_framework import status

# Create your views here.
class LogViewset(viewsets.ViewSet):
    
    @action(detail=False, methods=["get"], url_path="hello-world")
    def hello_world(self, request):
        return Response({"message": "Hello, world!"})
    
    @action(detail=False, methods=["post"], url_path="ping")
    def ping(self, request):
        return Response({"message": "pong", "data": request.data})
      
    
    @action(detail=False, methods=["post"], url_path="create-log")
    def create_log(self, request):
        try:
            log = Log.objects.create(
                who=request.data["who"],
                action_type=request.data["action_type"],
                object_type=request.data["object_type"],
                object_id=request.data["object_id"],
            )
            return Response({"message": "Log created", "data": log.to_json()})
        except KeyError as e:
            return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["get"], url_path="get-logs")
    def get_logs(self, request):
        logs = Log.objects.all()
        return Response({"message": "Logs retrieved", "data": [log.to_json() for log in logs]})
    

    @action(detail=False, methods=["get"], url_path="get-logs-by-date")
    def get_logs_by_date(self, request):
        try:
            logs = Log.objects.filter(created_at__date=request.query_params["date"])
            return Response({"message": "Logs retrieved", "data": [log.to_json() for log in logs]})
        except KeyError as e:
            return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=False, methods=["get"], url_path="get-logs-by-user")
    def get_logs_by_user(self, request):
        try:
            logs = Log.objects.filter(who=request.query_params["user"])
            return Response({"message": "Logs retrieved", "data": [log.to_json() for log in logs]})
        except KeyError as e:
            return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=["get"], url_path="get-logs-count-by-day")
    def get_logs_count_by_day(self, request):
        try:
            start_date = request.query_params["start_date"]
            end_date = request.query_params["end_date"]

            logs_count_by_day = (
                Log.objects
                .filter(created_at__date__range=[start_date, end_date])
                .annotate(day=TruncDate("created_at"))
                .values("day", "action_type")
                .annotate(count=Count("id"))
            )

            result = {}
            for log_count in logs_count_by_day:
                day = log_count["day"].strftime("%d/%m/%Y")
                action_type = log_count["action_type"]
                count = log_count["count"]

                if day not in result:
                    result[day] = {}

                result[day][action_type] = count

            return Response({"message": "Logs count by day retrieved", "data": result})
        except KeyError as e:
            return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)





