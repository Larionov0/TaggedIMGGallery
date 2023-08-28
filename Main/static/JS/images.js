function drawImagePartOld(imagePath, object, canvasId, multiplier) {
    // Створюємо нове зображення
    let img = new Image();
    img.src = imagePath;

    // Завантажуємо зображення
    img.onload = function() {
        // Отримуємо канвас з документу за ID
        let canvas = document.getElementById(canvasId);
        let ctx = canvas.getContext('2d');

        // Масштабуємо розмір канвасу до розміру частини зображення, яку ми хочемо вирізати, з урахуванням множника
        let scaleFactorX = img.naturalWidth / 100;
        let scaleFactorY = img.naturalHeight / 100;
        canvas.width = object.width * scaleFactorX * multiplier;
        canvas.height = object.height * scaleFactorY * multiplier;

        // Відображаємо потрібну частину зображення на канвасі
        ctx.drawImage(img, object.start_x * scaleFactorX, object.start_y * scaleFactorY, object.width * scaleFactorX, object.height * scaleFactorY, 0, 0, canvas.width, canvas.height);
    }
}


function drawImagePart2(img, object, canvasId, max_width, max_height) {
    img.onload = function() {
        let canvas = document.getElementById(canvasId);
        let ctx = canvas.getContext('2d');

        let objectWidth = img.naturalWidth * (object.width / 100);
        let objectHeight = img.naturalHeight * (object.height / 100);

        let widthRatio = objectWidth / max_width;
        let heightRatio = objectHeight / max_height;
        
        let canvasWidth, canvasHeight;

        if (widthRatio > heightRatio) {
            canvasWidth = max_width;
            canvasHeight = objectHeight / widthRatio;
        } else {
            canvasHeight = max_height;
            canvasWidth = objectWidth / heightRatio;
        }

        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        


        ctx.drawImage(
            img, 
            object.start_x * img.naturalWidth / 100, 
            object.start_y * img.naturalHeight / 100, 
            objectWidth, 
            objectHeight, 
            0, 
            0, 
            canvas.width, 
            canvas.height
        );
    };
}

function drawImagePart(img, rect, canvasId, max_width, max_height) {
    // створюємо об'єкт Image і встановлюємо джерело
    const image = new Image();
    image.src = img.src;

    image.onload = () => {
        // розраховуємо реальні розміри вирізаного зображення в пікселях
        const cutWidth = image.naturalWidth * (rect.width / 100);
        const cutHeight = image.naturalHeight * (rect.height / 100);

        // розраховуємо розташування вирізаного зображення в пікселях
        const startX = image.naturalWidth * (rect.start_x / 100);
        const startY = image.naturalHeight * (rect.start_y / 100);

        // розраховуємо пропорційні розміри для максимальної ширини та висоти
        let scaleWidth = max_width;
        let scaleHeight = cutHeight * (max_width / cutWidth);

        // перевіряємо, чи не перевищує висота максимальне обмеження
        if (scaleHeight > max_height) {
            scaleWidth = cutWidth * (max_height / cutHeight);
            scaleHeight = max_height;
        }

        // отримуємо доступ до canvas і встановлюємо розміри
        const canvas = document.getElementById(canvasId);
        const context = canvas.getContext('2d');
        canvas.width = scaleWidth;
        canvas.height = scaleHeight;

        console.log(scaleWidth, scaleHeight);

        // малюємо вирізане зображення на canvas
        context.drawImage(image, startX, startY, cutWidth, cutHeight, 0, 0, scaleWidth, scaleHeight);

        canvas.style.width = scaleWidth + 'px';
        canvas.style.height = scaleHeight + 'px';
    };
}


function create_canvas_animation(canvasId, x1=0, y1=0, x2=60, y2=240, duration=400, scaleStart=0.2, scaleEnd=1.0){
    let canvas = document.getElementById(canvasId);
    let startTime = null;

    function animateCanvas(currentTime) {
        if (startTime === null) startTime = currentTime;
        let elapsed = currentTime - startTime;
        
        if (elapsed < duration) {
            let t = elapsed / duration; // нормалізуємо час

            // позиція в кожному кадрі з прискоренням в центрі
            let currentX = x1 + (x2 - x1) * (t * t);
            let currentY = y1 + (y2 - y1) * (t * t);

            // зменшуємо та збільшуємо розмір канвасу
            let currentScale = scaleStart + (scaleEnd - scaleStart) * t;

            // встановлюємо нову позицію та масштаб
            canvas.style.left = currentX + "%";
            canvas.style.top = currentY + "px";
            canvas.style.transform = "scale(" + currentScale + ")";

            // рекурсивно викликаємо animateCanvas
            requestAnimationFrame(animateCanvas);
        } else {
            // коли анімація закінчена, встановлюємо точну кінцеву позицію та розмір
            canvas.style.left = x2 + "%";
            canvas.style.top = y2 + "px";
            canvas.style.transform = "scale(" + scaleEnd + ")";
        }
    }

    // починаємо анімацію
    requestAnimationFrame(animateCanvas);
}


