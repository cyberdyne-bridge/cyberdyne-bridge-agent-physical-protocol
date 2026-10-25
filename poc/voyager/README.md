# Voyager PoCs

These are minimal local reproductions for [`docs/VOYAGER-BUGS.md`](../../docs/VOYAGER-BUGS.md).

```bash
export VOYAGER_SRC=/path/to/Voyager
export PATH=/path/to/node/bin:$PATH

python3 poc/voyager/poc_record_onchat.py
bash poc/voyager/poc_babel_missing.sh
node poc/voyager/poc_hawkeye_plugin.js
```

Expected outputs:

```text
REPRODUCED: KeyError 'status' ...
REPRODUCED: @babel/core is missing ...
require("minecrafthawkeye") typeof = object
REPRODUCED: upstream calls bot.loadPlugin(minecraftHawkEye) with an object
```

The tests do not start Minecraft. They are parser/recorder/dependency repros.
