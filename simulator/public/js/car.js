class ServoVar {
    constructor(value, speed) {
        this.speed = speed;
        this.destValue = value;
        this.curValue = value;
    }

    set = (value) => {
        this.destValue = value;
    };

    update = (deltaTime) => {
        if (this.destValue < this.curValue) {
            this.curValue -= Math.min(this.curValue - this.destValue, this.speed * deltaTime);
        } else {
            this.curValue += Math.min(this.destValue - this.curValue, this.speed * deltaTime);
        }
    };
}

class Car {
    constructor(camBox, cam, x, y, heading) {
        this.camBox = camBox;
        this.cam = cam;

        // This values can change 360 degree per second
        this.camAngle = new ServoVar(0, Math.PI * 2);
        this.steering = new ServoVar(0, Math.PI * 2);

        // Maximum acceleration = 6m/s^2
        this.speed = new ServoVar(0, 6);

        this.heading = heading;
        this.x = x;
        this.y = y;
    }

    update = (deltaTime) => {
        this.camAngle.update(deltaTime);
        this.steering.update(deltaTime);
        this.speed.update(deltaTime);

        this.heading -= this.speed.curValue * Math.tan(this.steering.curValue) * deltaTime;
        this.x += this.speed.curValue * Math.cos(this.heading);
        this.y += this.speed.curValue * Math.sin(this.heading);

        this.camBox.position.set(this.x, 0, -this.y);
        this.camBox.rotation.y = this.heading - Math.PI / 2;
        this.cam.rotation.x = this.camAngle.curValue;
    };
}

export default Car;
