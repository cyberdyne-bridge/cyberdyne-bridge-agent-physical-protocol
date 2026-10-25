#!/usr/bin/env node
const path = require('path');
const src = process.env.VOYAGER_SRC || '/tmp/voyager-audit';
const h = require(path.join(src, 'voyager/env/mineflayer/node_modules/minecrafthawkeye'));
console.log('require("minecrafthawkeye") typeof =', typeof h);
if (typeof h !== 'function') {
  console.log('REPRODUCED: upstream calls bot.loadPlugin(minecraftHawkEye) with an object');
  process.exit(0);
}
console.log('NOT REPRODUCED: export is a function');
process.exit(1);
