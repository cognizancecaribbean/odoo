document.addEventListener('DOMContentLoaded', function() {
  // Get the select element and the fields to toggle
  var selectElement = document.getElementById('is_registered');
  var toggleFields = document.querySelectorAll('.business-field-col'); // Container divs to be toggled
  var requireFields = document.querySelectorAll('.business-field'); // Individual fields to toggle required

  // Add an event listener for when the selection changes
  selectElement.addEventListener('change', function() {
    console.log('Select element changed');

    // Loop through all toggleFields (container divs) and show/hide based on the selected value
    toggleFields.forEach(function(fieldContainer) {
      if (selectElement.value === 'registered') {
        fieldContainer.style.display = 'block'; // Show the container div
      } else {
        fieldContainer.style.display = 'none'; // Hide the container div
      }
    });

    // Loop through all requireFields (individual fields) and set the required property based on the selected value
    requireFields.forEach(function(field) {
      if (selectElement.value === 'registered') {
        field.required = true; // Make the field required
      } else {
        field.required = false; // Make the field not required
      }
    });
  });
});

  