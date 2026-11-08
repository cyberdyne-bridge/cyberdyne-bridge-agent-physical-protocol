# Cyberdyne MC Agent

Status: **legacy brain, migrated entrypoint / ours**

This is our original MC Agent:

```text
brain/bridge.py          brain
hand/node/server.js      hand
plugins/                 hot-plug carriages
```

The brain/hand direct UDS path is **legacy** and does not go through CBAP.
The hand can also be wrapped by `McDriver` as the CBAP device
`mc://bot/DeepSeek`.

M4 migration wrapper:

```text
agents/cyberdyne/brain/bridge_cbap.py
agents/cyberdyne/tools/启动大脑-cbap.sh
```

It keeps the legacy brain but replaces `接线口` with `CBAPHandAdapter`.
The original direct hand path remains frozen and is not the recommended runtime.

M4 removed the root compatibility shims. Use the physical paths or the
CBAP wrapper:

```text
agents/cyberdyne/brain/bridge_cbap.py
agents/cyberdyne/tools/启动大脑.sh
agents/cyberdyne/tools/启动手.sh
```

The old direct brain/hand path is frozen; it is not a second controller.

Local smoke: `python3 agents/cyberdyne/smoke.py`
Agent tools: `agents/cyberdyne/tools/`; root launch shims were removed in M4.

## 插件（车厢）

`plugins/` 下每个目录是一个热插拔车厢：`manifest.json` + 入口脚本。
声明 `可热拔: true` 的车厢，`卸下()` 会原样还原它打过的补丁点。

### 自我模型（`plugins/自我模型/`）

只读观察者，车厢 113，v0.2.1。

```text
补丁点    任务栈.接 / _下一步 / _失败 / _看完成了没 / _下发
只写      logs/自我模型.jsonl
不改      任务栈、动作、veto、bridge.py、其它车厢
记录      predicted vs actual、物理体检报告、回执噪声、owned / chest 真读数
```

边界：每个钩子第一件事都是回调原函数并原样返回；观察者自身的异常只写账，
不会让主链因为它失败；卸下时原样还原五个方法。

来源：`boundary-lab` 的 P2–P4 研究线，2026-10-22 经请示/批复接入
（先当身体、不先当大脑；先观察、不抢任务栈）。
