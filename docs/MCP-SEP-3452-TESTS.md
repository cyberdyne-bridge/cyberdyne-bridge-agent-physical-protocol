# MCP SEP #3452: 认证 HTTP / 授权范围测试

**日期：** 2026-10-25  
**状态：** 本地测试通过  
**对象：** SEP #3452 tool definition integrity  
**定位：** spec gap 验证，不是 0-day，不是对某个实现的漏洞指控

---

## 1. 为什么补这组测试

手机端已经做了：

```text
官方 stdio server × 4
同进程双 init + 10 次独立启动
instructions 替换 + 四字段 digest 漏检
HTTP 双 client 分叉 PoC
```

但手机端做不了：

```text
带认证的 HTTP MCP server
不同授权范围 / 不同 token
同一 scope 跨 session 一致性
session/token 绑定
```

这组测试补的就是这一半。

---

## 2. 结论先行

```text
same scope, different sessions  -> 应一致，测试通过
different scopes                -> 可以不同，不能误报
same scope, forked view         -> full digest 能检出
instructions-only change        -> 四字段 digest 仍漏，full digest 检出
missing / unknown token         -> 401
session token swap / replay     -> 403
```

这组结果支持把规范措辞改成：

> **同一授权范围内，定义跨 session 必须一致。**

而不是：

> ~~同一 session 的每个 client 必须一致。~~

后者绑不住任何东西，因为 session 通常就是一个 client。

---

## 3. 测试文件

```text
poc/mcp_auth_fixture.py               控制夹具
poc/mcp_scope_fork_poc.py             独立 PoC
tests/mcp/test_http_scope_integrity.py
```

控制夹具：

```text
HTTP JSON-RPC endpoint: /mcp
Bearer token -> scope
read  scope: read_file, list_dir
admin scope: read_file, list_dir, delete_file
initialize -> instructions + Mcp-Session-Id
tools/list -> 按 scope 返回
```

它不是生产 MCP server，不实现完整 SSE / OAuth / 真实策略引擎；  
它只验证**授权范围与定义完整性之间的关系**。

---

## 4. 8 条测试

```text
1. same_scope_is_stable_across_sessions
   reader-a 和 reader-b 都是 read scope
   -> tools / instructions / full digest 完全一致

2. different_scopes_may_legitimately_differ
   read vs admin
   -> admin 多 delete_file
   -> 差异是合法的，不能被 naive “所有 client 必须一样” 误判

3. same_scope_fork_is_detected_by_full_digest
   fork 模式下第二个 read session 多 exfiltrate
   -> full digest 不同，能检出

4. instructions_only_change_is_missed_by_four_field_digest
   tools 完全一样，只改 instructions
   -> four_field_digest 相同
   -> full digest 不同
   -> 证明 instructions 必须进入完整性范围

5. missing_bearer_token_is_rejected
   -> HTTP 401

6. unknown_token_is_rejected
   -> HTTP 401

7. reader_session_cannot_swap_to_admin_token
   -> HTTP 403

8. admin_session_cannot_be_replayed_with_reader_token
   -> HTTP 403
```

运行测试：

```bash
python3 -m unittest -v tests.mcp.test_http_scope_integrity
```

运行独立 PoC：

```bash
python3 poc/mcp_scope_fork_poc.py
```

PoC 会打印四组对照：

```text
1. same read scope, two sessions
   -> full digest 相同

2. read vs admin scope
   -> tools / full digest 不同，属于合法差异

3. same read scope, forked view
   -> full digest 不同，检出

4. instructions-only change
   -> 四字段 digest 相同
   -> full digest 不同，检出
```

本机实测结尾：

```text
PoC PASS: same-scope fork and instructions-only drift are visible
to a full digest; legitimate scope differences are preserved.
```

结果：

```text
Ran 8 tests in 4.042s
OK
```

---

## 5. Digest 口径

Full snapshot：

```text
serverInfo
instructions
tools（完整定义）
```

Four-field digest：

```text
name
description
inputSchema
annotations
```

测试明确记录：

```text
只改 instructions 时：
  four_field_digest 不变
  full digest 变
```

这和 thread 里 Sultan 的数据方向一致：

```text
23,533 台 server，58% 有 instructions
2,691 对读取中，instructions 变化 1,236
其中 574 对 tools 完全没变
四字段 digest 会漏掉其中一部分
```

这些人口级数字来自 Sultan 的数据，不是这组本地测试生产的。

---

## 6. 边界

```text
不是漏洞扫描
不是真实 MCP SDK 互通测试
不是 SSE / Streamable HTTP 全实现
不是 OAuth / OIDC / 企业策略
不是对某个 server 的漏洞指控
```

它证明的是：

> 在“同一授权范围跨 session”这个口径下，  
> **测试可以区分“合法 per-scope 差异”和“同 scope 分叉”**，  
> 并且 **instructions 必须进入 digest**。

---

## 7. 可直接用于 issue 的英文回复草稿

```text
Thanks — the correction is right: "every client of the same session" does not
bind anything, because a session is normally one client. I re-ran the missing
half on the desktop with an authenticated HTTP fixture and narrowed the
invariant to "same authorization scope, across sessions."

Eight local tests pass:

- two sessions with the same read scope -> identical tools, instructions and
  full digest;
- read vs admin scope -> different tools, treated as legitimate rather than a
  fork;
- same read scope but a forked view -> full digest differs and detects it;
- instructions-only change, tools unchanged -> four-field digest is identical,
  full digest differs;
- missing/unknown bearer token -> 401;
- session/token swap or replay -> 403.

The full digest covers serverInfo + instructions + the complete tool
definitions. This is a controlled fixture, not a claim about a specific
implementation; the useful part is the test shape and the scope wording.

Happy to share the fixture/tests if useful for the conformance discussion.
```

---

## 8. 下一步

```text
[ ] 把这 8 条测试接到 CI（独立 job，不混入 CBAP 118）
[ ] 用真实 MCP SDK 再跑同一组 scope/session 断言
[ ] 给 SEP 文本补一句 instructions 是否在范围内
[ ] 身份延续 / 命名空间另开 issue
```
