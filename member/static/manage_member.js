document.addEventListener('DOMContentLoaded', () => {
    const editButtons = document.querySelectorAll('.edit-btn');
    const deleteButtons = document.querySelectorAll('.delete-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Edit feature not implemented yet.');
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Delete feature not implemented yet.');
        });
    });
});
