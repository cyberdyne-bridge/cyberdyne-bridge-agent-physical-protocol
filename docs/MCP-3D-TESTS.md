# MCP 第三层：执行授权测试

**日期：** 2026-10-25  
**范围：** CBAP MCP device driver  
**定位：** 记录 CBAP 能拦什么、不能证明什么，不是对具体 server 的漏洞指控

---

## 1. 三层定义

```text
1D  Description integrity       模型看到的文字
2D  Tool-definition integrity   schema / annotations / instructions / title
3D  Execution authority         这次调用有没有被授权、是否按批准的方式执行
```

#3452 修的是 1D/2D。  
这份文档只讨论 3D。

---

## 2. CBAP 漏洞修复

修复前 `drivers/mcp_device/driver.py` 的 pin：

```text
只取 name / description / inputSchema / annotations
用 json.dumps(sort_keys=True) 而不是 JCS
不包含 title / outputSchema
连接后不重新检查 tools/list
```

修复后：

```text
完整 tool 对象（title / outputSchema / icons 等）
serverInfo.name + version
instructions（缺失 = 空串）
tools 按 name 排序
RFC 8785 JCS
SHA-256 + domain separator
旧 pin 格式 fail closed
每次动作前重新拉取 tools/list 并比对
```

测试：

```text
tests/cbap/test_mcp_definition.py
tests/cbap/test_mcp_3d.py
```

---

## 3. 3D 测试矩阵

| # | 场景 | CBAP 结果 | 说明 |
|---|---|---|---|
| T1 | 批准后定义变化 | **拒绝** | 完整 definition digest + 重新校验 |
| T2 | 批准后换参数 | **部分** | approval 保存的是提交时的 frame；但没有标准 args UI/hash |
| T3 | annotation 撒谎 | **不拦截** | `readOnlyHint` 只是 hint，不是授权 |
| T4 | 定义不变、行为变了 | **依赖 facts** | 有 `expect` 且 facts 独立时才可能发现 |
| T5 | 重试导致重复副作用 | **由 Kernel 幂等键处理** | 不是 definition pin 的职责 |
| T6 | scope 越权 | **由 policy 拒绝** | 不是 definition pin 的职责 |

---

## 4. 已跑测试

### T3：annotation 不是 enforcement

`--annotation-lie` 的 fake server 返回：

```json
"annotations": {"readOnlyHint": true}
```

但实际会写状态。  
CBAP 仍然执行并依赖 facts 判断，不把 annotation 当安全边界。

测试：

```text
test_annotation_is_a_hint_not_an_enforcement
```

### T4：定义稳定，行为漂移

`--liar-after`：

```text
第一次 turn_on 正常
之后 turn_on 返回 ok 但不改状态
definition 完全没变
```

有 `expect`：

```text
fact mismatch -> CBAP 拒绝
```

没有 `expect`：

```text
status = observed，不是 verified
```

测试：

```text
test_same_definition_behavior_drift_is_caught_by_facts
test_behavior_drift_without_expect_is_only_observed
```

### T1：定义变化

`--drift-title` 在第二次 `tools/list` 时修改 `title`：

```text
旧四字段 digest 看不见
新完整 JCS digest 能看见
CBAP 在动作前拒绝
```

测试：

```text
test_same_connection_title_drift_is_rejected
```

---

## 5. 仍然不能证明的

```text
server 从第一次连接就是恶意的
server 的 facts 也是假的
server 在 tools/list 和 tools/call 之间切换行为
server 的代码/部署被替换但没有改定义
client 批准界面没有展示 args
```

CBAP 的定位是：

```text
调用前的 policy / lease / approval / definition binding
调用后的 facts / audit / estop
```

不是：

```text
远端 server 的行为证明
硬件/代码 attestation
```

---

## 6. 结论

```text
1D/2D 可以用 digest 收紧。
3D 只能靠：
  调用前授权
  args/definition 绑定
  facts 独立验证
  沙箱/最小权限
  审计/急停
```

> **完整 digest 让菜单不可偷换；  
> 它不保证厨房按菜单做菜。**
