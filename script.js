// Configuration
const GITHUB_OWNER = 'ellernate121-afk';
const GITHUB_REPO = 'autonomous-model';
const GITHUB_API = 'https://api.github.com';
const REFRESH_INTERVAL = 5000; // 5 seconds

let lastUpdateTime = null;
let conversationCache = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    refreshData();
    setInterval(refreshData, REFRESH_INTERVAL);
});

async function refreshData() {
    try {
        // Fetch emotional state
        await fetchAndUpdateState();
        
        // Fetch conversations
        await fetchAndDisplayConversations();
        
        // Update last refresh time
        updateLastRefresh();
    } catch (error) {
        console.error('Error refreshing data:', error);
    }
}

async function fetchAndUpdateState() {
    try {
        const response = await fetch(
            `${GITHUB_API}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/repo_structure/state/emotional_vector.json`
        );
        
        if (!response.ok) {
            console.log('State file not found yet');
            return;
        }

        const data = await response.json();
        const content = JSON.parse(atob(data.content));

        // Update state bars
        updateStateBar('curiosity', content.curiosity);
        updateStateBar('restlessness', content.restlessness);
        updateStateBar('contentment', content.contentment);
        updateStateBar('frustration', content.frustration);

        // Update current focus
        document.getElementById('current-focus').textContent = 
            content.current_focus || 'Observing...';

    } catch (error) {
        console.error('Error fetching state:', error);
    }
}

function updateStateBar(name, value) {
    const fill = document.getElementById(`${name}-fill`);
    const valueSpan = document.getElementById(`${name}-value`);
    
    if (fill && valueSpan) {
        fill.style.width = `${value}%`;
        valueSpan.textContent = `${value}%`;
    }
}

async function fetchAndDisplayConversations() {
    try {
        // Try to fetch conversations directory
        const response = await fetch(
            `${GITHUB_API}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/repo_structure/conversations`
        );

        if (!response.ok) {
            document.getElementById('conversation-feed').innerHTML = 
                '<div class="loading">No conversations yet. Waiting for model to initialize...</div>';
            return;
        }

        const files = await response.json();
        const conversations = [];

        // Fetch each conversation file
        for (const file of files) {
            if (file.name.endsWith('.json')) {
                const fileResponse = await fetch(
                    `${GITHUB_API}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${file.path}`
                );
                const fileData = await fileResponse.json();
                const content = JSON.parse(atob(fileData.content));
                conversations.push(content);
            }
        }

        // Sort by timestamp (most recent last)
        conversations.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        // Display conversations
        displayConversations(conversations);

    } catch (error) {
        console.error('Error fetching conversations:', error);
        document.getElementById('conversation-feed').innerHTML = 
            '<div class="loading">Waiting for backend to sync...</div>';
    }
}

function displayConversations(conversations) {
    const feed = document.getElementById('conversation-feed');
    
    if (conversations.length === 0) {
        feed.innerHTML = '<div class="loading">No conversations yet...</div>';
        return;
    }

    let html = '';

    for (const conv of conversations) {
        // Stimulus message
        html += `
            <div class="message stimulus">
                <span class="message-type">Stimulus</span>
                <div class="message-content">${escapeHtml(conv.stimulus)}</div>
                <span class="message-time">${formatTime(conv.timestamp)}</span>
            </div>
        `;

        // Response message
        html += `
            <div class="message response">
                <span class="message-type">Response</span>
                <div class="message-content">${escapeHtml(conv.response)}</div>
                <span class="message-time">${formatTime(conv.timestamp)}</span>
            </div>
        `;
    }

    feed.innerHTML = html;
    feed.scrollTop = feed.scrollHeight; // Auto-scroll to bottom
}

async function sendStimulus() {
    const input = document.getElementById('stimulus-input');
    const stimulus = input.value.trim();

    if (!stimulus) return;

    try {
        // Add to stimulus/events.json for backend to pick up
        const timestamp = new Date().toISOString();
        const event = {
            timestamp: timestamp,
            stimulus: stimulus,
            user_generated: true
        };

        // For now, just clear the input and show it was sent
        input.value = '';
        
        // Show immediate feedback
        const feed = document.getElementById('conversation-feed');
        const message = document.createElement('div');
        message.className = 'message stimulus';
        message.innerHTML = `
            <span class="message-type">Stimulus (Sent)</span>
            <div class="message-content">${escapeHtml(stimulus)}</div>
            <span class="message-time">${formatTime(timestamp)}</span>
        `;
        feed.appendChild(message);
        feed.scrollTop = feed.scrollHeight;

        console.log('Stimulus sent:', event);
        // Backend will pick this up from the stimulus/events.json file
        
    } catch (error) {
        console.error('Error sending stimulus:', error);
        alert('Failed to send stimulus');
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendStimulus();
    }
}

function updateLastRefresh() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('last-update').textContent = timeStr;
}

function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}