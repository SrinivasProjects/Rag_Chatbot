
document.addEventListener('DOMContentLoaded', function() {
    // PDF Upload
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('pdfFile');
    const chatHistory = document.getElementById('chatHistory');

    uploadBtn.addEventListener('click', function() {
        if (!fileInput.files.length) {
            fileInput.click();
        } else {
            uploadForm.dispatchEvent(new Event('submit', {cancelable: true, bubbles: true}));
        }
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (!fileInput.files.length) {
            appendMessage('Please select a PDF file.', 'bot');
            fileInput.focus();
            return;
        }
        appendMessage('Uploading PDF...', 'bot');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        try {
            const response = await fetch('/upload_pdf/', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.status) {
                appendMessage(result.status, 'bot');
            } else {
                appendMessage(result.error || 'Upload failed.', 'bot');
            }
        } catch (err) {
            appendMessage('Error uploading PDF.', 'bot');
        }
        // Reset file input so user can upload again
        fileInput.value = '';
        fileInput.focus();
    });

    // Ask Question
    const askForm = document.getElementById('askForm');
    askForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const questionInput = document.getElementById('questionInput');
        const question = questionInput.value.trim();
        if (!question) {
            appendMessage('Please enter a question.', 'bot');
            return;
        }
        appendMessage(question, 'user');
        appendMessage('Thinking...', 'bot', true);
        try {
            const formData = new URLSearchParams();
            formData.append('question', question);
            const response = await fetch('/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });
            const result = await response.json();
            // Remove the 'Thinking...' bubble
            removeLastBotThinking();
            if (result.answer) {
                appendMessage(result.answer, 'bot');
            } else {
                appendMessage(result.error || 'No answer found.', 'bot');
            }
        } catch (err) {
            removeLastBotThinking();
            appendMessage('Error getting answer.', 'bot');
        }
    });

    function appendMessage(text, sender, isThinking=false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('bubble');
        msgDiv.classList.add(sender === 'user' ? 'user-bubble' : 'bot-bubble');
        if (isThinking) {
            msgDiv.classList.add('thinking');
            msgDiv.innerHTML = `<span class="bot-thinking-icon"><i class="fa-solid fa-robot"></i></span> <span class="spinner"></span> <span class="thinking-text">Thinking...</span>`;
        } else {
            msgDiv.textContent = text;
        }
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function removeLastBotThinking() {
        const bubbles = chatHistory.querySelectorAll('.bubble.bot-bubble.thinking');
        if (bubbles.length) {
            bubbles[bubbles.length-1].remove();
        }
    }
});
