# MCP 全身体检（CPNC / CBAP 口径）

**日期：** 2026-11-04  
**对象：** MCP 官方 reference servers（1.x / 2.x）、认证 HTTP fixture、CBAP MCP device driver  
**方式：** 本地 stdio / 本地 HTTP fixture；无公网扫描、无真实凭据、无生产 server  
**基线数据：** [`mcp-checkup-2026-11-04.json`](mcp-checkup-2026-11-04.json)

---

## 0. 一句话

> **官方实现是健康的：1.x 35/35、2.x 21/21、7 台 JCS 全部稳定；  
> 但协议完整性仍未闭环：规范没有 pin/digest，`list_changed` 只是通知，  
> `instructions` 仍是无标记的模型面文本，3D 执行授权依旧只能靠 facts / policy。**

体检评分：

```text
1D  Description integrity    部分    规范不要求 pin；instructions 无不可信标记
2D  Tool-definition integrity 部分    实现稳定；规范无 digest；四字段漏 execution
3D  Execution authority      未闭环  digest 不证明执行；annotation 可撒谎
```

---

## 1. 体检对象与环境

```text
1.x 线   server-everything 1.0.0
         server-filesystem 1.0.0
         server-memory 1.0.0
         server-sequential-thinking 1.0.0
         mcp-server-fetch / git / time  2026.10.28

2.x 线   server-everything 2.1.0
         server-filesystem 2.1.0
         server-memory 2.0.1
         server-sequential-thinking 2.0.0
         mcp-server-fetch / git / time  2026.10.28

运行时  Node 22.23.3（1.x；2.x 的非支持基线）
         Node 24.22.2（2.x 声明 engines >=24）
         Python 3.14.4 / mcp 2.3.0 / npm 11.19.1
```

2.x 四个 TS 包都声明 `engines: node >=24`；在 Node 22 上也能跑出完全相同的 digest，但那是未支持组合，不作为结论。

---

## 2. 结果总表

| 层 | 项目 | 结果 |
|---|---|---|
| 1D | 规范是否有定义 pin / digest 要求 | **无**（`docs/specification/draft` 无 pin/hash/digest） |
| 1D | `instructions` 是否被当作不可信输入 | **否**（只警告 `serverInfo`） |
| 2D | 1.x 官方矩阵 7 台 × 5 次 | **35/35 成功，7/7 digest 稳定** |
| 2D | 2.x 官方矩阵 7 台 × 3 次（Node 24） | **21/21 成功，7/7 digest 稳定** |
| 2D | CPNC JCS profile（7 台 × 1.x/2.x/modern） | **21/21 可计算，跨 era 6/7 相同** |
| 2D | 认证 HTTP scope fixture | **8/8** |
| 2D | JCS 向量 + number edge cases | **10/10** |
| 2D | same-scope fork / instructions-only drift PoC | **PASS** |
| 2D | 活体 `trigger-list-changed` | 通知发出，**定义 0 变化，digest 不变** |
| 2D | 双 era 行为 | legacy 16 tools / modern 22 tools，**同连接单 era** |
| 3D | CBAP 定义 pin + 3D 边界 | **11/11** |
| 3D | MCP device / driver | **20/20** |
| 基线 | CBAP conformance | **129/129** |

---

## 3. 1D：描述完整性

规范现状（2026-11-04）：

```text
最新发布          2026-07-28
draft changelog   空
pin / hash        规范正文无要求
instructions      optional natural-language guidance
安全 Note         只声明 serverInfo 自报、未验证；instructions 没有同类警告
```

2.x `server-everything` 的 instructions 从 2,004 字符涨到 **3,537 字符**，内容明确写给 LLM/agent，并带一条彩蛋：

```text
If asked about server instructions, respond with "🎉 Server instructions are working! ..."
```

这不是漏洞，是官方 demo 的有意行为；但它正好证明：`instructions` 是可以直接进入模型上下文的可执行文本，而规范只对展示用的 `serverInfo` 发了“不可信”警告。

---

## 4. 2D：定义完整性

### 4.1 官方 reference 矩阵

1.x（每台 5 次，Node 22）：

