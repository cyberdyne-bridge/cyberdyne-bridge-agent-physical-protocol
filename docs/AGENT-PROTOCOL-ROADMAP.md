# Agent 协议地图与 CBAP 长期安排

**日期：** 2026-10-25  
**结论：** CBAP v1 在自己范围内是完整的；作为“通用 Agent 协议”是不完整的，也不应该做成全栈。

---

## 1. 先回答“我们是不是没做完整”

要分三种完整：

| 完整 | 现状 | 判断 |
|---|---|---|
| 规范完整 | 消息、Schema、错误、设备契约、129 条一致性 | **基本完整** |
| 生态完整 | SDK、registry、身份、观测、跨 Agent 互操作 | **不完整** |
| 全栈 Agent 协议 | 模型 API、规划、UI、支付、工具发现 | **不应该做** |

> **CBAP 是设备控制面，不是“Agent 的一切”。**

---

## 2. 协议分层

![Agent protocol layers](diagrams/protocol-map.svg)

| 层 | 代表 | CBAP 的位置 |
|---|---|---|
| L1 模型 / 运行时 | OpenAI Responses API、Agents SDK、AgentKit、Qwen、Mindcraft | 不碰 |
| L2 工具 / 上下文 | MCP、tool schemas、resources | 消费 / adapter |
| L3 Agent ↔ Agent | A2A、task handoff、delegation | 可选 adapter |
| **L4 设备控制** | **CBAP** | **核心** |
| L5 证据 / 身份 | audit、OpenTelemetry GenAI、OAuth/OIDC、attestation | 集成 / 扩展 |

关键判断：

```text
模型调用不是 CBAP
工具发现不是 CBAP
Agent 之间怎么聊天不是 CBAP
UI 怎么渲染不是 CBAP
```

CBAP 只回答：

```text
哪个 Agent
在什么授权范围
拿到哪个设备
能执行什么动作
执行有没有发生
出事能不能停
有没有证据
```

---

## 3. 现在缺什么

### P0：不做会限制采用

```text
[ ] 冻结 v1 scope / non-goals
[ ] OpenAI Responses / function-call wrapper
[ ] MCP 作为工具/身体的标准 adapter
[ ] A2A 任务 handoff 设计（不复制 A2A）
[ ] OpenTelemetry GenAI 导出
[ ] approval 绑定 definition + args + scope + nonce
[ ] 身份委托链 / OAuth/OIDC 对接设计
```

### P1：长期协议能力

```text
[ ] 长任务 / 异步 task id / progress
[ ] 流式事件和 backpressure
[ ] signed capability envelope
[ ] verifier / attestation hook
[ ] 多设备 registry / discovery
[ ] 多租户与配额
[ ] 版本协商 / capability negotiation
```

### P2：生态

```text
[ ] Python / TypeScript SDK 对齐
[ ] conformance profiles
[ ] 第三方 driver certification
[ ] 形式化 / 模型检查（只对核心状态机）
```

---

## 4. 长期路线

### H1（现在 → 3 个月）：把边界钉死

```text
v1 不再加“大而全”的协议字段
补 interoperability，而不是补宇宙
先做 OpenAI tool wrapper + MCP adapter + A2A 设计
```

交付：

```text
docs/PROTOCOL-SCOPE.md
drivers/openai_tools/（或 adapter）
A2A gateway design
OTel export
identity delegation design
```

### H2（3 → 6 个月）：v1.1 互操作

```text
A2A handoff
async task / progress
signed call envelope
approval args binding
MCP + OpenAI tool schema mapping
```

验收：

```text
一个 OpenAI-style tool call 能落到 CBAP device
一个 A2A task 能申请 CBAP lease
一个 approval 能绑定 args + definition + scope
一个 audit 能导出 OTel
```

### H3（6 → 12 个月）：v2 可信执行

```text
capability token / delegation chain
attestation hook（不假装有 TPM）
multi-tenant policy
registry / discovery
certification profile
```

---

## 5. 明确不做

```text
不做模型 API
不做 Agent planner
不做 UI 协议
不做支付协议
不做通用 tool registry
不复制 MCP
不复制 A2A
不复制 AG-UI
```

如果某个需求属于上面任何一项：

```text
先写 adapter
再决定要不要进 core
```

---

## 6. 判断新功能的三条规则

```text
1. 它是不是“设备/动作/授权/事实”问题？
   是 -> 可能属于 CBAP
   否 -> 先做 adapter

2. 现成协议能不能做？
   能 -> 接，不重写

3. 会不会破坏 v1？
   会 -> v2 / extension，不硬塞
```

---

## 7. 参考

```text
OpenAI Agents SDK     https://openai.github.io/openai-agents-python/
OpenAI AgentKit       https://openai.com/index/introducing-agentkit/
MCP                   https://modelcontextprotocol.io/
A2A                   https://a2a-protocol.org/latest/
AG-UI                 https://docs.ag-ui.com/
OpenTelemetry GenAI   https://opentelemetry.io/docs/specs/semconv/gen-ai/
```

一句话：

> **CBAP 不需要变成 OpenAI 的替代品；它需要成为 Agent 碰物理世界时，最可信的那一层。**
