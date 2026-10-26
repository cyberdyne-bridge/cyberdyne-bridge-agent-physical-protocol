# MCP 上游状态

**日期：** 2026-10-26（增量更新）
**状态：** 等待官方规范修复
**CBAP 本地版本：** v1.7.5
**定位：** 本地缓解，不是官方结论

---

## 一句话

> **MCP #3452 还在上游讨论；CBAP 只做本地缓解，不把“本地 pin 住了”说成“MCP 修好了”。**

![MCP upstream status](diagrams/mcp-upstream-status.svg)

---

## 0. 2026-10-26 增量

交接实测带来的更新，不改 CBAP 的边界判断：

```text
MCP 2026-07-28 规范   已发布；去 session / 去 initialize；server/discover
官方 server 包         2.x 为现行线；2026.8.31 四个包已 deprecated
双 era 行为            同一条连接只属于一个 era，首请求决定；#2410 补服务端实测
```

关键后果：

```text
v1.7.5 的 pin 公式是按 legacy initialize / serverInfo 写的
它没有被验证覆盖 2026-07-28 的 _meta.protocolVersion / server/discover 形态
迁移不是改个字符串：scope × protocolVersion × capabilities 都要重新定义
```

所以：

```text
v1.7.5 仍可作为 legacy 本地缓解
不能对外说它覆盖了 2026-07-28
```

---

## 1. 上游还在讨论什么

| 议题 | 状态 | 链接 |
|---|---|---|
| 工具定义完整性 / description pinning | **OPEN** | [#3452](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3452) |
| `instructions` 是否属于完整性范围 | 已讨论，未有最终规范 | #3452 thread |
| 同授权范围跨 session 一致性 | 已有测试和措辞建议 | #3452 thread |
| serverInfo 可选身份元数据 | **MERGED** | [#3002](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/3002) |
| stateless / sessionless 方向 | **MERGED** | #2567 / #2575 |
| sessions / thread IDs | 工作组讨论 | [transports-wg#36](https://github.com/modelcontextprotocol/transports-wg/issues/36) |
| 2026-07-28 规范 | 已发布；去 session / 去 initialize / `server/discover` | [spec](https://modelcontextprotocol.io/specification/2026-07-28) |
| 官方 server 包 2.x | 现行；`2026.8.31` 系列 deprecated | `server-everything@2.0.1` 等 |
| SDK 双 era 默认 | #2410 讨论；服务端 legacy-first 也是 sticky | [#2410](https://github.com/modelcontextprotocol/typescript-sdk/issues/2410) |

不要把这些状态混成一句“官方认可”。

---

## 2. 三层边界

```text
1D  Description integrity        文字有没有被换
2D  Tool-definition integrity    schema / annotations / title / instructions
3D  Execution authority          这次调用是否被授权、是否按批准执行
```

#3452 主要讨论 1D/2D。

3D **不在 #3452 的修复范围内**。
一个稳定的 digest 不能证明远端 server 会按定义执行。

---

## 3. CBAP 本地做了什么

v1.7.5（**legacy profile，尚未覆盖 2026-07-28**）：

```text
完整 tool object
serverInfo.name + version
instructions（缺失 = 空串）
tools 按 name 排序
RFC 8785 JCS
SHA-256 + domain separator
旧 pin fail closed
每次动作前重新拉取 tools/list 校验
```

测试：

```text
tests/cbap/test_mcp_definition.py
tests/cbap/test_mcp_3d.py
docs/MCP-3D-TESTS.md
```

这些是 **CBAP 的 legacy 本地控制**，不是 MCP 官方实现，也不是 2026-07-28 的完整实现。

---

## 4. 还没有解决的

```text
server 从第一次连接就恶意
server 连 facts 一起撒谎
server 在 tools/list 和 tools/call 之间切换
远端代码/部署替换但没有改定义
approval UI 没有展示完整 args
没有 TPM / 代码 attestation
```

---

## 5. 现在的策略

```text
不在上游重复开 issue
不把本地 pin 说成官方修复
继续保留本地测试和 PoC
等 #3452 / transports-wg 有明确方向
```

如果上游需要，我们可以提供：

```text
JCS profile
限定 scope 的 fixture
同连接 definition drift 测试
3D 边界测试
```

---

## 6. 相关链接

```text
#3452       https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3452
#3002       https://github.com/modelcontextprotocol/modelcontextprotocol/pull/3002
#2410       https://github.com/modelcontextprotocol/typescript-sdk/issues/2410
WG #36      https://github.com/modelcontextprotocol/transports-wg/issues/36
3D tests    docs/MCP-3D-TESTS.md
Gist        https://gist.github.com/6750432/43837d3355de826dfb83f04acbda9139
```

一句话：

> **上游没修完，CBAP 先把能守的守住；剩下的明确写出来。**
