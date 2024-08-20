class Game {
	constructor(context, width, height) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.ball = new Ball(vec2(200, 200), vec2(5, 5), 20);
	}

	update() {
		this.ball.update();
		ballCollisionWithTheEdges(this);
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
