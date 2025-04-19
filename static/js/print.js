/**
 * JavaScript for handling print functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Print button functionality
    const printBtn = document.getElementById('printBtn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            printApplication();
        });
    }
});

/**
 * Function to handle application printing
 */
function printApplication() {
    // Hide elements that shouldn't be printed
    const elementsToHide = document.querySelectorAll('.no-print');
    elementsToHide.forEach(function(element) {
        element.setAttribute('data-original-display', element.style.display);
        element.style.display = 'none';
    });
    
    // Print the page
    window.print();
    
    // Restore the hidden elements
    elementsToHide.forEach(function(element) {
        element.style.display = element.getAttribute('data-original-display') || '';
    });
    
    return false;
}
