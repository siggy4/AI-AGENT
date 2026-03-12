// Modal functions
function openAddPartnershipModal() {
    document.getElementById('addPartnershipModal').classList.remove('hidden');
}

function closeAddPartnershipModal() {
    document.getElementById('addPartnershipModal').classList.add('hidden');
}

// Checkbox functions
function toggleSelectAll() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.partnership-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
    
    updateDeleteButton();
}

function updateDeleteButton() {
    const checkboxes = document.querySelectorAll('.partnership-checkbox:checked');
    const deleteBtn = document.getElementById('deleteBtn');
    
    if (checkboxes.length > 0) {
        deleteBtn.disabled = false;
    } else {
        deleteBtn.disabled = true;
    }
}

function deleteSelected() {
    const checkboxes = document.querySelectorAll('.partnership-checkbox:checked');
    
    if (checkboxes.length === 0) {
        alert('Please select at least one partnership to delete.');
        return;
    }
    
    const partnershipIds = Array.from(checkboxes).map(cb => cb.value);
    
    if (confirm(`Are you sure you want to delete ${partnershipIds.length} partnership(s)?`)) {
        // Create form to submit deletion
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/partnerships/delete/';
        
        // Add CSRF token
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = getCookie('csrftoken');
        form.appendChild(csrfInput);
        
        // Add partnership IDs
        partnershipIds.forEach(id => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'partnership_ids';
            input.value = id;
            form.appendChild(input);
        });
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toggle details dropdown
function toggleDetails(partnershipId) {
    const detailsRow = document.getElementById(`details-${partnershipId}`);
    const arrow = document.getElementById(`arrow-${partnershipId}`);
    
    if (detailsRow.classList.contains('hidden')) {
        detailsRow.classList.remove('hidden');
        arrow.classList.add('rotate-180');
    } else {
        detailsRow.classList.add('hidden');
        arrow.classList.remove('rotate-180');
    }
}

function toggleFeedback(feedbackId) {
    const feedbackDiv = document.getElementById(feedbackId);
    
    if (feedbackDiv.classList.contains('hidden')) {
        feedbackDiv.classList.remove('hidden');
    } else {
        feedbackDiv.classList.add('hidden');
    }
}

function saveDetails(partnershipId) {
    const meetingDate = document.getElementById(`meeting-date-${partnershipId}`).value;
    const followupDate = document.getElementById(`followup-date-${partnershipId}`).value;
    const contactMethod = document.getElementById(`contact-method-${partnershipId}`).value;
    const companyEmail = document.getElementById(`company-email-${partnershipId}`).value;
    const companyPhone = document.getElementById(`company-phone-${partnershipId}`).value;
    const positiveFeedback = document.getElementById(`positive-feedback-${partnershipId}`).value;
    const negativeFeedback = document.getElementById(`negative-feedback-${partnershipId}`).value;
    const meetingType = document.getElementById(`meeting-type-${partnershipId}`).value;
    
    console.log('Saving details for partnership', partnershipId, {
        meetingDate,
        followupDate,
        contactMethod,
        companyEmail,
        companyPhone,
        positiveFeedback,
        negativeFeedback,
        meetingType
    });
    
    alert('Details saved successfully!');
}

// File upload functions
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('border-blue-500', 'bg-blue-50');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
}

function handleDrop(event, partnershipId) {
    event.preventDefault();
    event.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
    
    const files = event.dataTransfer.files;
    handleFiles(files, partnershipId);
}

function handleFileSelect(event, partnershipId) {
    const files = event.target.files;
    handleFiles(files, partnershipId);
}

function handleFiles(files, partnershipId) {
    const fileList = document.getElementById(`file-list-${partnershipId}`);
    const dropZone = document.getElementById(`drop-zone-${partnershipId}`);
    
    // Show file list container
    fileList.classList.remove('hidden');
    
    // Process each file
    Array.from(files).forEach(file => {
        if (file.type === 'application/pdf') {
            addFileToList(file, partnershipId);
        } else {
            alert(`${file.name} is not a PDF file. Please upload only PDF files.`);
        }
    });
}

function addFileToList(file, partnershipId) {
    const pdfList = document.getElementById(`pdf-list-${partnershipId}`);
    
    // Remove "No PDFs uploaded yet" message if it exists
    if (pdfList.querySelector('.text-gray-500.italic')) {
        pdfList.innerHTML = '';
    }
    
    const fileItem = document.createElement('div');
    fileItem.className = 'flex items-center justify-between p-2 bg-white rounded border border-gray-200';
    
    fileItem.innerHTML = `
        <div class="flex items-center gap-2">
            <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/>
            </svg>
            <span class="text-xs text-gray-700 truncate flex-1">${file.name}</span>
            <span class="text-xs text-gray-500">(${formatFileSize(file.size)})</span>
        </div>
        <button onclick="removeFile(this, '${file.name}', '${partnershipId}')" class="text-red-500 hover:text-red-700 ml-2">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    `;
    
    pdfList.appendChild(fileItem);
}

function removeFile(button, fileName, partnershipId) {
    button.parentElement.remove();
    console.log('Removed file:', fileName);
    
    // Check if PDF list is empty and show message
    const pdfList = document.getElementById(`pdf-list-${partnershipId}`);
    if (pdfList.children.length === 0) {
        pdfList.innerHTML = '<p class="text-xs text-gray-500 italic">No PDFs uploaded yet</p>';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Make drop zone clickable
document.addEventListener('DOMContentLoaded', function() {
    // This will be called for each partnership when the page loads
    const dropZones = document.querySelectorAll('[id^="drop-zone-"]');
    dropZones.forEach(zone => {
        zone.addEventListener('click', function() {
            const partnershipId = this.id.replace('drop-zone-', '');
            document.getElementById(`file-input-${partnershipId}`).click();
        });
    });
});

// Back to Top functionality
window.addEventListener('scroll', function() {
    const backToTopButton = document.getElementById('backToTop');
    if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
});
