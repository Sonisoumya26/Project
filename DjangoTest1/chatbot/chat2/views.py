import json
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


def chat_view(request):
    """
    Render the main chat page at "/"
    """
    return render(request, 'chat2/chat.html')


@csrf_protect
def chat_api(request):
    """
    Handle POST chat messages from the frontend and return plain text bot replies.
    """
    if request.method == 'POST':
        try:
            # Parse incoming JSON
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return HttpResponse("Error: Message is empty", status=400, content_type="text/plain")

            # Prepare payload for OpenWebUI
            payload = {
                "model": "llama3.2:3b",   # adjust if needed
                "messages": [{"role": "user", "content": user_message}]
            }
            api_url = "http://localhost:3000/api/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-da10b97c11c6487da2a3c9a7769f527b"
            }

            # Send request to OpenWebUI backend
            r = requests.post(api_url, json=payload, headers=headers, timeout=30)

            if r.status_code == 200:
                try:
                    result = r.json()
                    # Extract bot reply text
                    bot_reply = (
                        result.get('choices', [{}])[0]
                        .get('message', {})
                        .get('content', '')
                        .strip()
                    )

                    if not bot_reply:
                        return HttpResponse("Error: Empty reply from backend",
                                            status=502,
                                            content_type="text/plain")

                    # ✅ Return plain text response
                    return HttpResponse(bot_reply, content_type="text/plain")

                except Exception as e:
                    return HttpResponse("Error: Could not parse backend reply",
                                        status=502,
                                        content_type="text/plain")
            else:
                return HttpResponse(f"Error: Backend returned {r.status_code}",
                                    status=r.status_code,
                                    content_type="text/plain")

        except requests.RequestException:
            return HttpResponse("Error: Backend connection failed",
                                status=503,
                                content_type="text/plain")
        except Exception:
            return HttpResponse("Error: Internal Server Error",
                                status=500,
                                content_type="text/plain")

    # Method not allowed
    return HttpResponse("Error: Only POST allowed",
                        status=405,
                        content_type="text/plain")
