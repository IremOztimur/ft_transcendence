class Game {
	constructor(context, width, height) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.ball = new Ball(vec2(200, 200), vec2(5, 5), 20);
	}

	ballCollisionWithTheEdges() {
		if (this.ball.pos.y + this.ball.radius > this.height || this.ball.pos.y - this.ball.radius <= 0) {
			this.ball.velocity.y *= -1;
		}

		if (this.ball.pos.x + this.ball.radius > this.width || this.ball.pos.x - this.ball.radius <= 0) {
			this.ball.velocity.x *= -1;
		}
	}

	update() {
		this.ball.update();
		this.ballCollisionWithTheEdges();
	}

	render() {
		this.context.clearRect(0, 0, this.width, this.height);
		this.ball.draw(this.context);
	}

	loop() {
		this.update();
		this.render();
		requestAnimationFrame(() => this.loop());
	}
}
