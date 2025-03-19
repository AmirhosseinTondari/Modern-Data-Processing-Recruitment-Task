from django.http import HttpRequest, StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from langchain_community.chat_message_histories import ChatMessageHistory

from . import engines

# Used to store and manage user and AI messages in memory. 
# However, in production enviroment databases like Reddis need to be used.
# TODO Reddis for User Message history
chat_history = ChatMessageHistory()

class HistoryView(APIView):
    """
    Provides an endpoint to retrieve the entire chat history.
    """
    def get(self, requset:HttpRequest) -> list:
        return Response(chat_history.dict())

class CoTView(APIView):
    """
    Endpoint for processing user messages.
    and streams responses from the CoT engine.
    """
    def stream(self, generator):
        """
        Collects and streams the content from a generator (CoT engine's response stream).
        Once the final response is received, 
        it splits the content to extract and store the AI's final response in the chat_history.
        and omits the thoughts part of response
        """
        response_content = ""
        for i in generator:
            i = i.content
            response_content += i
            yield i

        _, response = response_content.split("Final Response: ")
        chat_history.add_ai_message(response)

    def get(self, request:HttpRequest) -> dict:
        """
        request with a query parameter message.
        Adds the user's message to the chat history.
        Passes the chat history to the CoT engine.
        Returns a StreamingHttpResponse that streams the generated response to the endpoint.
        """
        message = request.GET.get("message")
        chat_history.add_user_message(message)
        res = engines.CoT.chain.stream({"history": chat_history.messages})

        return StreamingHttpResponse(self.stream(res), content_type="text/plain", status=status.HTTP_200_OK)
