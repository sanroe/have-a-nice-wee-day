document.getElementById('make-your-own').addEventListener('click', function showCustomhaikuForm() {
    document.getElementById("for-custom-haiku").style.display = "block";
});

document.getElementById('pick-ours').addEventListener('click', function hideCustomhaikuForm() {
    document.getElementById("for-custom-haiku").style.display = "none";
});

const textarea = document.querySelector('textarea')
const count = document.getElementById('long-message-count')
textarea.onkeyup = (e) => {
    count.innerHTML = (1000 - e.target.value.length) + "/1000 characters";
};