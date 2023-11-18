import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

// Create scene, camera and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 2000);

// Set camera position and rotation for top-down view
camera.position.set(0, 3, 0); // Adjust the Y value to set the height of the camera
camera.rotation.set(-Math.PI / 2, 0, 0);

const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setSize(window.innerWidth - 100, window.innerHeight -100);
renderer.setClearColor(0x000000, 0); 
document.body.appendChild(renderer.domElement);

// Add controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 1, 0);

// Get the div element where you want to load the scene
var container = document.getElementById('threejs-container');

// Append the renderer's DOM element to the div
container.appendChild(renderer.domElement);

const loader = new THREE.ObjectLoader();
loader.load('/scenes/scene.json', (object) => {
    // Add the loaded object to the scene
    scene.add(object);
    
    // Access the UR3 object after it's loaded
    var UR3 = scene.getObjectByName("UR3");
    var joint1 = UR3.getObjectByName("Joint_1");
    var joint2 = UR3.getObjectByName("Joint_2");
    var joint3 = UR3.getObjectByName("Joint_3");
    var joint4 = UR3.getObjectByName("Joint_4");
    var joint5 = UR3.getObjectByName("Joint_5");
    var joint6 = UR3.getObjectByName("Joint_6");
    
    var links = [joint1, joint2, joint3, joint4, joint5, joint6];
    var get_data = new EventSource("http://localhost:5000/digital");

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);

        get_data.onmessage = function(event) {
            var jointPositions = JSON.parse(event.data);
            // console.log(jointPositions);
            for (var i = 0; i < links.length; i++) {
                links[i].rotation.y = jointPositions[i];

                // print to modal
                document.getElementById("j" + String(i)).innerHTML = String(Math.floor(jointPositions[i] * (180 / Math.PI))) + "°";
            }
        };
    }

    animate();

}, (xhr) => {
    console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
}, (error) => {
    console.log(error);
});