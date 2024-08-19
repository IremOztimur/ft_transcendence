window.onload = function() {
	const canvas = document.getElementById("pong");
	const context = canvas.getContext('2d');

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	const game = new Game(context, canvas.width, canvas.height);
	game.loop();
};
