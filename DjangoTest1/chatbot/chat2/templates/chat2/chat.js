document.getElementById("chat-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const inputEl = document.getElementById("user-input");
    const chatWindow = document.getElementById("chat-window");
    const userText = inputEl.value;
    if (!userText) return;
    chatWindow.innerHTML += `<div><b>You:</b> ${userText}</div>`;
    inputEl.value = "";
    fetch("/chat2/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText })
    })
    .then(res => res.json())
    .then(data => {
        chatWindow.innerHTML += `<div><b>AI:</b> ${data.reply || data.error}</div>`;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    });
});
