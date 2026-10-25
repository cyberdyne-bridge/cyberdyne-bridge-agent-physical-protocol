# Voyager 评估（2026-10-25）

**结论：** 1.21.1 bridge 已打通，本地 Qwen 单步 action 已跑通；完整 Voyager 自治脑（VoyagerEnv / curriculum / skill library / critic）仍未接，不作为第一版 brain。

---

## 1. 当前真实状态

`agents/voyager/agent.json` 已明确写：

```text
kind: bridge-only
summary: Voyager Mineflayer HTTP bridge exposed through a line-JSON adapter.
         Voyager's autonomous agent is not wired.
```

也就是说，现在有：

```text
Mineflayer bridge
state / exec / forward / say / stop
CBAP McDriver adapter
Qwen planner / exec 实验脚本
```

没有：

```text
VoyagerEnv
curriculum
skill library
critic
自动代码生成
Voyager 自己的 autonomous Python agent
```


---

## 1.5 上游事实（2026-10-25 静态审计）

从 `MineDojo/Voyager` 拉取的当前 `main`：

```text
repo          MineDojo/Voyager
license       MIT
stars         7,287
last code     55e45a8 / 2023-07-27
open issues   7
Python LOC    2,809
tests         无
```

它不是“最近还在活跃开发”的框架。
`pushed_at` 看起来较新，但最后一次代码 commit 是 2023-07-27。

依赖/运行方式：

```text
Python >= 3.9（README 写 3.9）
Minecraft 1.19
Fabric  0.14.18-1.19
Java 17
5 个 Fabric mods
Node >= 16
mineflayer 4.8.1
```

模型不是本地 Qwen：

```text
GPT-4
GPT-3.5-turbo
OpenAIEmbeddings
tiktoken
chromadb==0.3.29
```

`requirements.txt` 没有 lock，且 `chromadb` 是老版本；
在 Python 3.14 下直接安装不是一个合理的第一选择。

```text
Python compileall   pass
adapter node --check pass
端到端 bridge 测试  8/8（2026-10-25 复现，见下）
```

上游 bridge 暴露：

```text
/start
/step
/stop
/pause
```

`/state` 是我们 adapter 的 patch 加的，不是上游默认接口。

### 这意味着

```text
Voyager 是 2023 年的 research code
不是本地 Qwen-ready 的 planner
上游默认不是 1.21.1 的 body；我们用兼容补丁验证了 1.21.1 bridge
没有测试套件
```

---

## 2. 本地验证

```text
python3 agents/voyager/smoke.py
-> voyager smoke ok

node --check agents/voyager/adapter/adapter.mjs
-> exit 0
```

注意：smoke 只检查文件存在和 JSON 可解析，**不是端到端 MC 测试**。

2026-10-25 已用真实环境复现 bridge-only 的 8/8：

```text
JDK              Corretto 17.0.21
Minecraft        1.19.2 vanilla, offline-mode, port 25566
Node             22.14.0
Voyager bridge   /tmp/voyager-audit, patched /state
CBAP adapter     agents/voyager/adapter/adapter.mjs
Kernel          explicit test policy (read/write/lease/estop)
test            agents/voyager/tools/voyager_cbap.py
result          8/8
```

复现结果：

```text
OK  Voyager device visible
OK  read state             [15.5, 65, -30.089...]
OK  lease
OK  forward under lease
OK  position changed       z -30.089 -> -26.210
OK  say under lease
OK  estop
OK  offline after estop
```

两个实测修正：

```text
1. 上游 /state 需要 adapter patch；上游默认没有这个 endpoint。
2. forward 不能用 bot.waitForTicks(20)：1.19.2 server 暂停/慢 tick 时会
   抛 "Timeout waiting for 10 ticks"; 改为 1000ms wall-clock pulse。
```

这仍然只是 **bridge body** 的 8/8：

```text
没有 VoyagerEnv
没有 curriculum
没有 skill library
没有 critic
没有 GPT-4
没有完整 1.21.1 自治 agent
```

`external/Voyager` / `external/voyager-mc` 仍不在仓库内；测试环境在 `/tmp`，
不会把 1.2G node_modules 或 1.9G server 提交进主仓。

另外提供了无 Minecraft 的 fake bridge 测试：

```bash
python3 agents/voyager/tools/voyager_fake_smoke.py
# 8/8, 不证明真实 Mineflayer
```

---

## 3. A/B 结果（2026-10-25）

### A. 1.21.1 bridge

```text
mineflayer       4.39.0
minecraft-data   3.117.0
patch            voyager-state.patch + voyager-1.21.1.patch
result           8/8
position         z -41.3 -> -42.7
```

完整步骤：[`VOYAGER-1.21.1.md`](VOYAGER-1.21.1.md)。

### B. 本地 Qwen action planner

```text
model            Qwen3-4B-Instruct-2507-Q4_K_M.gguf @ 127.0.0.1:8099
prompt           Voyager action_template.txt + response format
embeddings       local hashing fallback, not OpenAIEmbeddings
execution        CBAP -> Voyager adapter -> 1.21.1 bridge
result           Qwen-generated JS ran; server logged "qwen voyager 121"
```

完整边界：[`VOYAGER-LOCAL-QWEN.md`](VOYAGER-LOCAL-QWEN.md)。

这不是完整 VoyagerEnv/curriculum/skill library/critic。
1.21.1 也只验证了 state / forward / say / estop，不是 mining/crafting 全覆盖。

---

## 4. 结论

### 可以做什么

```text
保留 adapter 作为兼容性参考
保留 state / exec / forward / say / stop 语义
需要时接 Voyager planner，但作为外部 brain
```

### 不建议做什么

```text
把 Voyager 当第一版 1.21.1 的 brain
把 bridge-only 说成 autonomous Voyager
把历史 1.19.2 8/8 说成当前可复现
为了 Voyager 把 MC 固定版本退回 1.19.2
```

### 现在的优先级

```text
1. 保留 1.21.1 Voyager bridge
2. 本地 Qwen planner 作为可替换脑
3. 完整 VoyagerEnv/curriculum 另立项目，不混进 CBAP core
```

---

## 5. 如果以后要重启 Voyager

最小验收：

```text
[x] 1.21.1 server + Mineflayer bridge
[x] bridge /state 可读
[x] adapter 能 forward / say / stop
[x] CBAP device mc://voyager/bot 可见
[x] lease + estop + facts
[x] 8/8 重跑
[ ] VoyagerEnv / curriculum / skill library / critic
[ ] 1.21.1 mining/crafting/furnace 全覆盖
```

上游：

```text
https://github.com/MineDojo/Voyager
commit 55e45a880755d0c8c66ca7fb5fe7962ac8974f89
```

一句话：

> **Voyager 现在是一个有价值的 bridge 参考，不是一个已经接好的 1.21.1 brain。**
