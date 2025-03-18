import json
from time import sleep
from django.shortcuts import render
from django.http import HttpRequest, StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from langchain_community.chat_message_histories import ChatMessageHistory

from . import engines

chat_history = ChatMessageHistory()
# chat_history.add_user_message("hi")
# chat_history.add_ai_message("Hi there! How can I assist you today?")

class HistoryView(APIView):
    def get(self, requset:HttpRequest) -> list:
        return Response(chat_history.dict())

class CoTView(APIView):
    def stream(self, generator):
        response_content = ""
        for i in generator:
            i = i.content
            response_content += i
            yield i

        _, response = response_content.split("Final Response: ")
        chat_history.add_ai_message(response)

    def get(self, request:HttpRequest) -> dict:
        message = request.GET.get("message")
        chat_history.add_user_message(message)
        res = engines.CoT.chain.stream({"history": chat_history.messages})

        return StreamingHttpResponse(self.stream(res), content_type="text/plain")
