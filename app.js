(function() {
	var scene = new THREE.Scene();
	var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

	var renderer = new THREE.WebGLRenderer();
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );

	var geometry = new THREE.SphereGeometry(150, 100, 100);
	var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
	var sphere = new THREE.Mesh( geometry, material );
	scene.add( sphere );
	camera.position.z = 5;

	function render() {
		requestAnimationFrame( render );

		sphere.rotation.x += 0.1;
		sphere.rotation.y += 0.1;

		renderer.render( scene, camera );
	}
	render();
})();