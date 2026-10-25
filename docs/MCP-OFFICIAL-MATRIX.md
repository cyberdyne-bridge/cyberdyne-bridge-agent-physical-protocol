# MCP 官方 reference server 矩阵

**日期：** 2026-10-25  
**范围：** `modelcontextprotocol/servers` 当前 7 台 reference server  
**传输：** 本地 stdio  
**重复：** 每台 5 次  
**性质：** 本地结构矩阵，不是公网扫描，不是生产级安全认证

---

## 1. 范围

`modelcontextprotocol/servers` 当前 reference servers：

```text
everything          TypeScript
fetch               Python
filesystem          TypeScript
git                 Python
memory              TypeScript
sequentialthinking  TypeScript
time                Python
```

**不是** registry 里的 2,376 / 23,533 台社区服务器。  
**不是** `servers-archived` 里的归档实现。

---

## 2. 环境

```text
Node.js       v22.14.0
Python        3.14
mcp           2.3.0
```

TypeScript 包：

```text
@modelcontextprotocol/server-everything@1.0.0
@modelcontextprotocol/server-filesystem@1.0.0
@modelcontextprotocol/server-memory@1.0.0
@modelcontextprotocol/server-sequential-thinking@1.0.0
```

Python 包：

```text
mcp-server-fetch  2026.10.24
mcp-server-git    2026.10.19
mcp-server-time   2026.10.19
```

依赖安装在 `/tmp`，没有写进仓库。  
没有 root，没有公网服务，没有 API key。

---

## 3. 每台做什么

每台重复 5 次：

```text
启动进程
initialize
tools/list
取 serverInfo / instructions / tools
计算 full digest
做一次安全、本地的 tools/call smoke
关闭
```

Digest 覆盖：

```text
serverInfo
instructions
完整 tools
```

不是只看：

```text
name + description + inputSchema + annotations
```

---

## 4. 结果

| server | runs | digest stable | tools | instructions | smoke | p50 |
|---|---:|---:|---:|---:|---:|---:|
| everything | 5/5 | yes | 13 | 2004 chars | yes | 273 ms |
| filesystem | 5/5 | yes | 14 | 0 | yes | 264 ms |
| memory | 5/5 | yes | 9 | 0 | yes | 248 ms |
| sequentialthinking | 5/5 | yes | 1 | 0 | yes | 242 ms |
| fetch | 5/5 | yes | 1 | 0 | yes | 918 ms |
| git | 5/5 | yes | 12 | 0 | yes | 817 ms |
| time | 5/5 | yes | 2 | 0 | yes | 794 ms |

结果：

```text
7/7 server 启动成功
35/35 次运行成功
7/7 full digest 在 5 次启动间稳定
7/7 smoke 调用成功
```

Digest：

```text
everything          b9136ee65067aba5
filesystem          a6932e5fcd524b64
memory              052bdf215e7c72cf
sequentialthinking  ae51c64678ab9035
fetch               0e9b0d714b5a8694
git                 aa9ec73aa42f151b
time                f31729bb0a9a417c
```

`everything` 是唯一一个返回 server-level `instructions` 的 reference server。  
当前版本 instructions 为 2,004 字符；旧手机端测到的 1,575 字符是另一个版本/时点，不能混用。

---

## 5. Smoke 调用

```text
everything          echo
filesystem          list_allowed_directories
memory              read_graph
sequentialthinking  sequentialthinking
fetch               fetch(local HTTP fixture)
git                 git_status(temp repo)
time                get_current_time(UTC)
```

`fetch` 只在 `127.0.0.1` 上取一个本地测试页；启动时使用：

```text
--allow-private-ips
```

这是为了允许本地 fixture，不代表默认应该开放私网抓取。

---

## 6. 怎么复现

```bash
# 1) portable Node 22（示例路径）
# 2) TS 包
cd /tmp/mcp-official
npm install --no-audit --no-fund \
  @modelcontextprotocol/server-everything \
  @modelcontextprotocol/server-filesystem \
  @modelcontextprotocol/server-memory \
  @modelcontextprotocol/server-sequential-thinking

# 3) Python 包
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python \
  'mcp-server-fetch==2026.10.24' \
  'mcp-server-git==2026.10.19' \
  'mcp-server-time==2026.10.19'

# 4) 矩阵
cd /path/to/cyberdyne-bridge
PATH=/tmp/node22/bin:$PATH \
python3 tools/mcp_official_matrix.py \
  --repeat 5 \
  --out /tmp/mcp-official/matrix.json \
  --md /tmp/mcp-official/matrix.md
```

---

## 7. 结论

### 能说的

```text
当前 7 台官方 reference server 在本地 stdio 下：
  - 都能启动
  - tools/list 结构稳定
  - full digest 跨 5 次启动稳定
  - 每台一个安全 smoke call 成功
```

### 不能说的

```text
不能说“所有 MCP 官方/社区服务器都安全”
不能说“tools/call 全量工具都验证过”
不能说“HTTP / OAuth / 多租户 scope 已验证”
不能说“这是漏洞扫描”
```

HTTP + 认证 + scope 分叉的测试在：

```text
tests/mcp/test_http_scope_integrity.py
poc/mcp_scope_fork_poc.py
```

## 8. 和 #3452 的关系

这组数据补的是：

```text
官方 reference 的当前稳定性基线
instructions 是否真的存在
full digest 是否覆盖 instructions
```

它不替代 #3452 的协议讨论，也不把“稳定”误写成“安全”。

一句话：

> **7 台官方 reference，35 次启动，full digest 全稳定；  
> 但稳定不等于可信，完整性也不等于授权。**
