const canvas = document.getElementById('map');
const mapView = new harp.MapView({
   canvas,
   theme: "https://unpkg.com/@here/harp-map-theme@latest/resources/berlin_tilezen_night_reduced.json"
});

// center the camera to New York
mapView.lookAt({
  target: new harp.GeoCoordinates(48.92312, 24.71248),
  zoomLevel: 17,
  tilt: 40,
});

const mapControls = new harp.MapControls(mapView);
const ui = new harp.MapControlsUI(mapControls);
canvas.parentElement.appendChild(ui.domElement);

mapView.resize(window.innerWidth, window.innerHeight);
window.onresize = () => mapView.resize(window.innerWidth, window.innerHeight);

const vectorTileDataSource = new harp.VectorTileDataSource({
   authenticationCode: 'R_eJy1bCsrX_R4hoD2d5lSV0Doiqgs4kHMtFKJ8KAKs',
});
mapView.addDataSource(vectorTileDataSource);

//window.addEventListener("click", (evt) => {
//   //Create the three.js cube
//   const geometry = new THREE.BoxGeometry(100, 100, 100);
//   const material = new THREE.MeshStandardMaterial({ color: 0x00ff00fe });
//   const cube = new THREE.Mesh(geometry, material);
//   cube.renderOrder = 100000;
//
//   //Get the position of the click
//   const geoPosition = mapView.getGeoCoordinatesAt(48.92312, 24.71248);
//   cube.anchor = geoPosition;
//
//   //Add object to the map
//   mapView.mapAnchors.add(cube);
//   mapView.update();
//});

function addCar(){
        //Create the three.js cube
        const geometry = new THREE.BoxGeometry(100, 100, 100);
        const material = new THREE.MeshStandardMaterial({ color: 0x00ff00fe });
        const cube = new THREE.Mesh(geometry, material);
        cube.renderOrder = 100000;

        //Get the position of the click
        const geoPosition = mapView.getGeoCoordinatesAt(48.92312, 24.71248);
        cube.anchor = geoPosition;

        //Add object to the map
        mapView.mapAnchors.add(cube);
        mapView.update();

}

addCar()