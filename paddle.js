class Paddle {
	constructor(pos, velocity, width, height) {
		this.pos = pos;
		this.velocity = velocity;
		this.width = width;
		this.height = height;
	}

	update() {}

	draw(context) {
		context.fillStyle = "#33ff00";
		context.fillRect(this.pos.x, this.pos.y, this.width, this.height);
	}
}
