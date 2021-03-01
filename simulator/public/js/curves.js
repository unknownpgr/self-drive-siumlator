import Vec2D from './vec2d.js';

// Get path function from segments
function getPathFunction(segments) {
  /**
   * 'segments' is a list of tuples <radius, anlge(length)>.
   * If radius <= 0, then the given segment is regarded as a line with given length.
   * Else, the given segment is regarded as a arc with given radius and angle.
   * 
   * pathFunctions is a list of spline functions.
   */

  let angle = 0;
  let pos1 = new Vec2D(0, 0);
  let pathFunctions = [];
  let segmentLengthes = [0];
  let totalLength = 0;

  segments.forEach(segment => {
    const a = angle; // Copy variable so that it would be immutable.
    const p = pos1.clone();
    if (segment[0] <= 0) {
      // Line segment
      pathFunctions.push(t => new Vec2D(Math.cos(a), Math.sin(a)).mul(segment[1] * t).add(p));
      totalLength += segment[1];
    } else {
      // Curve segment
      pathFunctions.push(t => new Vec2D(Math.cos(segment[1] * t) - 1, Math.sin(segment[1] * t)).rot(a - Math.sign(segment[1]) * Math.PI / 2).mul(segment[0]).add(p));
      totalLength += Math.abs(segment[0] * segment[1]);
      angle += segment[1];
    }
    pos1 = pathFunctions[pathFunctions.length - 1](1);
    segmentLengthes.push(totalLength);
  });

  return x => {
    /**
     * `x` is position in curve. The range of x must be in [0,1].
     * t is global position in curve.
     */
    if (x < 0) x = 0;
    if (x > 1) x = 1;
    let t = x * totalLength;
    let i;
    // If given t is in range of [0,1]
    for (i = 0; i < pathFunctions.length; i++) {
      if (segmentLengthes[i] <= t && t <= segmentLengthes[i + 1]) {
        let sgementT = (t - segmentLengthes[i]) / (segmentLengthes[i + 1] - segmentLengthes[i]);
        return pathFunctions[i](sgementT);
      }
    }
  };
}


function createThickLine(points, thickness) {
  const EPSILON = 0.0001;
  const t = thickness / 2;
  const n = points.length;
  const R = Math.PI / 2;

  let segments = [], left = [], right = [];

  for (let i = 0; i < n - 1; i++)segments.push(points[i + 1].sub(points[i]));

  // Start points
  left.push(points[0].add(segments[0].rot(R).norm().mul(t)));
  right.push(points[0].add(segments[0].rot(-R).norm().mul(t)));

  // Middle points
  for (let i = 0; i < n - 2; i++) {
    const sint = segments[i].crs(segments[i + 1]) / (segments[i].len() * segments[i + 1].len()); // sin(theta); theta = angle between segment[i] and segment[i+1]
    if (Math.abs(sint) < EPSILON) {
      left.push(points[i + 1].add(segments[i].rot(R).norm().mul(t)));
      right.push(points[i + 1].add(segments[i].rot(-R).norm().mul(t)));
    } else {
      const unit = segments[i].norm().sub(segments[i + 1].norm());
      const d = unit.mul(t).div(sint); // d is 'right' side vector.0
      right.push(points[i + 1].add(d));
      left.push(points[i + 1].sub(d));
    }
  }

  // End points
  left.push(points[n - 1].add(segments[n - 2].rot(R).norm().mul(t)));
  right.push(points[n - 1].add(segments[n - 2].rot(-R).norm().mul(t)));

  return [left, right];
}

export { createThickLine, getPathFunction };