// Copyright : Unknownpgr (unknownpgr@gmail.com)

class Vec2D {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  add(a) {
    return new Vec2D(this.x + a.x, this.y + a.y);
  }

  sub(a) {
    return new Vec2D(this.x - a.x, this.y - a.y);
  }

  mul(a) {
    return new Vec2D(this.x * a, this.y * a);
  }

  div(a) {
    return new Vec2D(this.x / a, this.y / a);
  }

  dot(a) {
    return this.x * a.x + this.y * a.y;
  }

  crs(a) {
    return this.x * a.y - this.y * a.x;
  }

  rot(t) {
    return new Vec2D(this.x * Math.cos(t) - this.y * Math.sin(t), this.x * Math.sin(t) + this.y * Math.cos(t));
  }

  len() {
    return Math.sqrt(this.dot(this));
  }

  norm() {
    return this.div(this.len());
  }

  clone() {
    return new Vec2D(this.x, this.y);
  }
}

export default Vec2D;