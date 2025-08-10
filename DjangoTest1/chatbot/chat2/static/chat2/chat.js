document.addEventListener('DOMContentLoaded', () => {
    console.log('chat.js loaded');

    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const chatbox = document.getElementById('chatbox');

    // --- Get CSRF token (Django) ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            for (let cookie of document.cookie.split(';')) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- Append message (label + message same line) ---
    function appendMessage(sender, text, domId, extraClass = '') {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        if (extraClass) msgDiv.classList.add(extraClass);
        if (domId) msgDiv.id = domId;

        // SAME line after label
        msgDiv.innerHTML = `<b>${sender === 'user' ? 'You' : 'Bot'}:</b> ` +
            text.replace(/\n/g, '<br>');

        msgDiv.style.display = 'block';
        msgDiv.style.clear = 'both';

        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
        return msgDiv;
    }

    // --- Typing animation ---
    function startTypingAnimation(domId) {
        const el = document.getElementById(domId);
        if (!el) return;
        let dots = 0;
        el._typingInterval = setInterval(() => {
            dots = (dots + 1) % 4;
            el.innerHTML = `<b>Bot:</b> <span class="bot-typing-animated">Typing${'.'.repeat(dots)}</span>`;
        }, 500);
    }
    function stopTypingAnimation(domId) {
        const el = document.getElementById(domId);
        if (!el) return;
        clearInterval(el._typingInterval);
        el._typingInterval = null;
    }

    // --- Enter sends, Shift+Enter = newline ---
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.requestSubmit();
        }
    });

    // --- On form submit ---
    form.onsubmit = async (e) => {
        e.preventDefault();
        const userMessage = input.value.trim();
        if (!userMessage) return;

        appendMessage('user', userMessage);
        input.value = '';

        // Show typing animation
        const typingId = `bot-typing-${Date.now()}`;
        appendMessage('bot', 'Typing', typingId, 'bot-typing-animated');
        startTypingAnimation(typingId);
        const startTime = Date.now();

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);

            if (response.body && window.ReadableStream) {
                // Streaming response
                const elapsed = Date.now() - startTime;
                if (elapsed < 1000) await new Promise(r => setTimeout(r, 1000 - elapsed));

                stopTypingAnimation(typingId);
                document.getElementById(typingId)?.remove();

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let botMessage = '';
                const botMsgDiv = appendMessage('bot', '', `bot-msg-${Date.now()}`);

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    botMessage += decoder.decode(value, { stream: true });
                    botMsgDiv.innerHTML = `<b>Bot:</b> ` + botMessage.replace(/\n/g, '<br>');
                    chatbox.scrollTop = chatbox.scrollHeight;
                }
            } else {
                // Plain-text response
                const textReply = await response.text();
                const elapsed = Date.now() - startTime;
                if (elapsed < 1000) await new Promise(r => setTimeout(r, 1000 - elapsed));

                stopTypingAnimation(typingId);
                document.getElementById(typingId)?.remove();
                appendMessage('bot', textReply);
            }
        } catch (err) {
            stopTypingAnimation(typingId);
            document.getElementById(typingId)?.remove();
            appendMessage('bot', 'Server error. Please try again later.');
            console.error(err);
        }
    };
});
