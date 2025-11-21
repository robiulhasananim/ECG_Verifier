function loadImage() {
    let img = document.getElementById('ecg-img');
    let imgName = images[currentIndex];
    img.src = '/media/ecg_images/' + imgName;

    fetch(`/api/data/${imgName}/`)
    .then(res => res.json())
    .then(data => {
        let form = document.getElementById('data-form');
        form.innerHTML = '';
        for (let key in data) {
            form.innerHTML += `<label>${key}</label><input name="${key}" value="${data[key]}"/><br/>`;
        }
    });
}

function saveData() {
    let form = document.getElementById('data-form');
    let data = {};
    [...form.elements].forEach(el => {
        if (el.name) data[el.name] = el.value;
    });

    fetch('/api/save/', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({image_name: images[currentIndex], verified_data: data})
    }).then(res => res.json())
    .then(res => {
        if(res.status === 'success'){
            currentIndex++;
            if(currentIndex < images.length) loadImage();
            else alert("All images verified!");
        }
    });
}

// Zoom functionality
const img = document.getElementById('ecg-img');
img.addEventListener('wheel', (e)=>{
    e.preventDefault();
    let scale = e.deltaY < 0 ? 1.1 : 0.9;
    img.style.width = (img.width * scale) + 'px';
});

loadImage();
