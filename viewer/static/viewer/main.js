// variables declared in index.html
// let images = [...];
// let currentIndex = ...;
// let img_base64 = "...";

// Initialize OpenSeadragon
let viewer = OpenSeadragon({
    id: "openseadragon",
    prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/3.1.0/images/",
    tileSources: {
        type: "image",
        url: "data:image/jpeg;base64," + img_base64
    },
    showNavigator: true,
    navigatorPosition: "BOTTOM_RIGHT",
    animationTime: 0.5,
    zoomPerScroll: 1.5
});

// Load JSON data for current image
function loadData() {
    let imgName = images[currentIndex];
    fetch(`/api/data/${imgName}/`)
        .then(res => res.json())
        .then(data => {
            let form = document.getElementById('data-form');
            form.innerHTML = '';
            for (let key in data) {
                let label = document.createElement('label');
                label.innerText = key;
                let input = document.createElement('input');
                input.name = key;
                input.value = data[key];
                form.appendChild(label);
                form.appendChild(input);
            }
        });
}

// Update viewer image dynamically
function updateViewer(newBase64) {
    viewer.open({
        type: "image",
        url: "data:image/jpeg;base64," + newBase64
    });
}

// Save verified data and move to next image
document.getElementById('save-btn').addEventListener('click', () => {
    let form = document.getElementById('data-form');
    let verified_data = {};
    [...form.elements].forEach(el => {
        if(el.name) verified_data[el.name] = el.value;
    });

    let imgName = images[currentIndex];

    fetch('/api/save/', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({image_name: imgName, verified_data: verified_data})
    })
    .then(res => res.json())
    .then(res => {
        if(res.status === 'success'){
            currentIndex++;
            if(currentIndex < images.length){
                // Fetch next image base64 from backend
                fetch(`/api/next_image/${images[currentIndex]}/`)
                    .then(r => r.json())
                    .then(data => {
                        updateViewer(data.img_base64);
                        loadData(); // load next JSON
                    });
            } else {
                alert("All images verified!");
            }
        } else {
            alert("Error saving data: " + res.message);
        }
    });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Load initial JSON data
loadData();
