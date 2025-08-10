import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

def chat_view(request):
    # Only renders the main chat page at "/"
    return render(request, 'chat2/chat.html')

@csrf_protect
def chat_api(request):
    if request.method == 'POST':
        try:
            # Parse the AJAX request
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            print("🔹 User message:", user_message)  # DEBUG

            if not user_message:
                return JsonResponse({'error': 'Message is empty'}, status=400)

            # Use the correct model name! (Get this from /api/models in OpenWebUI)
            payload = {
                "model": "llama3.2:3b",
                "messages": [{"role": "user", "content": user_message}]
            }
            api_url = "http://localhost:3000/api/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-da10b97c11c6487da2a3c9a7769f527b"
            }
            print("📤 POST", api_url)
            print("📦 Payload", payload)

            # Send to OpenWebUI backend
            r = requests.post(api_url, json=payload, headers=headers, timeout=30)
            print("📥 Backend status:", r.status_code)
            print("📥 Backend raw:", r.text[:500])

            if r.status_code == 200:
                try:
                    result = r.json()
                    # OpenWebUI returns 'choices' as a list, first item has message.content
                    bot_reply = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    print("🤖 Reply:", bot_reply)
                    return JsonResponse({'response': bot_reply})
                except Exception as e:
                    print("🚨 Backend JSON error:", e)
                    return JsonResponse({'error': 'Could not parse backend reply'}, status=502)
            else:
                print("❌ Backend non-200 error", r.status_code, r.text)
                return JsonResponse({'error': 'Backend error'}, status=r.status_code)

        except requests.RequestException as e:
            print("🔴 Cannot reach backend:", str(e))
            return JsonResponse({'error': 'Backend connection failed'}, status=503)
        except Exception as e:
            print("🔥 Internal error:", str(e))
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    # If GET or other method
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
