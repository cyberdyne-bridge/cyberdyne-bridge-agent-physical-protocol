# Cyberdyne Bridge / CBAP / CPNC · 企业级代码审查

- 审查日期：2026-11-19
- 仓库：`/home/bzys17mintstart/cyberdyne-bridge`
- 审查基线：`289e8a9`（当前分支；含 2026-11-19 审查报告提交）
- 审查范围：CBAP Kernel、安全/审计、MC driver、native Brain/Hand、Console、MCP、测试与部署配置
- 审查方式：代码阅读、git 历史、单元/集成测试、异常扫描、运行时监听检查、配置审查
- 结论：**代码质量中等偏上，但当前部署不可称为生产级。存在 3 个部署 P0、若干 P1 代码/工程缺口。**

---

## 0. 执行摘要

### 已经做对的部分

```text
CBAP default-deny
UDS SO_PEERCRED + token + operator token
lease + fencing + estop/resume
hash-chained audit + checkpoint
CBAP 默认执行路径
lease 申请/续租
allow-foot / watch / error-facts 映射
相同命令去重、不同命令排队
测试与 CI 已存在
```

### 当前最严重的问题

1. **Minecraft RCON 暴露在所有网卡，密码是 `cyberdyne`。**
2. **MC 以 `online-mode=false` + `white-list=false` 运行在全部网卡。**
3. **`/tmp/honeypot/multi.py` 在 `0.0.0.0:2201-2209` 监听，来源不在本仓。**
4. **729 处吞异常，其中 482 处纯静默；`logs/静默.jsonl` 仍有 5985 条历史。**
5. **测试绿不代表覆盖完整：JS 运行逻辑没有行为测试；`tests/body` 已进 CI，但总体仍无 coverage 门槛。**
6. **CI 没有 lint / type / SAST / SCA / coverage。**

### 判定

```text
代码审查：通过，但带条件
生产部署：不通过
最终 MC 自主验收：仍未通过（随机世界 stone_pickaxe 未闭环）
```

---

## 1. 审查证据

### 1.1 测试结果

本次实际运行：

```text
CBAP/CPNC: 136/136 OK
MCP:       27/27  OK
Native:     7/7   OK
Body SDK:   5/5   OK
```

注意：当前 `verify.yml` 已包含 `tests/body`；仍缺 JS 行为测试和 coverage 门槛。

### 1.2 运行时监听

```text
*:25565          java        Minecraft，全部网卡
*:25575          java        RCON，全部网卡
0.0.0.0:2201-2209 python3     /tmp/honeypot/multi.py，来源不在本仓
127.0.0.1:8765   python3     Console
127.0.0.1:8766   python3     local service
127.0.0.1:8099   llama-server
127.0.0.1:9229   CherryStudio inspector
*:1716           kdeconnectd
```

本会话无法以 root 读取 `ufw status`；监听事实本身已足以说明风险。

### 1.3 部署配置

`runtime/server.properties`：

```text
enable-rcon=true
rcon.password=cyberdyne
rcon.port=25575
online-mode=false
white-list=false
enforce-whitelist=false
server-ip=
server-port=25565
op-permission-level=4
```

---

## 2. 发现清单

### P0-01 · RCON 暴露且凭据弱

- 证据：`runtime/server.properties:13,44,45`；`ss` 显示 `*:25575`。
- CWE：CWE-306（关键功能缺少认证）、CWE-521（弱密码）。
- 影响：校园网 `/16` 可达时，RCON 可被暴力/猜测；RCON 具备服务器控制能力。
- 估算严重度：Critical（CVSS 9.0+，视网络可达性）。
- 修复：

```text
优先 enable-rcon=false
如必须保留：rcon.password 改为随机 32+ 字符，且只绑定 loopback/受控网段
UFW 永远不要放行 25575
```

### P0-02 · Minecraft 离线模式 + 关闭白名单 + 全部网卡

- 证据：`runtime/server.properties:37,52,63`；`ss` 显示 `*:25565`。
- CWE：CWE-287（认证不当）、CWE-1188（不安全默认）。
- 影响：同网段任何人可用任意 ID 进入；白名单在 offline-mode 下也不能可靠防冒充。
- 修复：

```text
只本机 bot：server-ip=127.0.0.1，或 UFW 不开 25565
需要联机：online-mode=true
无法正版验证：至少 whitelist + 受控网段/VPN，并明确接受冒充风险
```

### P0-03 · 未登记服务监听全部网卡

- 证据：`/proc/49078/cwd -> /tmp/honeypot`；`multi.py` 监听 `0.0.0.0:2201-2209`。
- 风险：不属于本仓的长期服务；无代码审查、无日志归属、无防火墙规则。
- 修复：

```text
确认是否为有意的 honeypot
不是：立即停止并移除
是：登记 owner、目的、数据保留、访问控制；绝不能默认全 /16 可达
```

### P1-01 · 静默异常仍然过多

- 证据：`tools/扫吞异常.py` 当前统计 **729 处，纯静默 482 处**；`logs/静默.jsonl` 5985 条。
- CWE：CWE-703（异常处理不当）、CWE-778（日志不足）。
- 影响：任务停滞、数据未写、网络失败都可能表现成“什么都没发生”。
- 修复：

```text
新增纯静默即 CI 失败
只允许带上下文/降级动作的 except
将 FileNotFound 的 5 类根因逐条关闭
```

### P1-02 · 幂等缓存无上限

