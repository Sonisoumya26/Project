from django.db import models

# Create your models here.
from transformers import pipeline
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Load only once at startup (pick a model you have downloaded)
llm = pipeline("text-generation", model="distilgpt2", device=-1)

@csrf_exempt
def chat_with_llm(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        result = llm(user_message, max_new_tokens=50)
        ai_text = result[0]["generated_text"]

        return JsonResponse({"reply": ai_text})
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
