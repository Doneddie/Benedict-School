// Select the navbar toggle button and the navbar container
const navbarToggle = document.querySelector('.navbar-toggle');
const navbar = document.querySelector('.navbar');

// Add event listener to toggle the navbar visibility
navbarToggle.addEventListener('click', () => {
    navbar.classList.toggle('open');
});

function initMap() {
    const schoolLocation = {
        lat: 0.313575,  // actual latitude
        lng: 32.506578   // actual longitude
    };

    const map = new google.maps.Map(document.getElementById('school-map'), {
        center: schoolLocation,
        zoom: 15,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
        zoomControl: true,
        styles: [
            {
                "featureType": "poi.school",
                "elementType": "all",
                "stylers": [
                    { "visibility": "on" },
                    { "color": "#3498db" }
                ]
            }
        ]
    });

    const marker = new google.maps.Marker({
        position: schoolLocation,
        map: map,
        title: 'Benedict School',
        animation: google.maps.Animation.DROP
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="padding: 10px;">
                <h3 style="margin: 0 0 5px 0; color: #2c3e50;">Benedict School</h3>
                <p style="margin: 0; color: #7f8c8d;">Bulenga-Kikaaya, Wakiso</p>
                <p style="margin: 5px 0 0 0; color: #7f8c8d;">Phone: +256784499434</p>
            </div>
        `
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });
}

// Initialize the map when the page loads
window.addEventListener('load', initMap);


document.addEventListener("DOMContentLoaded", function () {
    const imagesContainer = document.getElementById("gallery-container");
    const images = imagesContainer.querySelectorAll(".gallery-card");
    let currentIndex = 0;

    // Function to hide all images
    function hideAllImages() {
        images.forEach(image => {
            image.style.display = "none";
        });
    }

    // Function to show the next image
    function showNextImage() {
        hideAllImages();
        images[currentIndex].style.display = "block";
        currentIndex = (currentIndex + 1) % images.length; // Loop back to the first image when we reach the end
    }

    // Initially show the first image
    showNextImage();

    // Set interval to show the next image every 5 seconds
    setInterval(showNextImage, 5000);  // Change images every 5 seconds (5000 milliseconds)
});

