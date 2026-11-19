'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const {
  SonarProbe,
  归座标,
  方位名,
  环名,
} = require(path.resolve(__dirname, '../../agents/cyberdyne/hand/node/plugins/sonar/proto_sonar.js'));

test('归座标 accepts arrays, Vec3-like objects, and falls back on NaN', () => {
  assert.deepEqual(归座标([1, 2, 3], [9, 9, 9]), [1, 2, 3]);
  assert.deepEqual(归座标({x: 4, y: 5, z: 6}, [9, 9, 9]), [4, 5, 6]);
  assert.deepEqual(归座标([Number.NaN, 2, 3], [9, 9, 9]), [9, 9, 9]);
  assert.deepEqual(归座标(null, [7, 8, 9]), [7, 8, 9]);
});

test('方位距离 returns front/left/back/right and 10-block rings', () => {
  const p = new SonarProbe();
  // Current implementation convention: +x = 前, +z = 右, -x = 后, -z = 左.
  // TODO: yaw direction still needs live calibration; this test locks the
  // current pure-function contract so a silent change cannot slip through.
  assert.equal(p.方位距离([10, 0, 0], [0, 0, 0], 0).方位, 方位名[0]);
  assert.equal(p.方位距离([0, 0, 10], [0, 0, 0], 0).方位, 方位名[6]);
  assert.equal(p.方位距离([-10, 0, 0], [0, 0, 0], 0).方位, 方位名[4]);
  assert.equal(p.方位距离([0, 0, -10], [0, 0, 0], 0).方位, 方位名[2]);

  const near = p.方位距离([0, 0, 3], [0, 0, 0], 0);
  assert.equal(near.环, 环名[0]);
  assert.equal(near.距离, 3);
  assert.equal(p.方位距离([0, 0, 25], [0, 0, 0], 0).环, 环名[2]);
  assert.equal(p.方位距离([0, 0, 99], [0, 0, 0], 0).环, 环名[4]);
});

test('方位距离 rotates with facing angle', () => {
  const p = new SonarProbe();
  // This is the current rotation convention; if yaw calibration changes,
  // the test must be updated together with the implementation.
  const r = p.方位距离([10, 0, 0], [0, 0, 0], 90);
  assert.equal(r.方位, 方位名[6]);
});
