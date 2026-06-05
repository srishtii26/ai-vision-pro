const fileInput = document.querySelector('input[type="file"]');

fileInput.addEventListener("change", function(){

    const file = this.files[0];

    if(file){

        const size = (file.size / (1024 * 1024)).toFixed(2);

        document.getElementById("fileInfo").innerHTML =
            `📄 ${file.name}<br>📦 ${size} MB`;
    }

});