document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const chatbox = document.getElementById('chatbox');

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.textContent = (sender === 'user' ? 'You: ' : 'Bot: ') + text;
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    form.onsubmit = async (e) => {
        e.preventDefault();
        const userMessage = input.value.trim();
        if (!userMessage) return;

        appendMessage('user', userMessage);
        input.value = '';

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();

            if (data.response) {
                appendMessage('bot', data.response);
            } else if (data.error) {
                appendMessage('bot', 'Error: ' + data.error);
            } else {
                appendMessage('bot', 'Unexpected response.');
            }
        } catch (err) {
            appendMessage('bot', 'Server error, try again later.');
            console.error('Chat API error:', err);
        }
    };
});
