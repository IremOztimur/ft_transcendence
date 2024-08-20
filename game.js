class Game {
	constructor(context, width, height) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.ball = new Ball(vec2(200, 200), vec2(5, 5), 20);
		this.paddle1 = new Paddle(vec2(0, 50), vec2(5, 5), 20, 160);
		this.paddle2 = new Paddle(vec2(width-20, 200), vec2(5, 5), 20, 160);
	}

	update() {
		this.ball.update();
		this.paddle1.update();
		this.paddle2.update();
		ballCollisionWithTheEdges(this);
	}

	render() {
		this.context.clearRect(0, 0, this.width, this.height);
		this.ball.draw(this.context);
		this.paddle1.draw(this.context);
		this.paddle2.draw(this.context);
	}

	loop() {
		this.update();
		this.render();
		requestAnimationFrame(() => this.loop());
	}
}
