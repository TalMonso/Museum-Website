let canvas, ctx;
let baseImage = new Image();

//initialize canvas and load image
document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById('editorCanvas');
    ctx = canvas.getContext('2d');
    
    const imgPath = document.getElementById('baseImageSrc').value;
    
    baseImage.crossOrigin = "anonymous";
    baseImage.src = imgPath;

    baseImage.onload = function() {
        const maxWidth = 1024; 
        const aspectRatio = baseImage.width / baseImage.height;
        canvas.width = maxWidth;
        canvas.height = maxWidth / aspectRatio;
        
        resetCanvas();
    };
    
    baseImage.onerror = function() {
        console.error("Failed to load image at:", imgPath);
        alert("Error loading artwork.");
    };

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
});


//function to reset canvas to base image
function resetCanvas() {
    if (baseImage.complete) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(baseImage, 0, 0, canvas.width, canvas.height);
    }
}

//function to apply filters
function applyFilter(filterType) {
    resetCanvas(); 

    let filterString = "none";

    switch(filterType) {
        case 'none':
            filterString = "none";
            break;
            
        case 'noir':
            filterString = "grayscale(100%) contrast(120%) brightness(90%)";
            break;
            
        case 'vintage':
            filterString = "sepia(50%) saturate(150%) contrast(90%) brightness(110%) hue-rotate(-10deg)";
            break;
            
        case 'drama':
            filterString = "contrast(140%) saturate(120%) sepia(30%) brightness(85%)";
            break;
            
        case 'cinematic':
            filterString = "contrast(110%) brightness(95%) saturate(110%) hue-rotate(15deg)";
            break;

        case 'cyber':
            filterString = "saturate(250%) contrast(130%) brightness(110%) hue-rotate(-20deg)";
            break;

        case 'matte':
            filterString = "contrast(85%) brightness(120%) saturate(80%)";
            break;

        case 'vivid':
            filterString = "saturate(180%) contrast(125%)";
            break;
    }

    canvas.style.filter = filterString;
}

//function to download the edited canvas
function downloadCanvas() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
    
    tempCtx.filter = canvas.style.filter || 'none';
    
    tempCtx.drawImage(baseImage, 0, 0, canvas.width, canvas.height);
    
    const link = document.createElement('a');
    link.download = 'Regensburg_Museum_Art.png';
    link.href = tempCanvas.toDataURL('image/png', 0.9);
    link.click();
}