# Cyberdyne Bridge / CBAP 代码审计

- 日期：2026-10-26
- 审计对象：CBAP `kernel/legacy_runtime`、MC driver、legacy brain、hand/body、插件编组、测试与配置
- 基线：`b0cb1a7`
- 方式：静态阅读、运行时日志、异常扫描、逐文件 `unittest`、CBAP 安全路径检查
- 结论：**不能把当前状态当成“已验收”**。协议骨架和部分安全闸门是好的，但仍有 P0 级控制面绕过、任务静默停滞和异常可见性问题。
- 进度（2026-10-26 晚，非最终验收）：
  - 官网已挂中英文“代码审计中”提示。
  - `AuditChain` 已补跨进程 `flock`，并发 60 条写入验证 `(True, 'ok')`。
  - CBAP 测试在包模式下 `129/129` 通过（约 119 秒），已加 `.github/workflows/verify.yml`。
  - 热保护挂起现在会显式 `任务.暂停('过热保护')`，恢复时显式恢复。
  - 主链数据目录创建已补；剩余 `FileNotFoundError` 根因和 legacy 路径仍未完成。
  - 实机石井已确认第一镐会下发：wooden_pickaxe 挖 [844,63,-2] -> air，接着 [844,62,-2] -> air。
  - 竖井安全闸门修了两处：有镐子时允许自然石头；竖井允许空气间隔。
  - 挖空守卫现在对已标记 `_陈坐标` 的步骤直接 0.5 秒超时，即使计划步骤没有 `方块` 字段。
  - 新的实机阻塞点：计划第 3 步 [844,61,-2] 是空气，步骤层仍把它当挖点；应过滤空气步骤，避免等待/陈坐标循环。
  - 第二轮实机验证：wooden_pickaxe 已实际挖掉 [844,63,-2] 和 [844,62,-2] stone，任务第一镐链路已打通。
  - 但之后计划换成 [845,63,-2]，挖空守卫仍反复报陈坐标；`_陈坐标` 的 0.5s 超时/`_失败` 包装没有稳定生效，需检查插件包装顺序和任务步骤字段。
  - 第三轮已把陈坐标状态同时写到 **step** 和 **task**，并在 `任务栈.跑()` 核心入口兜底：
    现场 1 秒内出现 `这活我干不了了：陈坐标，重新规划。`，不再无限重试。
  - 第四轮已把“当前已是空气”的挖点，在任务接单时直接标记 `跳过`；不再把空气留给执行/物理体检。
  - 第五轮已加“目标物品任务”的有限自动重规划：陈坐标失败后最多重规划 2 次，新计划仍过全部 fail-closed 闸。
  - 实机 `stone_shaft` 演示任务没有 `目标物品`，因此还不会自动重规划；这是下一步要补的无目标任务路径。
  - 第六轮已让 `stone_shaft` 无目标演示任务也进入有限重规划（最多 2 次）；现场已看到第二次接单。
  - 同时补了“事实完成”闸：计划里有「挖」但 `实际挖 == 0` 时，任务必须失败为 `no_dig`，不能把空动作吹成完成。
  - 仍未完成：实机默认仍走 legacy UDS；重规划后的竖井计划仍可能包含空气/爬升不物理的步骤。
  - 第七轮新增 `CYBERDYNE_CBAP=1` 的原生 hook 模式，实机已成功连到 CBAP Kernel（`bridge-legacy`、fd-1）并通过 CBAP 发出 dig。
  - 同一轮修复了 CBAP adapter 的两处实机断链：
    1) 不在 `连()` 后申请 lease → 30 秒后全部 `write requires a lease`；
    2) `dig` 的 `允许挖脚下` 没进 mapping → 手侧反复拒绝“正脚下那块”。
  - 已实测 CBAP 审计链 `verify() = (True, 'ok')`，`/tmp/cbap-live-audit2.jsonl`。
  - 第八轮已把 `watch_items` / `furnace_watch` 接到 CBAP ioctl；实机任务启动时不再出现“不支持”两条。
  - 实机 CBAP 任务已连续挖掉 [847,62,-2]/[847,61,-2] stone；`/tmp/cbap-live-audit3.jsonl` 仍可 verify。
  - 观察到的剩余 CBAP 噪声：`device max_inflight reached`，重下命令会撞 kernel 的单请求上限；需要 adapter 侧去重/排队，不能让任务把 E_BUSY 当作动作失败。
  - 第九轮已对相同 in-flight 命令做去重；实机连续 dig 不再因同一命令重发撞 `max_inflight`。
  - 第十轮改为**不同命令排队**：一个写请求在飞时，后续 say/dig 等排队，不再直接撞 `max_inflight`；`stop` 仍可插队。
  - 物理体检会跳过已标记 `跳过` 的空气步骤，不再重复报 T1。
  - 完整回归：CBAP `129/129 OK`（约 119s），native `6/6 OK`。
  - 默认启动仍是 legacy，但会明确记 `legacy 直连模式（未启用 CYBERDYNE_CBAP=1）`。
  - 第十一轮实机尝试 `做个石镐`：CBAP 下已拿到 `cobblestone 4` / `diorite 4`，但任务卡在“前面挡着 diorite”的重复 dig 拒绝；服务端背包仍没有 `stone_pickaxe`，因此不构成成功。
  - 第十二轮去掉 adapter 的伪造状态字段：`look`/`friends`/`deaths`/`respawned` 现在从 CBAP 状态帧读取，不再硬编码 0/空。
  - 第十三轮把 legacy hand 的中文机器字段（`先挖`/`挡着`/`未暴露`/`够不着`/`距`…）在 CBAP wire 上映射为 ASCII，再由 adapter 还原，避免障碍自愈丢失 `先挖`。
  - 第十四轮修了更根的一层：CBAP 错误结果把机器字段放在 `facts`，adapter 之前只读 `payload`；现在两者都读。
  - 实机复验：障碍自愈已能读到 `先挖`，现场出现
    `[障碍自愈] 「diorite」@[848,52,-2] 就在手边 ... 直接挖`
    并成功挖掉挡路的 diorite。随后又撞到插入步骤的陈坐标，任务失败；石镐仍未拿到。
  - 第十五轮补了两道生命周期闸：
    - `任务栈.跑()` 每拍发现当前「挖」点已是空气，直接标记跳过；
    - `插进当前活()` 插入前按当前 blocks 事实跳过空气挖点，并把被同一短活清掉的原步骤标记跳过。
  - 实机 `做个石镐` 已连续挖到 `cobblestone 4` / `diorite 13`，障碍自愈连续插入挡路步骤；仍未出现 `stone_pickaxe`。
  - 第十八轮把原生 hook 默认改成 CBAP；legacy 必须显式 `CYBERDYNE_LEGACY=1`。实机启动日志已确认 `CBAP 模式` 与 `接线口连上了`。

