document.addEventListener('DOMContentLoaded', function() {
    var uploadButton = document.getElementById('upload-button');
    var fileInput = document.getElementById('file-input');
    var pdfText = document.getElementById('pdf-text');

    uploadButton.addEventListener('click', function() {
        var file = fileInput.files[0];
        if (file) {
            var formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                pdfText.value = data;
            })
            .catch(error => console.error('Error:', error));
        } else {
            console.error('No file selected!');
        }
    });
});