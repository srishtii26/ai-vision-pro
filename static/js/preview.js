function previewImage(event) {
    const preview = document.getElementById("preview");

    preview.src = URL.createObjectURL(event.target.files[0]);
    preview.style.display = "block";
}

const dropArea = document.querySelector(".upload-box");

["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.style.borderColor = "#ffffff";
        dropArea.style.transform = "scale(1.03)";
    });
});

["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.style.borderColor = "rgba(255,255,255,0.5)";
        dropArea.style.transform = "scale(1)";
    });
});

dropArea.addEventListener("drop", e => {

    const fileInput = document.querySelector('input[type="file"]');

    fileInput.files = e.dataTransfer.files;

    previewImage({
        target: {
            files: e.dataTransfer.files
        }
    });

});