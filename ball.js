class Ball {
	constructor(pos, velocity, radius) {
		this.pos = pos;
		this.velocity = velocity;
		this.radius = radius;
	}

	update() {
		this.pos.x += this.velocity.x;
		this.pos.y += this.velocity.y;
	}

	draw(context) {
		context.beginPath();
		context.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI * 2);
		context.stroke();
	}
}
