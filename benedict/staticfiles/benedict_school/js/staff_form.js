document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.querySelector('select[name="role"]');
    const teachingFields = document.querySelector('.teaching-fields');
    const nonTeachingFields = document.querySelector('.non-teaching-fields');

    function updateFieldsVisibility() {
        const isTeaching = ['teacher', 'director'].includes(roleSelect.value);
        
        teachingFields.style.display = isTeaching ? 'block' : 'none';
        nonTeachingFields.style.display = isTeaching ? 'none' : 'block';
        
        // Update required fields
        const requiredFields = isTeaching ? 
            ['class_name', 'subjects_handled'] : 
            ['department', 'work_schedule'];
            
        document.querySelectorAll('input, select').forEach(field => {
            if (requiredFields.includes(field.name)) {
                field.required = true;
            }
        });
    }

    if (roleSelect) {
        roleSelect.addEventListener('change', updateFieldsVisibility);
        updateFieldsVisibility(); // Initial state
    }
});