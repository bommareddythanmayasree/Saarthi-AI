// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    // Form validation and submission
    const form = document.getElementById('studentForm');
    
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
        
        // Handle pill-style checkboxes
        document.querySelectorAll('.pill-label input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    this.parentElement.classList.add('active');
                } else {
                    this.parentElement.classList.remove('active');
                }
            });
        });
        
        // Handle step navigation
        const nextBtn = document.getElementById('nextBtn');
        const backBtn = document.getElementById('backBtn');
        const submitBtn = document.getElementById('submitBtn');
        
        if (nextBtn) {
            nextBtn.addEventListener('click', goToStep2);
        }
        
        if (backBtn) {
            backBtn.addEventListener('click', goToStep1);
        }
    }
});

function goToStep2() {
    // Validate Step 1 fields
    const step1Errors = validateStep1();
    
    if (step1Errors.length > 0) {
        displayErrors(step1Errors);
        return;
    }
    
    // Clear errors
    clearErrors();
    
    // Hide Step 1, Show Step 2
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'block';
    
    // Update buttons
    document.getElementById('nextBtn').style.display = 'none';
    document.getElementById('backBtn').style.display = 'inline-block';
    document.getElementById('submitBtn').style.display = 'inline-block';
    
    // Update header - keep same title, just update subtitle
    document.getElementById('formSubtitle').textContent = 'Help us understand your context to find the best opportunities tailored for you.';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goToStep1() {
    // Hide Step 2, Show Step 1
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step1').style.display = 'block';
    
    // Update buttons
    document.getElementById('nextBtn').style.display = 'inline-block';
    document.getElementById('backBtn').style.display = 'none';
    document.getElementById('submitBtn').style.display = 'none';
    
    // Update header - restore original subtitle
    document.getElementById('formSubtitle').textContent = 'Fill in your details to discover opportunities you might be missing.';
    
    // Clear errors
    clearErrors();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function validateStep1() {
    const errors = [];
    const formData = collectFormData();
    
    if (!formData.name || formData.name.trim() === '') {
        errors.push('Name is required');
    }
    
    if (!formData.age || formData.age <= 0) {
        errors.push('Valid age is required');
    }
    
    if (formData.age && (formData.age < 1 || formData.age > 150)) {
        errors.push('Age must be between 1 and 150');
    }
    
    if (!formData.education_level) {
        errors.push('Education level is required');
    }
    
    if (!formData.degree || formData.degree.trim() === '') {
        errors.push('Degree is required');
    }
    
    if (!formData.field_of_study || formData.field_of_study.trim() === '') {
        errors.push('Field of study is required');
    }
    
    if (!formData.year_of_study || formData.year_of_study <= 0) {
        errors.push('Valid year of study is required');
    }
    
    if (!formData.institution_type) {
        errors.push('Institution type is required');
    }
    
    return errors;
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Clear previous errors
    clearErrors();
    
    // Validate form
    const formData = collectFormData();
    const validationErrors = validateForm(formData);
    
    if (validationErrors.length > 0) {
        displayErrors(validationErrors);
        return;
    }
    
    // Show loading overlay
    showLoading();
    
    try {
        // Submit to API
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Store results in sessionStorage
            sessionStorage.setItem('saarthiResults', JSON.stringify(result));
            
            // Redirect to results page
            window.location.href = '/results';
        } else {
            hideLoading();
            
            // Display server-side errors
            const errors = [];
            
            if (result.error) {
                errors.push(result.error);
            }
            
            if (result.missing_fields) {
                result.missing_fields.forEach(field => {
                    errors.push(`Missing required field: ${field}`);
                });
            }
            
            if (result.invalid_fields) {
                result.invalid_fields.forEach(field => {
                    errors.push(`Invalid field: ${field}`);
                });
            }
            
            displayErrors(errors);
        }
    } catch (error) {
        hideLoading();
        displayErrors(['An error occurred while submitting the form. Please try again.']);
        console.error('Submission error:', error);
    }
}

function collectFormData() {
    const form = document.getElementById('studentForm');
    const formData = new FormData(form);
    
    const data = {
        name: formData.get('name'),
        age: formData.get('age'),
        gender: formData.get('gender'),
        education_level: formData.get('education_level'),
        degree: formData.get('degree'),
        field_of_study: formData.get('field_of_study'),
        year_of_study: formData.get('year_of_study'),
        institution_type: formData.get('institution_type'),
        background_indicators: formData.getAll('background_indicators'),
        opportunity_goals: formData.getAll('opportunity_goals'),
        missed_opportunities_before: formData.get('missed_opportunities_before'),
        additional_context: formData.get('additional_context')
    };
    
    return data;
}

function validateForm(data) {
    const errors = [];
    
    // Required field validation
    if (!data.name || data.name.trim() === '') {
        errors.push('Name is required');
    }
    
    if (!data.age || data.age <= 0) {
        errors.push('Valid age is required');
    }
    
    if (data.age && (data.age < 1 || data.age > 150)) {
        errors.push('Age must be between 1 and 150');
    }
    
    if (!data.education_level) {
        errors.push('Education level is required');
    }
    
    if (!data.degree || data.degree.trim() === '') {
        errors.push('Degree is required');
    }
    
    if (!data.field_of_study || data.field_of_study.trim() === '') {
        errors.push('Field of study is required');
    }
    
    if (!data.year_of_study || data.year_of_study <= 0) {
        errors.push('Valid year of study is required');
    }
    
    if (data.year_of_study && (data.year_of_study < 1 || data.year_of_study > 10)) {
        errors.push('Year of study must be between 1 and 10');
    }
    
    if (!data.institution_type) {
        errors.push('Institution type is required');
    }
    
    // Background indicators are optional - no validation needed
    
    if (!data.opportunity_goals || data.opportunity_goals.length === 0) {
        errors.push('At least one opportunity goal is required');
        highlightFieldError('opportunity_goals_error', 'Please select at least one option');
    }
    
    if (!data.missed_opportunities_before) {
        errors.push('Please indicate if you have missed opportunities before');
    }
    
    return errors;
}

function displayErrors(errors) {
    const errorContainer = document.getElementById('errorContainer');
    const errorList = document.getElementById('errorList');
    
    errorList.innerHTML = '';
    
    errors.forEach(error => {
        const li = document.createElement('li');
        li.textContent = error;
        errorList.appendChild(li);
    });
    
    errorContainer.style.display = 'block';
    
    // Scroll to error container
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function clearErrors() {
    const errorContainer = document.getElementById('errorContainer');
    errorContainer.style.display = 'none';
    
    // Clear field-specific errors
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
    });
}

function highlightFieldError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
    }
}

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'flex';
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'none';
}
