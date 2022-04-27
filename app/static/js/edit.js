document.getElementById('make-your-own').addEventListener('click', function showCustomhaikuForm() {
    document.getElementById("for-custom-haiku-edit").style.display = "block";
});
document.getElementById('pick-ours').addEventListener('click', function hideCustomhaikuForm() {
    document.getElementById("for-custom-haiku-edit").style.display = "none";
});