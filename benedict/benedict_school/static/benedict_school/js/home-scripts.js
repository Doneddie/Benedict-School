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
            // Add more custom styles as needed
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