- 证据：`kernel/legacy_runtime/server.py:242` 初始化 `_idem`；`:1817` 写 done 结果；没有 TTL/容量淘汰。
- CWE：CWE-400（资源耗尽）。
- 影响：长时间运行 + 大量唯一 `idempotency_key` 可持续增长。
- 修复：TTL + LRU 上限 + 指标；重放窗口明确写进协议。

### P1-03 · 请求异常统一吞成 E_INTERNAL

- 证据：`kernel/legacy_runtime/server.py:906-910` 捕获所有异常，只返回 code/message。
- CWE：CWE-755（异常处理不当）。
- 影响：真实 bug 没有 traceback/请求上下文，审计链也看不到内部异常。
- 修复：客户端仍收 E_INTERNAL，但 kernel 侧写 `request_exception` 审计事件，含 request id、agent、op、异常类型、栈顶。

### P1-04 · 远端审计失败只加计数器

- 证据：`kernel/legacy_runtime/security.py:387-388`。
- CWE：CWE-778。
- 影响：远端审计不可用时没有告警、没有状态暴露。
- 修复：失败写本地审计/指标；连续失败触发显式降级状态；不要静默。

### P1-05 · 测试绿灯但覆盖不完整

- 证据：
  - `tests/body` 已纳入 CI；这是正确方向。
  - JS hand 只有 `node --check`，没有行为测试；也没有 coverage 门槛。
  - 没有 coverage 门槛。
- CWE：CWE-1059（测试覆盖不足）。
- 修复：

```text
CI 加 tests/body
加 JS 单元/模拟 hand 测试
加 coverage 报告和最低门槛
增加随机任务 E2E（至少 stone_pickaxe）
```

### P1-06 · 没有 SCA/SAST/lint/type gate

- 证据：`verify.yml` 只有 compileall + unittest + node --check。
- CWE：CWE-1104（未维护的第三方组件）、CWE-1127（依赖漏洞）。
- 修复：

```text
Python: ruff + mypy（渐进）+ bandit/semgrep
Node: npm audit --omit=dev + eslint
Secret scan: gitleaks/trufflehog
依赖锁定与升级策略
```

### P2-01 · 仓库/运行时体积与日志保留

- 证据：工作区约 **2.3G**；`runtime` 约 1.4G，`logs` 约 649M，单文件 `logs/全程-20261023.jsonl` 202M。
- 风险：备份、审计、泄露面、磁盘耗尽。
- 修复：日志轮转/保留策略；运行时资产移出仓库；`.gitignore` 与发布包分离。

### P2-02 · 单进程、无服务管理

- 证据：启动依赖 `nohup`/手工脚本；无 systemd/supervisor/healthcheck。
- 风险：崩溃后无自动恢复，审计链/任务状态可能半开。
- 修复：systemd unit + restart policy + readiness/liveness + 启动前 socket 清理。

### P2-03 · 原生 Brain/Hand 单体较大

- 证据：`agents/cyberdyne/brain/bridge.py` 约 4.5k 行；插件通过 `setattr` 包装主链。
- 风险：补丁顺序冲突（实机已出现“障碍自愈/够不着自愈都动看回执”警告）。
- 修复：明确补丁点契约/顺序测试；长期拆出任务栈/感知/执行适配层。

### P2-04 · 日志含坐标/玩家/行为数据

- 证据：`logs` 下大量任务、位置、玩家交互日志。
- 修复：脱敏/保留期/访问控制；公开仓库不提交运行日志。

---

## 3. 代码层正向控制

以下不是问题，应保留：

```text
CBAP 默认拒绝
token 文件 0600 + O_NOFOLLOW
SO_PEERCRED / operator token
lease + fencing + estop/resume
审计链 hash + seq + checkpoint
远端审计可选
CBAP 默认执行路径
lease 续租、命令去重、队列
障碍自愈 facts 链
第一镐实机链路
```

---

## 4. 上线/验收门槛

必须全部满足才可移除官网“代码审计中”：

- [ ] RCON 关闭或只 loopback，密码不再是 `cyberdyne`
- [ ] MC 不暴露给不可信网段，或 online-mode/whitelist 正确
- [ ] `/tmp/honeypot` 服务确认/关闭/登记
- [ ] `ufw` 实际启用并复核监听面
- [ ] JS 行为测试、coverage 进入 CI（tests/body 已完成）
- [ ] SAST/SCA/secret scan 进入 CI
- [ ] `_idem` 有 TTL/上限
- [ ] `E_INTERNAL` 有服务端 traceback 审计
- [ ] 远端审计失败有告警
- [ ] 纯静默异常不得新增
- [ ] 随机世界 `stone_pickaxe` 验收通过
- [ ] 官网提示移除与 CI banner gate 同步删除

---

## 5. 建议修复顺序

```text
今天：
1. 关/限 RCON
2. 关/限 25565，确认 online-mode/whitelist
3. 处理 /tmp/honeypot
4. 开 ufw 并复测

本周：
5. JS 行为测试 + coverage 进 CI（tests/body 已完成）
6. ruff/bandit/npm audit/secret scan
7. _idem TTL + E_INTERNAL trace + remote audit alarm
8. 纯静默异常预算

验收前：
9. 随机世界石镐全链路
10. 移除审计提示与 banner gate
```

---

## 6. 最终判定

```text
代码设计：中上
安全控制：有，但部署面有 P0
测试：绿，但覆盖不足
可维护性：中
生产就绪：否
最终 MC 自主验收：否
```

企业级结论：**可以有条件进入受控内测，不能直接对外生产；先处理 3 个部署 P0。**