---

## 1. 执行摘要

最严重的六件事：

1. **当前实机 DeepSeek 走的是 legacy 直连 UDS，不是 CBAP。**
   CBAP 的 lease、fencing、审计、estop 都没有覆盖这条实机执行路径。
2. **静默异常仍然大量存在。**
   扫描器统计 `725` 处吞异常，其中 `479` 处是纯静默；运行时 `logs/静默.jsonl` 已累计 `5957` 条，几乎全是 `FileNotFoundError`。
3. **任务第一镐没有下发。**
   16 步竖井计划已接单，但 hand 侧 `dig` 次数为 0；`任务栈.跑()` 加了 traceback 后也没有异常。说明不是“挖空守卫拦住了”，而是任务调度/暂停/下发前返回。
4. **CBAP 审计链不是跨进程安全的。**
   `AuditChain` 只有进程内 `threading.Lock`；kernel 和 legacy bridge 可以同时写 `logs/cbap-audit.jsonl`，会破坏 `seq/hash` 链。
5. **CBAP 测试当前已转为绿灯，但验证方式必须统一。**
   包模式 `python -m unittest discover -s tests/cbap`：129/129 通过，约 119 秒。
   ⚠ 直接 `python3 tests/cbap/test_*.py` 仍会因未走 `tests.cbap` 包初始化而出现 policy/路径假红；CI 已统一走包模式。
6. **CI 测试门已新增。**
   `.github/workflows/verify.yml`：Python 编译、CBAP 129 测试、native hand JS 语法检查、审计提示存在性检查。

## 2. P0 / Blocker

### P0-1 实机执行绕过 CBAP 控制面

证据：