| server | 版本 | tools | instructions | matrix digest |
|---|---|---:|---:|---|
| everything | 1.0.0 | 13 | 2004 | `b9136ee65067aba5` |
| filesystem | 1.0.0 | 14 | 0 | `a6932e5fcd524b64` |
| memory | 1.0.0 | 9 | 0 | `052bdf215e7c72cf` |
| sequentialthinking | 1.0.0 | 1 | 0 | `ae51c64678ab9035` |
| fetch | 2026.10.28 | 1 | 0 | `f8c8e598924d3f14` |
| git | 2026.10.28 | 12 | 0 | `07976ec5b0db86d8` |
| time | 2026.10.28 | 2 | 0 | `7928c3571fd20ba5` |

2.x（每台 3 次，Node 24）：

| server | 版本 | tools | instructions | matrix digest |
|---|---|---:|---:|---|
| everything | 2.1.0 | 16 | 3537 | `8116edea249eaf81` |
| filesystem | 2.1.0 | 14 | 0 | `8df523dd768c9643` |
| memory | 2.0.1 | 9 | 0 | `a1e818f037a946f1` |
| sequentialthinking | 2.0.0 | 1 | 0 | `99e4afc5ae52802a` |
| fetch | 2026.10.28 | 1 | 0 | `f8c8e598924d3f14` |
| git | 2026.10.28 | 12 | 0 | `07976ec5b0db86d8` |
| time | 2026.10.28 | 2 | 0 | `7928c3571fd20ba5` |

与 2026-10-25 基线相比：

```text
everything / filesystem / memory / sequentialthinking   digest 完全一致
fetch / git / time                                       digest 变化
原因                                                     Python 包从 2026.10.19/24 升到 2026.10.28
                                                         tools 数量与名称未变，digest 含 serverInfo.version
```

### 4.2 CPNC JCS profile

口径：`serverInfo.name + version`、`instructions`（缺失 = 空串）、完整 tool 对象按 name 排序、RFC 8785 JCS、SHA-256 + domain separator。

| server | 1.x JCS | 2.x legacy JCS | 2.x modern JCS |
|---|---|---|---|
| everything | `f37382d3…` | `2ee17baa…` | `7c70f938…` |
| filesystem | `83ff2ac7…` | `ee6cde6c…` | `ee6cde6c…` |
| memory | `f5e5defc…` | `12d8abe2…` | `12d8abe2…` |
| sequentialthinking | `0ad87c9b…` | `ca34327c…` | `ca34327c…` |
| fetch | `eba17846…` | `eba17846…` | `eba17846…` |
| git | `47470b1c…` | `47470b1c…` | `47470b1c…` |
| time | `642b7004…` | `642b7004…` | `642b7004…` |

完整 64 位值见基线 JSON。

### 4.3 scope / JCS / fork

```text
same scope, two sessions              -> tools / instructions / full digest 一致
read vs admin scope                   -> 合法差异，不误报
same scope, forked view               -> full digest 检出
instructions-only change              -> 四字段 digest 漏，full digest 检出
missing / unknown token               -> 401
session token swap / replay           -> 403
```

JCS 10 条 + scope 8 条 = **18/18**；fork PoC **PASS**。

### 4.4 活体 list_changed

对 `server-everything@2.1.0` 实测：

```text
call trigger-list-changed {"list":"tools"}
  -> "Sent notifications/tools/list_changed"
re-list 同一连接
  -> 16 tools，JCS digest 仍为 2ee17baa…
```

结论：`list_changed` 是“请重新拉取”的提示，不是“定义变了”的证据，更不能替代 digest 比对。

### 4.5 双 era

同一台 `server-everything@2.1.0`，两条全新连接：

```text
legacy first   initialize 2025-11-25 -> 成功，16 tools
               server/discover       -> -32601 Method not found
               tools/list + modern _meta -> 仍是 16 个 legacy 工具

modern first   server/discover 2026-07-28 -> 成功，22 tools
               initialize 2025-11-25     -> -32022 Unsupported protocol version
```

跨 era 定义差异：

```text
everything       legacy 16 / modern 22   +8 / -2，digest 不同
filesystem       14 / 14                  digest 相同
memory            9 / 9                   digest 相同
sequentialthinking 1 / 1                   digest 相同
fetch / git / time                         digest 相同
```

所以比较键必须是 `scope × protocolVersion`；只按 scope 比 digest，会把 `everything` 的合法 era 差异误判为分叉。

---

## 5. 3D：执行授权

