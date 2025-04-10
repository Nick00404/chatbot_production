document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.querySelector('.chat-messages');
    const uploadInput = document.getElementById('imageUpload');
    const sessionList = document.querySelector('.session-list');
    const newChatButton = document.querySelector('.new-chat');

    let currentSessionId = null;

    // Load sessions on start
    fetch('/api/sessions')
        .then(res => res.json())
        .then(data => {
            data.sessions.forEach(session => addSessionToList(session));
        });

    // Create new session
    newChatButton.addEventListener('click', () => {
        fetch('/api/sessions', {
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            currentSessionId = data.session_id;
            clearMessages();
            addSessionToList(data.session_id);
        });
    });

    // Send message
    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (!message || !currentSessionId) return;

        appendMessage('user', message);
        messageInput.value = '';

        fetch(`/api/chat/${currentSessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            appendMessage('bot', data.response);
        })
        .catch(err => {
            appendMessage('bot', 'Error: Unable to get response.');
            console.error(err);
        });
    });

    // Upload image
    uploadInput.addEventListener('change', () => {
        const file = uploadInput.files[0];
        if (!file || !currentSessionId) return;

        const formData = new FormData();
        formData.append('image', file);

        fetch(`/api/chat/${currentSessionId}/image`, {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            appendMessage('user', `[Image Uploaded]`);
            appendMessage('bot', data.response);
        })
        .catch(err => {
            appendMessage('bot', 'Error: Failed to process image.');
            console.error(err);
        });
    });

    // Helper: Add message to UI
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerText = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Helper: Clear messages
    function clearMessages() {
        chatMessages.innerHTML = '';
    }

    // Helper: Add session to sidebar
    function addSessionToList(sessionId) {
        const sessionItem = document.createElement('div');
        sessionItem.className = 'session-item';
        sessionItem.innerHTML = `
            <span>Session ${sessionId}</span>
            <span class="delete-session">&times;</span>
        `;

        sessionItem.querySelector('.delete-session').addEventListener('click', () => {
            fetch(`/api/sessions/${sessionId}`, { method: 'DELETE' })
                .then(() => sessionItem.remove());
        });

        sessionItem.addEventListener('click', () => {
            currentSessionId = sessionId;
            fetch(`/api/sessions/${sessionId}`)
                .then(res => res.json())
                .then(data => {
                    clearMessages();
                    data.messages.forEach(m => {
                        appendMessage(m.role, m.content);
                    });
                });
        });

        sessionList.appendChild(sessionItem);
    }
});