function drawImageParts(){
    let img = document.getElementById('clickableImage');

    let image_part_place = document.querySelector('.image_part_place');
    // get cur canvas width and height
    let maxWidth = image_part_place.clientWidth;
    let maxHeight = image_part_place.clientHeight;
    

    var new_canvases = []
    var i_ = 1;
    for (let place of document.querySelectorAll('.image_part_place')) {
        place.innerHTML = '';
        let new_canvas = document.createElement('canvas');
        new_canvas.id = 'canvas' + i_;
        place.appendChild(new_canvas);
        new_canvases.push(new_canvas);
        i_ ++
    }

    new_canvases[0].style.left = canvas1_position.x_pct + "%";
    new_canvases[0].style.top = canvas1_position.y_px + "px";
    new_canvases[1].style.left = canvas2_position.x_pct + "%";
    new_canvases[1].style.top = canvas2_position.y_px + "px";
    new_canvases[2].style.left = canvas3_position.x_pct + "%";
    new_canvases[2].style.top = canvas3_position.y_px + "px";

    var i = 0
    for (imagePart of imageParts) {
        i++
        if (i > 3) break
        drawImagePart(img, imagePart, 'canvas' + i, maxWidth, maxHeight)

        let canvas = document.getElementById('canvas' + i);
        canvas.addEventListener('click', function() {
        console.log('click')
        })
        // popup text
//        canvas.title = imagePart.tags.join(', ')

        console.log(`Adding event listeners to canvas ${i}`);

        (function(i, canvas, imagePart) {
            canvas.addEventListener('mouseover', () => {
                console.log('mouseover');
                activeCanvas = canvas;
                activeCanvasNumber = i;
    
                canvas.style.zIndex = 1;

                temporaryAlert(imagePart.tags.join(', '), 1000)
            
                drawImagePart(img, imagePart, 'canvas' + i, maxWidth * 1.8, maxHeight * 1.8);
            });

            canvas.addEventListener('mouseout', function() {
                console.log('mouseout')
                for (let other_canvas of document.querySelectorAll('.image_part_place canvas')) {
                    other_canvas.style.zIndex = 0;
                }
                activeCanvas = null;
                activeCanvasNumber = null;
    
                drawImagePart(img, imagePart, 'canvas' + i, maxWidth, maxHeight)
            });

            canvas.addEventListener('contextmenu', function(event) { // rigth click = delete
                console.log('right click')
                event.preventDefault();
                imageParts.splice(i - 1, 1);
                activeCanvas = null;
                activeCanvasNumber = null;
                drawImageParts();
            })   
        })(i, canvas, imagePart);
    }
}


var img = document.querySelector('#clickableImage');
var rect = {}; // ми визначимо цей об'єкт під час mousedown

document.addEventListener('mousedown', function(e) {
    let imgRect = img.getBoundingClientRect();
    let scaleX = img.naturalWidth / imgRect.width;
    let scaleY = img.naturalHeight / imgRect.height;
    let scale = Math.max(scaleX, scaleY);
    let displayedWidth = img.naturalWidth / scale;
    let displayedHeight = img.naturalHeight / scale;

    let offsetLeft = (imgRect.width - displayedWidth) / 2;
    let offsetTop = (imgRect.height - displayedHeight) / 2;

    rect.start_x = (((e.clientX - imgRect.left - offsetLeft) / displayedWidth) * 100);
    rect.start_y = (((e.clientY - imgRect.top - offsetTop) / displayedHeight) * 100);
});

img.addEventListener('mouseup', function(e) {
    let imgRect = img.getBoundingClientRect();
    let scaleX = img.naturalWidth / imgRect.width;
    let scaleY = img.naturalHeight / imgRect.height;
    let scale = Math.max(scaleX, scaleY);
    let displayedWidth = img.naturalWidth / scale;
    let displayedHeight = img.naturalHeight / scale;

    let offsetLeft = (imgRect.width - displayedWidth) / 2;
    let offsetTop = (imgRect.height - displayedHeight) / 2;

    rect.width = (((e.clientX - imgRect.left - offsetLeft) / displayedWidth) * 100) - rect.start_x;
    rect.height = (((e.clientY - imgRect.top - offsetTop) / displayedHeight) * 100) - rect.start_y;

    rect.name = "custom";

    // Перевіряємо, чи лежить прямокутник в межах зображення
    if (rect.start_x >= 0 && rect.start_y >= 0 && rect.start_x + rect.width <= 100 && rect.start_y + rect.height <= 100) {
        // Додаємо прямокутник до списку
        imageParts.push({...rect, tags: []}); // створюємо новий об'єкт, щоб не зберігати посилання на оригінальний
        drawImageParts()
    } else {
        console.log('Selected rectangle is out of image bounds');
    }
});



