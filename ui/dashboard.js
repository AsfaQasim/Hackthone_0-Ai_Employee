// Email Dashboard JavaScript
let allEmails = [];
let filteredEmails = [];

// Load emails from Needs_Action folder
async function loadEmails() {
    try {
        const response = await fetch('/api/emails');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allEmails = await response.json();
        filteredEmails = [...allEmails];
        console.log('Loaded emails:', allEmails.length);
        updateStats();
        renderEmails();
    } catch (error) {
        console.error('Error loading emails:', error);
        document.getElementById('emailList').innerHTML = 
            '<div class="no-results">Error loading emails. Make sure the server is running.</div>';
    }
}

// Update statistics
function updateStats() {
    const total = allEmails.length;
    const high = allEmails.filter(e => e.priority === 'high').length;
    const medium = allEmails.filter(e => e.priority === 'medium').length;
    const low = allEmails.filter(e => e.priority === 'low').length;

    document.getElementById('totalTasks').textContent = total;
    document.getElementById('highPriority').textContent = high;
    document.getElementById('mediumPriority').textContent = medium;
    document.getElementById('lowPriority').textContent = low;
}

// Render emails to the page
function renderEmails() {
    const emailList = document.getElementById('emailList');
    
    if (filteredEmails.length === 0) {
        emailList.innerHTML = '<div class="no-results">No emails found</div>';
        return;
    }

    emailList.innerHTML = filteredEmails.map(email => {
        const cleanPreview = escapeHtml(email.preview).replace(/\\r/g, '').replace(/\\n/g, ' ');
        return `
        <div class="email-card" data-filename="${email.filename}">
            <div class="email-header">
                <div class="email-subject">${escapeHtml(email.subject)}</div>
                <span class="priority-badge priority-${email.priority}">
                    ${email.priority === 'high' ? '🔴' : email.priority === 'medium' ? '🟡' : '🔵'} 
                    ${email.priority}
                </span>
            </div>
            <div class="email-meta">
                <span class="email-sender">📧 ${escapeHtml(email.sender)}</span>
                <span class="email-date">📅 ${formatDate(email.date)}</span>
            </div>
            <div class="email-preview">${cleanPreview}</div>
        </div>
    `;
    }).join('');
    
    // Add click handlers to email cards
    document.querySelectorAll('.email-card').forEach(card => {
        card.addEventListener('click', function() {
            const filename = this.getAttribute('data-filename');
            openEmail(filename);
        });
    });
}

// Filter emails based on search and priority
function filterEmails(searchTerm, priority) {
    filteredEmails = allEmails.filter(email => {
        const matchesSearch = !searchTerm || 
            email.subject.toLowerCase().includes(searchTerm) ||
            email.sender.toLowerCase().includes(searchTerm) ||
            email.preview.toLowerCase().includes(searchTerm);
        
        const matchesPriority = priority === 'all' || email.priority === priority;
        
        return matchesSearch && matchesPriority;
    });
    
    console.log('Filtered emails:', filteredEmails.length);
    renderEmails();
}

// Open email file
function openEmail(filename) {
    console.log('Opening email:', filename);
    window.open(`../Needs_Action/${filename}`, '_blank');
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    } catch (e) {
        return 'Unknown date';
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initialized');
    
    // Search functionality
    const searchBox = document.getElementById('searchBox');
    if (searchBox) {
        searchBox.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const priority = document.getElementById('filterPriority').value;
            filterEmails(searchTerm, priority);
        });
    }

    // Priority filter
    const filterPriority = document.getElementById('filterPriority');
    if (filterPriority) {
        filterPriority.addEventListener('change', (e) => {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            filterEmails(searchTerm, e.target.value);
        });
    }

    // Refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            document.getElementById('emailList').innerHTML = '<div class="loading">Loading emails...</div>';
            loadEmails();
        });
    }
    
    // Load emails on startup
    loadEmails();
});
