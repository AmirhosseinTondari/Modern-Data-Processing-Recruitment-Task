from django.http import HttpRequest, StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from time import sleep
import json

from . import engines

cot_engine = engines.CoT()
cotsc_engine = engines.CoTSC()


class HistoryView(APIView):
    """
    Provides an endpoint to retrieve the entire chat history.
    """
    def get(self, requset:HttpRequest) -> list:
        return Response(engines.chat_history.dict())

class CoTView(APIView):
    """
    Endpoint for processing user messages.
    and streams responses from the CoT engine.
    """

    def get(self, request:HttpRequest) -> dict:
        """
        request with a query parameter message.
        Adds the user's message to the chat history.
        Passes the chat history to the CoT engine.
        Returns a StreamingHttpResponse that streams the generated response to the endpoint.
        """
        message = request.GET.get("message")

        return StreamingHttpResponse(cot_engine.stream(message), content_type="text/plain", status=status.HTTP_200_OK)

class CoTSCView(APIView):
    def get(self, request:HttpRequest) -> dict:
        """
        request with a query parameter message.
        Adds the user's message to the chat history.
        Passes the chat history to the CoTSC engine.
        Returns a StreamingHttpResponse that streams the generated response to the endpoint.
        """
        message = request.GET.get("message")
        
        return StreamingHttpResponse(cotsc_engine.stream(message),  content_type="text/plain", status=status.HTTP_200_OK)
    
class test(APIView):
    def t(self):
        for i in range(5):
            sleep(1)    
            yield json.dumps({"a":1}) + "\n"
    def get(self, r):
        return StreamingHttpResponse(self.t(), content_type="text/plain")
        