```text
agents/cyberdyne/README.md:13
  The brain/hand direct UDS path is legacy and does not go through CBAP.

agents/cyberdyne/brain/bridge.py
  直接 接线口/Unix socket

agents/cyberdyne/brain/bridge_cbap.py
  CBAPHandAdapter 已存在，但当前实机进程没有使用它
```

影响：

```text
lease / fencing / estop / audit 都没有覆盖当前 DeepSeek 的物理动作
“服务端事实”有，但“控制面事实”没有
```

建议：

```text
实机验收统一从 bridge_cbap.py 启动
或在 CBAPHandAdapter 路径上补齐实机验证
legacy 直连只能作为离线调试模式，并在状态中显式标记 legacy=true
```

### P0-2 静默异常洪水

证据：

```text
python3 tools/扫吞异常.py
  合计 725 处吞异常
  纯静默 479 处
  有动作不出声 246 处
  主链 69 处 (旧红线)

logs/静默.jsonl
  5957 条
  5956 条 FileNotFoundError
  主要位置：2035 / 1460 / 1467 / 2912 / 2552 行
```

影响：

```text
第一镐没发、任务暂停、记忆没写、箱子账没写，
都可能表现为“安静地什么都没发生”
```

已做：

```text
bridge.py 的 21 个静默写账点已改为 记静默()
记静默() 现在写 logs/静默.jsonl + logs/cbap-audit.jsonl
```

仍未做：

```text
other modules 仍然有大量 except Exception: pass
FileNotFoundError 的五类根因还没逐条修
```

### P0-3 任务接了单但没有下发第一镐

实机证据：

```text
任务：常识：学主人挖石井
16 步
首步：{"动作":"挖","p":[844,63,-2],"允许挖脚下":true}

hand logs/手.log: dig 次数 = 0
任务栈.跑() traceback: 没有异常
```

结论：

```text
不是挖空守卫
不是坐标截断（已修）
是任务没有真正进入可下发状态，或下发前被暂停/返回 False
```

下一步必须查：

```text
任务.暂停 / 恢复 / 冷静够了
_跑一轮反射 的决策分支
_下发 之前的坐标/状态闸门
```

### P0-4 CBAP 审计链跨进程写竞争

证据：

```text
kernel/legacy_runtime/security.py
  AuditChain.__init__: self._lock = threading.Lock()
  append(): with self._lock:
  # 没有 fcntl / 文件锁

agents/cyberdyne/brain/bridge.py
  记静默(): 使用 logs/.cbap-audit.lock + flock
  # 只保护自己的写，不保护 kernel 的写
```

影响：

```text
两个进程同时 append 会读到同一个 prev/hash
seq 可能重复，hash 链可能断裂
下一次 verify() 会 fail closed，或者审计事实不可信
```

建议：

```text
选一个唯一审计写者（推荐 kernel 提供 audit IPC）
或 AuditChain 全路径统一使用跨进程 flock
禁止任何第二个进程直接打开 cbap-audit.jsonl
```

## 3. P1 / High

### P1-1 CBAP 测试红灯与挂起

已验证（包模式，`PYTHONPATH=.`）：

```text
python3 -m unittest discover -s tests/cbap -p 'test_*.py'
129 tests, 118.940s, OK
```

补充说明：

```text
直接按文件执行 test_*.py 不会加载 tests.cbap 包初始化，
CBAP_TEST_MODE 与测试路径不生效，会产生假红。
CI 必须固定使用 `python -m unittest ...` 或 pytest 的包模式。
```

### P1-2 无 CI 测试门

证据：

```text
.github/workflows/pages.yml
  只部署 site/
```

影响：

```text
测试红灯不会阻止合并
静默异常扫描不会阻止合并
CBAP 安全回归不会阻止合并
```

### P1-3 CBAP 请求异常被统一吞成 E_INTERNAL

证据：

```text
kernel/legacy_runtime/server.py: _handle_request
  except Exception as e:
      self._result(... E_INTERNAL ...)
```

影响：

```text
真正的 bug 只剩一个 E_INTERNAL，没有 traceback / audit 细节
```

建议：

```text
保留客户端 E_INTERNAL
同时写 kernel_error / request_exception 审计事件
记录异常类型、栈顶、request id、agent、op
```

### P1-4 幂等缓存无上限

证据：

