window.onload = function() {
	const canvas = document.getElementById("pong");
	const context = canvas.getContext('2d');

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	const keysPressed = [];

	window.addEventListener('keydown', function(event)
	{
		keysPressed[event.keyCode] = true;
	});

	window.addEventListener('keyup', function(event)
	{
		keysPressed[event.keyCode] = false;
	});

	const game = new Game(context, canvas.width, canvas.height);

	game.loop(keysPressed);
};