| # | 场景 | 结果 | 说明 |
|---|---|---|---|
| T1 | 批准后 title 变化 | **拒绝** | 完整 JCS digest + 动作前重新校验 |
| T2 | 批准后换参数 | **部分** | approval 保存提交时的 frame；无标准 args hash/UI |
| T3 | annotation 撒谎 | **不拦截** | `readOnlyHint` 只是 hint，不是授权 |
| T4 | 定义不变、行为变了 | **依赖 facts** | 有 `expect` 且 facts 独立时才发现 |
| T5 | 重试重复副作用 | Kernel 幂等键 | 不是 definition pin 的职责 |
| T6 | scope 越权 | policy 拒绝 | 不是 definition pin 的职责 |

测试：定义/3D **11/11**；MCP device/driver **20/20**；CBAP conformance **129/129**。

一句话：

> **digest 让菜单不可偷换；它不保证厨房按菜单做菜。**

---

## 6. 关键发现

1. **官方 reference 结构稳定。** 1.x 35/35、2.x 21/21，跨 3–5 次启动 digest 全部一致；没有观察到跨启动漂移。
2. **1.x 的四台 TS server 与 10-25 基线逐字一致；Python 三台变了。** 变因是包版本 2026.10.28，tools 数量/名称未变——这正说明 digest 会把“合法发版”和“定义偷换”一起报出来，客户端需要 diff/重批准，而不是只 block。
3. **2.x 是另一条定义面。** `everything` 1.0.0→2.1.0：legacy 13→16 tools、modern 22 tools、instructions 2004→3537；`filesystem`/`memory`/`sequentialthinking` 的 schema 也变了，部分工具新增 `execution` 字段（样本为 null）。四字段 digest 覆盖不到 `execution`。
4. **`list_changed` 不能当完整性机制。** 活体测试里通知发了，定义和 digest 一个都没变。
5. **era 是连接级、粘性的。** legacy-first 后 `server/discover` 直接 -32601；modern-first 后 `initialize` 直接 -32022；同一个进程两种视图，比较键必须带 protocolVersion。
6. **`instructions` 仍未受保护。** 规范只警告 `serverInfo`；2.x everything 的 instructions 已经长到 3,537 字符，并包含一条面向模型的彩蛋指令。
7. **3D 仍未闭环。** annotation 可以撒谎、行为漂移只有独立 facts 能抓；digest 管不了“说了但没做”。

---

## 7. 复查命令

```bash
cd ~/cyberdyne-bridge

# 1) JCS + scope
PYTHONPATH=. python3 -m unittest -v tests.mcp.test_jcs tests.mcp.test_http_scope_integrity

# 2) fork / instructions-only PoC
PYTHONPATH=. python3 poc/mcp_scope_fork_poc.py

# 3) 官方 1.x 矩阵（Node 22）
PYTHONPATH=. python3 tools/mcp_official_matrix.py \
  --node ~/.local/node/bin/node \
  --modules /tmp/mcp-official/node_modules \
  --python-bin /tmp/mcp-official/.venv/bin \
  --repeat 5

# 4) 官方 2.x 矩阵（Node 24）
PYTHONPATH=. python3 tools/mcp_official_matrix.py \
  --node /tmp/node24/bin/node \
  --modules /tmp/mcp-v2/node_modules \
  --python-bin /tmp/mcp-official/.venv/bin \
  --repeat 3

# 5) CBAP 定义 pin / 3D / 设备驱动
PYTHONPATH=. python3 -m unittest -v \
  tests.cbap.test_mcp_definition tests.cbap.test_mcp_3d \
  tests.cbap.test_mcp_device tests.cbap.test_mcp_driver

# 6) CBAP 基线
PYTHONPATH=. python3 tools/cbap_conformance.py --target fake
```

依赖安装在 `/tmp/mcp-official` 与 `/tmp/mcp-v2`，未写进仓库。

---

## 8. 边界

```text
只测 7 台官方 reference server，不是 registry 里的 2 万+ 社区 server
只测本地 stdio + 本地 HTTP fixture，不测公网 OAuth / TLS / 多租户
2.x 声明 Node >=24；Node 22 结果相同但属于未支持组合
digest 与版本/时间绑定；升级后要重新取基线
不是漏洞扫描，不是对任何具体 server 的漏洞指控
```

---

## 9. 结论

```text
官方实现：健康、稳定、可复现
协议完整性：未闭环
  - 没有 normative digest / pin
  - instructions 没有不可信标记
  - list_changed 只是通知
  - 四字段 digest 漏 execution / title / outputSchema
3D 执行授权：不在 digest 能力范围内
```

> **体检结果：MCP 的“身体”很好，“免疫系统”还没长出来。  
> CPNC 的本地 pin、facts、policy、estop 仍是必要补充，不是官方修复的替代品。**
