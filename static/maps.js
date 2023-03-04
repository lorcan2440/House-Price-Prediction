function initMap() {
    var myLatLng = { lat: 1.3737186, lng: 103.8229259 };
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 10.5
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        animation: google.maps.Animation.DROP // Add animation to the marker when it is dropped
    });

    marker.addListener('click', function () {
        marker.setAnimation(google.maps.Animation.BOUNCE); // Add animation to the marker when it is clicked
    });

    map.addListener('click', function (event) {

        // update the entry fields
        document.getElementById('lat').value = event.latLng.lat();
        document.getElementById('long').value = event.latLng.lng();

        // move marker to the clicked location
        marker.setPosition(event.latLng);

    });

    const latInput = document.getElementById('lat');
    const longInput = document.getElementById('long');

    latInput.addEventListener('blur', function() {
        const latitude = parseFloat(this.value);
        if (!isNaN(latitude)) {
            dropMarker(latitude, parseFloat(longInput.value));
        }
    });

    longInput.addEventListener('blur', function() {
        const longitude = parseFloat(this.value);
        if (!isNaN(longitude)) {
            dropMarker(parseFloat(latInput.value), longitude);
        }
    });

    function dropMarker(latitude, longitude) {
        // drop the marker at the specified latitude and longitude
        var marker = new google.maps.Marker({
            position: { lat: latitude, lng: longitude },
            map: map,
            animation: google.maps.Animation.DROP // Add animation to the marker when it is dropped
        });
        
        map.setCenter({ lat: latitude, lng: longitude });
    }
}
