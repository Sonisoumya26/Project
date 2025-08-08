from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os

# Load environment variables
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:3000/api/chat/completions")
LLM_API_KEY = os.getenv("sk-6e6fd81ee8e244d58d8cfa230dace65d")

def index(request):
    return HttpResponse("Hi, I am Soumya")

def welcome(request):
    return render(request, 'chat2/welcome.html')

def chat_page(request):
    return render(request, 'chat2/chat.html')

@csrf_exempt
def chat_with_llm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            payload = {"model": "llama3.2:3b", "messages": [{"role": "user", "content": user_message}]}
            headers = {
                "Authorization": f"Bearer {LLM_API_KEY}" if LLM_API_KEY else "",
                "Content-Type": "application/json"
            }
            response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No reply.")

            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
