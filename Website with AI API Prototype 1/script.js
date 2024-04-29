const uploadButton = document.getElementById('upload-button');
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.style.display = 'none';
document.body.appendChild(fileInput);

const readButton = document.getElementById('read-button');

uploadButton.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    const fileName = file.name;
    const fileSize = file.size;
    const fileType = file.type;

    const fileInfo = `Name: ${fileName} | Size: ${fileSize} bytes | Type: ${fileType}`;
    const fileNameElement = document.getElementById('file-name');
    fileNameElement.textContent = fileInfo;
});

readButton.addEventListener('click', () => {
    const fileInput = document.getElementById('pdf-file');
    const file = fileInput.files[0];
    const fileName = file.name;
    const fileSize = file.size;
    const fileType = file.type;

    if (fileType !== 'application/pdf') {
        alert('Please select a PDF file to read.');
        return;
    }

    const fileReader = new FileReader();
    fileReader.onload = async () => {
        const arrayBuffer = fileReader.result;
        const pdfDoc = await PDFDocument.load(arrayBuffer);
        const pages = pdfDoc.getPages();
        let text = "";
        pages.forEach((page) => {
            const content = page.getContent();
            content.forEach((item) => {
                text += item.toString() + " ";
            });
        });

        const pdfContentElement = document.getElementById('pdf-content');
        pdfContentElement.textContent = text;
        pdfContentElement.style.display = 'block';
    };
    fileReader.readAsArrayBuffer(file);
});