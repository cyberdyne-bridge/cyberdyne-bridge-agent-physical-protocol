# 命名 / Naming

## 层级

```text
CPNC — Critical Protocol: NEKXSR Core / 临界协议：中枢核
└─ CBAP — Agent ↔ 设备控制子协议（当前 v1）
   ├─ CBAP-U：Agent 侧系统调用
   ├─ CBAP Kernel：租约 / 安全 / 审计 / 取消
   └─ CBAP-D：设备侧驱动 ABI
```

## 正式名称

| 项目 | 名称 |
|---|---|
| 项目 / 协议族中文全称 | 临界协议：中枢核 |
| 项目 / 协议族英文全称 | Critical Protocol: NEKXSR Core |
| 项目英文简称 | CPNC |
| 子协议 | CBAP |
| 视觉字标 | NEKXSRCORE |

CPNC 是项目与协议族。CBAP 是 CPNC 下的一个子协议，负责 Agent ↔ 设备控制面；
它不是一个“旧的兼容别名”，也不是 CPNC 的上一级名称。

## 旧名

**Cyberdyne Bridge** 是已停用的旧项目名。CBAP 这个缩写保留下来，作为
CPNC 子协议的代号；历史文档中的 “Cyberdyne Bridge Agent Protocol” 仅用于
解释缩写来源，不再作为项目名使用。

## 技术命名

代码符号、环境变量、历史文件名继续使用 `CBAP` / `cbap`，因为它们属于
CBAP 子协议本身：

- 代码符号：`CBAPClient`、`CBAPError`、`CBAPHandAdapter`；
- 环境变量：`CBAP_*`；
- 线协议字段、内核参数、Unix socket 名称；
- 测试目录、历史契约文件与 Schema `$id`。

不要再写 `CBAP-U` / `CBAP-D` / `CBAP Kernel`；这些层的正确名称是
`CBAP-U` / `CBAP-D` / `CBAP Kernel`。

## 写作约定

- 中文首现：`临界协议：中枢核（CPNC）`。
- 英文首现：`Critical Protocol: NEKXSR Core (CPNC)`。
- 子协议首现：`CBAP 子协议（CPNC 下的 Agent ↔ 设备控制面）`。
- `NEKXSRCORE` 是视觉字标，不是正式英文全称。
- 英文全称使用半角冒号：`Critical Protocol: NEKXSR Core`。
