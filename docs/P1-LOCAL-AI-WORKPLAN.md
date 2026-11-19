# P1 修复 × 本地 AI 分工与验收方案

- 日期：2026-11-19
- 本地模型：`Qwen3-4B-Instruct-2507-Q4_K_M.gguf`
- 端点：`http://127.0.0.1:8099/v1`
- 上下文：4096 tokens
- 统一验收人：主 Agent（本会话）
- 结论：**可以让本地模型做 P1 的“候选补丁/测试/分类”，不能让它自己验收或直接合并。**

---

## 1. 模型能力边界

### 适合交给本地模型

```text
单文件、100~200 行以内的局部修改
测试用例生成
异常分类/去重
文档/注释补全
简单重构
把失败日志整理成问题清单
```

### 不适合交给本地模型

```text
RCON/防火墙/online-mode 等部署安全决策
lease/fencing/estop 的语义改动
审计链/幂等缓存的数据一致性核心
跨模块并发和生命周期
最终合并与验收
```

原因：4B 模型的能力足够做“候选”，不足以为安全关键路径负责；且 4096 上下文装不下 4.5k 行 `bridge.py`。

---

## 2. P1 任务拆分

| ID | 任务 | 风险 | 本地模型可做 | 验收人 |
|---|---|---|---|---|
| P1-A | `_idem` TTL + 容量上限 + 重放测试 | 中 | 生成测试/初稿 | 主 Agent |
| P1-B | `request_exception` 审计事件（含 traceback） | 中 | 生成测试/初稿 | 主 Agent |
| P1-C | 远端审计失败计数、状态、告警事件 | 中 | 生成测试/初稿 | 主 Agent |
| P1-D | 482 处纯静默异常分类 | 低 | 分类/建议 | 主 Agent 复核 |
| P1-E | JS 纯函数行为测试 + coverage | 中 | 生成测试 | 主 Agent |
| P1-F | CI 加 ruff/bandit/npm audit/secret scan | 低 | 配置草案 | 主 Agent |
| P1-G | `tests/body` 已进 CI | 已做 | 不需要 | 已验收 |

### 推荐顺序

```text
第一批（低风险、可快速验收）
  P1-F CI 静态检查
  P1-D 静默异常分类

第二批（核心但范围小）
  P1-A _idem TTL
  P1-B E_INTERNAL trace
  P1-C 远端审计失败

第三批（测试工程）
  P1-E JS 行为测试 + coverage
```

---

## 3. 本地模型任务包格式

每个任务必须给模型一个**封闭包**，而不是整个仓库：

```text
目标：只改 X，不改 Y
输入：函数/测试片段 + 现有测试约定
输出：unified diff 或单文件补丁
约束：不新增依赖、不改运行配置、不碰密钥
验收：必须给出新增测试和运行命令
```

禁止：

```text
“帮我重构整个项目”
“帮我修安全”
“直接给我最终代码，不用测试”
```

---

## 4. 统一验收流程

每个 AI 候选补丁都走同一套闸：

```text
1. 在独立 worktree/分支生成候选
2. 主 Agent 审查 diff：
   - 范围是否只碰目标文件
   - 是否新增静默异常
   - 是否改运行配置/密钥
3. 先跑新增测试，确认能红/能绿
4. 跑回归：
   - CBAP 136
   - MCP 27
   - Native 7
   - Body 5
5. 跑审计：
   - AuditChain.verify() == True
   - 不新增纯静默异常
6. 主 Agent 写入正式分支
7. 提交前再跑 CI 等价命令
```

### P1-A 的专项验收

```text
TTL 到期后缓存被清理
容量超限按 LRU/TTL 淘汰
pending 状态不会被错误重放
done 重放仍返回原结果
并发同 key 仍 E_BUSY
```

### P1-B 的专项验收

```text
E_INTERNAL 仍返回给客户端
服务端 audit 出现 request_exception
事件含 request id / op / agent / exception type / traceback
不把 traceback 泄露给客户端
```

### P1-C 的专项验收

```text
远端 sink 失败 -> 本地可见事件/指标
连续失败达到阈值 -> degraded 状态
恢复后状态回正
不阻塞主写入链路
```

### P1-D 的专项验收

```text
只做分类，不直接批量改代码
每类给根因/建议/风险
主 Agent 按类分批修改
扫描器纯静默数量不得上升
```

---

## 5. 本地模型试点结果

已实际调用本机 Qwen：

```text
端点：http://127.0.0.1:8099/v1/chat/completions
模型：Qwen3-4B-Instruct-2507-Q4_K_M.gguf
```

试点任务：为 `_ascii_extra` 生成 unittest。

模型输出了可读的测试草稿，覆盖：

```text
中文键映射
未知键保持
输入不被修改
```

结论：**可以做“测试草稿/候选补丁”，但需要主 Agent 转成项目 unittest 风格并实际运行，不能直接合并。**

---

## 6. 不建议交给本地模型的部分

```text
P0-01 RCON 暴露
P0-02 online-mode / whitelist
P0-03 /tmp/honeypot
lease/fencing/estop 语义
审计链跨进程锁
生产部署与防火墙
最终验收
```

这些由主 Agent + 人工决策负责。

---

## 7. 下一步

先做两个低风险任务验证流水线：

```text
1. P1-F：CI 静态检查草案
2. P1-D：静默异常分类
```

流水线稳定后，再把 P1-A/B/C 交给本地模型出候选，主 Agent 统一验收。

验收报告：

```text
docs/ENTERPRISE-CODE-REVIEW-2026-11-19.md
```
