document.getElementById("copy-link-button").addEventListener("click", function copyLink() {
    var copyText = document.getElementById("scroller-link");

    copyText.select();
    copyText.setSelectionRange(0, 99999);

    document.execCommand("copy");
});