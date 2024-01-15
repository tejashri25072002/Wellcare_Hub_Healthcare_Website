/*const canvas = document.querySelector('.canvas');
const ctx = canvas.getContext('2d');

const pixelRatio = window.devicePixelRatio || 1;

const snowflakes = [];

class Snowflake {
  constructor() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    
    const maxSize = 3;
    this.size = Math.random() * (maxSize - 1) + 1;
    this.velocity = this.size * 0.35;
    const opacity = this.size / maxSize;
    this.fill = `rgb(255 255 255 / ${opacity})`;
    
    this.windSpeed = (Math.random() - 0.5) * 0.1;
    this.windAngle = Math.random() * Math.PI * 2;
  }
  isOutsideCanvas() {
    return this.y > canvas.height + this.size;
  }
  reset() {
    this.x = Math.random() * canvas.width;
    this.y = -this.size;
  }
  update() {
    this.windAngle += this.windSpeed;
    this.wind = Math.cos(this.windAngle) * 0.5;

    this.x += this.wind;
    this.y += this.velocity;

    if (this.isOutsideCanvas()) {
      this.reset();
    }
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = this.fill;
    ctx.fill();
    ctx.closePath();
  }
}

const createSnowflakes = () => {
  snowflakeCount = Math.floor(window.innerWidth * window.innerHeight / 1400);
  
  for (let i = 0; i < snowflakeCount; i++) {  
    snowflakes.push(new Snowflake());
  }
}

const resizeCanvas = () => {
  const width = window.innerWidth;
  const height = window.innerHeight;
  canvas.width = width * pixelRatio;
  canvas.height = height * pixelRatio;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  ctx.scale(pixelRatio, pixelRatio);
  snowflakes.length = 0;
  createSnowflakes();
};

window.addEventListener('resize', resizeCanvas);

resizeCanvas();

const render = () => {
  requestAnimationFrame(render);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  snowflakes.forEach(snowflake => {
    snowflake.update();
    snowflake.draw();
  });
};

render();

//IIFE
(function () {
	'use strict';
	
	var canvas,ctx;
	var points = [];
	var maxDist = 100;

	function init () {
		//Add on load scripts
		canvas = document.getElementById("canvas");
		ctx = canvas.getContext("2d");
		resizeCanvas();
		generatePoints(700);
		pointFun();
		setInterval(pointFun,25);
		window.addEventListener('resize', resizeCanvas, false);
	}

  //Particle constructor
	function point () {
		this.x = Math.random()*(canvas.width+maxDist)-(maxDist/2);
		this.y = Math.random()*(canvas.height+maxDist)-(maxDist/2);
		this.z = (Math.random()*0.5)+0.5;
		this.vx = ((Math.random()*2)-0.5)*this.z;
		this.vy = ((Math.random()*1.5)+1.5)*this.z;
		this.fill = "rgba(255,255,255,"+((0.5*Math.random())+0.5)+")";
		this.dia = ((Math.random()*2.5)+1.5)*this.z;
		points.push(this);
	}

  //Point generator
	function generatePoints (amount) {
		var temp;
		for (var i = 0; i < amount; i++) {
			temp = new point();
		};
		console.log(points);
	}
	//Point drawer
	function draw (obj) {
		ctx.beginPath();
		ctx.strokeStyle = "transparent";
		ctx.fillStyle = obj.fill;
		ctx.arc(obj.x,obj.y,obj.dia,0,2*Math.PI);
		ctx.closePath();
		ctx.stroke();
		ctx.fill();
	}
//Updates point position values
	function update (obj) {
		obj.x += obj.vx;
		obj.y += obj.vy;
		if (obj.x > canvas.width+(maxDist/2)) {
			obj.x = -(maxDist/2);
		}
		else if (obj.xpos < -(maxDist/2)) {
			obj.x = canvas.width+(maxDist/2);
		}
		if (obj.y > canvas.height+(maxDist/2)) {
			obj.y = -(maxDist/2);
		}
		else if (obj.y < -(maxDist/2)) {
			obj.y = canvas.height+(maxDist/2);
		}
	}
	//
	function pointFun () {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
for (var i = 0; i < points.length; i++) {
			draw(points[i]);
			update(points[i]);
		};
	}

	function resizeCanvas() {
		canvas.width = window.innerWidth;
		canvas.height = window.innerHeight;
		pointFun();
	}

	//Execute when DOM has loaded
	document.addEventListener('DOMContentLoaded',init,false);
})();*/

'use strict'

const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')

let width, height, lastNow
let snowflakes
const maxSnowflakes = 100

function init() {
  snowflakes = []
  resize()
  render(lastNow = performance.now())
}

function render(now) {
  requestAnimationFrame(render)
  
  const elapsed = now - lastNow
  lastNow = now
  
  ctx.clearRect(0, 0, width, height)
  if (snowflakes.length < maxSnowflakes)
    snowflakes.push(new Snowflake())
  
  ctx.fillStyle = ctx.strokeStyle = '#fff'

  snowflakes.forEach(snowflake => snowflake.update(elapsed, now))
}

function pause() {
  cancelAnimationFrame(render)
}
function resume() {
  lastNow = performance.now()
  requestAnimationFrame(render)
}


class Snowflake {
  constructor() {
    this.spawn()
  }
  
  spawn(anyY = false) {
    this.x = rand(0, width)
    this.y = anyY === true
      ? rand(-50, height + 50)
      : rand(-50, -10)
    this.xVel = rand(-.05, .05)
    this.yVel = rand(.02, .1)
    this.angle = rand(0, Math.PI * 2)
    this.angleVel = rand(-.001, .001)
    this.size = rand(7, 12)
    this.sizeOsc = rand(.01, .5)
  }
  
  update(elapsed, now) {
    const xForce = rand(-.001, .001);

    if (Math.abs(this.xVel + xForce) < .075) {
      this.xVel += xForce
    }
    
    this.x += this.xVel * elapsed
    this.y += this.yVel * elapsed
    this.angle += this.xVel * 0.05 * elapsed //this.angleVel * elapsed
    
    if (
      this.y - this.size > height ||
      this.x + this.size < 0 ||
      this.x - this.size > width
    ) {
      this.spawn()
    }
    
    this.render()
  }
  
  render() {
    ctx.save()
    const { x, y, angle, size } = this
    ctx.beginPath()
    ctx.arc(x, y, size * 0.2, 0, Math.PI * 2, false)
    ctx.fill()
    ctx.restore()
  }
}

// Utils
const rand = (min, max) => min + Math.random() * (max - min)

function resize() {
  width = canvas.width = window.innerWidth
  height = canvas.height = window.innerHeight
}

window.addEventListener('resize', resize)
window.addEventListener('blur', pause)
window.addEventListener('focus', resume)
init()