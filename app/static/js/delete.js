document.getElementById('delete-all').addEventListener('click', function confirmDeleteAll() {
    let proceed = confirm('Are you sure you want to delete your account and all your scrollers? This cannot be undone.')
    if (proceed) {
        return true;
    } else {
        return false;
    }
});

document.getElementById('delete-account').addEventListener('click', function confirmDeleteUser() {
    let proceed = confirm('Are you sure you want to delete your account? Your scrollers will remain but you will not be able to edit or delete them later. This cannot be undone.')
    if (proceed) {
        return true;
    } else {
        return false;
    }
});