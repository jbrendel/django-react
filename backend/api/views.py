from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def welcome_message(request):
    """Return a welcome message for the frontend to display."""
    return Response({"message": "Hello World!"})
