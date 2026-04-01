// ── Chat Functions ─────────────────────────────────────────────────────────────

function sendMessage() {
    const input = document.getElementById("chat-input");
    const messagesDiv = document.getElementById("chat-messages");

    if (!input) return; // we're not on the chat page
    
    const userText = input.value.trim();
    if (!userText) return;

    // add the user's message to the chat
    appendMessage("user", userText, "👤");
    input.value = "";

    // show a loading indicator while waiting for the AI
    const loadingId = appendMessage("bot", "Thinking...", "🤖", "message-loading");

    // call our Flask backend
    fetch("/chat/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText })
    })
    .then(response => response.json())
    .then(data => {
        // remove loading message and show the real response
        const loadingEl = document.getElementById(loadingId);
        if (loadingEl) loadingEl.remove();

        if (data.error) {
            appendMessage("bot", "Sorry, something went wrong. Please try again.", "🤖");
        } else {
            appendMessage("bot", data.response, "🤖");
        }
    })
    .catch(err => {
        const loadingEl = document.getElementById(loadingId);
        if (loadingEl) loadingEl.remove();
        appendMessage("bot", "Network error. Make sure the server is running.", "🤖");
        console.error("Chat error:", err);
    });
}


function appendMessage(type, text, avatar, extraClass = "") {
    const messagesDiv = document.getElementById("chat-messages");
    const id = "msg-" + Date.now();

    const messageDiv = document.createElement("div");
    messageDiv.className = `message message-${type} ${extraClass}`;
    messageDiv.id = id;

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-bubble">${escapeHtml(text)}</div>
    `;

    messagesDiv.appendChild(messageDiv);
    // scroll to bottom so newest message is visible
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    return id;
}


function fillSuggestion(button) {
    const input = document.getElementById("chat-input");
    if (input) {
        input.value = button.textContent;
        input.focus();
    }
}


// simple html escaping so user input doesn't break the page
function escapeHtml(text) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}


// ── Newsletter Copy ────────────────────────────────────────────────────────────

function copyNewsletter() {
    const content = document.getElementById("newsletter-content");
    if (!content) return;

    navigator.clipboard.writeText(content.innerText).then(() => {
        // temporarily change button text to give user feedback
        const btn = document.querySelector(".newsletter-actions .btn");
        const originalText = btn.textContent;
        btn.textContent = "✅ Copied!";
        setTimeout(() => { btn.textContent = originalText; }, 2000);
    }).catch(err => {
        console.error("Copy failed:", err);
        alert("Could not copy. Please select and copy the text manually.");
    });
}
