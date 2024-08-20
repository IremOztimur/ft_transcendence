// Utility function for creating 2D vectors
function vec2(x, y) {
	return { x, y };
}

function ballCollisionWithTheEdges(game) {
	if (game.ball.pos.y + game.ball.radius > game.height || game.ball.pos.y - game.ball.radius <= 0) {
		game.ball.velocity.y *= -1;
	}

	// if (game.ball.pos.x + game.ball.radius > game.width || game.ball.pos.x - game.ball.radius <= 0) {
	// 	game.ball.velocity.x *= -1;
	// }
}

function paddleCollisionWithTheEdges(game) {
	if (game.paddle1.pos.y <= 0)
		game.paddle1.pos.y = 0;

	if (game.paddle1.pos.y + game.paddle1.height >= game.height)
			game.paddle1.pos.y = game.height - game.paddle1.height;
}


function ballCollisionWithThePaddle(game) {
	let dx1 =  Math.abs(game.ball.pos.x - game.paddle1.getCenter().x);
	let dy1 =  Math.abs(game.ball.pos.y - game.paddle1.getCenter().y);
	let dx2 =  Math.abs(game.ball.pos.x - game.paddle2.getCenter().x);
	let dy2 =  Math.abs(game.ball.pos.y - game.paddle2.getCenter().y);

	if (dx1 <= (game.ball.radius + game.paddle1.getHalfWidth()) && dy1 <= (game.ball.radius + game.paddle1.getHalfHeight())){
		game.ball.velocity.x *= -1;
	}
	if (dx2 <= (game.ball.radius + game.paddle2.getHalfWidth()) && dy2 <= (game.ball.radius + game.paddle2.getHalfHeight())){
		game.ball.velocity.x *= -1;
	}

}