```text
server.py: self._idem: dict[tuple, dict] = {}
server.py: _finish_pending -> self._idem[p.idem_key] = {...}
```

没有 TTL、没有容量上限、没有清理策略。长时间运行后可被大量唯一 `idempotency_key` 撑大。

### P1-5 审计远端失败静默

证据：

```text
kernel/legacy_runtime/security.py: _remote_worker
  except Exception:
      self._remote_failures += 1
```

影响：

```text
远端审计不可用 / 不 ACK 时，本地只增加一个计数器
没有审计事件、没有告警、没有状态暴露
```

### P1-6 brain_adapter 伪造/硬编码关键事实

证据：

```text
kernel/legacy_runtime/brain_adapter.py: _state_to_legacy
  "hz": 5
  "look": {"yaw": 0.0, "pitch": 0.0}
  "friends": []
  "deaths": 0
  "respawned": False
```

影响：

```text
legacy brain 会把“未知/不支持”当成“已知的 0”
这与“服务端事实优先”直接冲突
```

### P1-7 实机性能与热风险

观察：

```text
CPU 75°C 触发过热挂起
FOV 扫描 128 格 + 木头 1 格步长扫描，5Hz
```

不是协议错误，但会导致任务停摆、扫描过期、测试结论失真。

### P1-8 `allow_from` 语义需要收紧

配置：

```text
agents/cyberdyne/config.json
  m5.allow_from: []
  m6.allow_from: [...]
```

需要确认 `[]` 的语义是“谁都不听”还是“默认允许”。当前实现若把空数组解释成“不限制”，就是权限放大。

## 4. P2 / Medium

1. `tools/扫吞异常.py` 只报告，不阻断；建议作为 CI gate，至少对新增纯静默报错失败。
2. 测试文件依赖 `PYTHONPATH`，没有 `pyproject.toml` / `pytest.ini` / `unittest` 统一入口。
3. `tests/cbap/test_conformance.py` 缺少单测试超时和资源清理。
4. 根目录存在大量 `.bak-*`、`__pycache__`、历史日志，仓库 2.8G；容易误读/误提交。
5. `AuditChain.append` 对审计数据行没有 `fsync`，只对 checkpoint 做 `fsync`；崩溃窗口内最后一条审计可能丢失。
6. `brain_adapter.发` 没有显式传 `fencing_token`；目前靠 `_op_write` 查 lease 兜底，但客户端缺少 fence 语义，迁移时容易误用。
7. CBAP `TEST_POLICY` 由环境变量 `CBAP_TEST_MODE=1` 触发；需要在生产启动时显式拒绝/告警，防止测试策略误入生产。
8. native hand/body 仍有大量 `catch {}` 和 `except Exception: pass`，与“不许静默”的项目宪法冲突。

## 5. 正向部分（不是全坏）

以下控制是实际存在的：

```text
CBAP 默认策略 default-deny
UDS SO_PEERCRED + token + operator token
token/audit 文件 0600 + O_NOFOLLOW
lease + fencing token
全局/单设备 estop
resume 需要 admin + reason + confirm=RESUME
audit hash chain + checkpoint + 可选 HMAC
TCP 默认只允许 loopback，公网 bind 必须显式 allow_public_bind
测试中 TLS/transport/registry/gateway 等多数组通过
```

语法检查：

```text
Python compileall: 通过
非 node_modules JS --check: 通过
```

## 6. 建议修复顺序

```text
1. 任务第一镐不下发（P0-3）——先让实机能动
2. CBAP 审计单写者 + 文件锁（P0-4）
3. 把实机切到 bridge_cbap 或显式标记 legacy（P0-1）
4. 修 5 类 FileNotFoundError 根因（P0-2）
5. 修 CBAP 测试 policy/挂起，接入 CI（P1-1/P1-2）
6. 清理幂等缓存、远端审计告警、E_INTERNAL 审计（P1-3/4/5）
7. 最后再谈“随机世界完整科技树通过”
```

## 7. 审计判定

```text
协议设计：中上
安全闸门：有，但未覆盖实机路径
错误可见性：不合格
测试可信度：包模式下 129/129 通过，CI 已加；仍需清理直接按文件运行的假红入口
实机自主性：未通过（第一镐未下发）
总体：不可验收，可继续修
```

审计只做了只读检查和报告，没有改动业务逻辑。
