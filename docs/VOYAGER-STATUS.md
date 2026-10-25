# Voyager 评估（2026-10-25）

**结论：** 保留为 bridge / 历史参考；不作为第一版 1.21.1 外部 brain。

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

## 2. 本地验证

```text
python3 agents/voyager/smoke.py
-> voyager smoke ok

node --check agents/voyager/adapter/adapter.mjs
-> exit 0
```

注意：smoke 只检查文件存在和 JSON 可解析，**不是端到端 MC 测试**。

历史文档记录过 2026-10-23 的 1.19.2 bridge 8/8 实测，但当前：

```text
external/Voyager        不在当前 checkout
external/voyager-mc     不在当前 checkout
Minecraft 1.19.2 server 未运行
bridge                  未运行
```

所以那组 8/8 **现在不能当场复现**，只能作为历史证据引用。

---

## 3. 和当前目标的冲突

当前 MC 计划固定：

```text
Minecraft 1.21.1
```

Voyager 文档和历史测试是：

```text
Minecraft 1.19.2
```

这不是“改个端口”就能忽略的差异：

```text
protocol / packet ids
Mineflayer version
bridge API
item/block data
pathfinder behavior
```

要接 1.21.1，需要重新验证 Voyager bridge 和 Mineflayer，不是直接复用。

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
1. Qwen 本地 planner
2. Mindcraft 作为外部 brain 对照
3. Voyager 只在 1.21.1 bridge 重新验证后再考虑
```

---

## 5. 如果以后要重启 Voyager

最小验收：

```text
[ ] 1.21.1 server + 对应 Mineflayer bridge
[ ] bridge /state 可读
[ ] adapter 能 forward / say / stop
[ ] CBAP device mc://voyager/bot 可见
[ ] lease + estop + facts
[ ] 8/8 重跑，不引用旧 1.19.2 结果
```

一句话：

> **Voyager 现在是一个有价值的 bridge 参考，不是一个已经接好的 1.21.1 brain。**
