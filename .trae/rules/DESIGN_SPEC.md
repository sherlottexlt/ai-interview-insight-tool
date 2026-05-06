---
alwaysApply: false
---
# InsightFlow AI 设计规范

# InsightFlow AI 设计规范 v1.0

> 本文档基于「项目看板 / 访谈文本输入 / 结构化洞察 / 多访谈洞察 / RICE 优先级 / 报告导出」六个界面的截图提炼，面向 Streamlit + 自定义 CSS 的复刻场景。可直接被 AI 编码工具（如 Trae）作为上下文引用。
> 

<aside>
📌

**使用方式**：将本文导入 Trae 等 AI IDE，在生成 Streamlit 页面时让模型严格遵循下方的 Design Tokens、组件规范和 CSS 实现。所有颜色、间距、组件类名均已统一。

</aside>

---

## 1. 设计风格总结

- **整体风格**：现代 SaaS Dashboard，干净、轻量、信息密度适中。
- **视觉语言**：白色卡片 + 极浅灰底；少量彩色图标和状态标签提供视觉引导。
- **重点元素**：
    - 主操作按钮：**深色实心**（页面级操作）或**紫蓝渐变**（AI 触发型操作）。
    - 数据指标卡：淡彩色图标背景（蓝/红/绿/紫）做分类区分。
    - 圆角统一中等（8–12px），无强阴影或仅极轻阴影，整体偏「扁平 + 微立体」。
- **气质**：专业、克制、AI 感（紫蓝渐变是品牌锚点）。

---

## 2. Design Tokens（CSS 变量集中表）

所有颜色、尺寸唯一来源。其它组件 CSS 必须通过 `var(--xxx)` 引用，不要写死色值。

```css
:root{
	/* === Surfaces === */
	--bg:           #F7F8FA;
	--card:         #FFFFFF;
	--surface-2:    #F8FAFC;
	--divider:      #F1F5F9;
	--border:       #E5E7EB;
	--border-strong:#CBD5E1;

	/* === Text === */
	--text:         #0F172A;
	--text-2:       #475569;
	--text-3:       #94A3B8;

	/* === Brand === */
	--primary:      #6366F1;
	--primary-2:    #8B5CF6;
	--gradient-ai:  linear-gradient(90deg,#6366F1,#8B5CF6);
	--dark:         #0F172A;

	/* === Semantic === */
	--info:    #2563EB;  --info-bg:    #EFF6FF;
	--success: #059669;  --success-bg: #ECFDF5;
	--warn:    #B45309;  --warn-bg:    #FEF3C7;
	--danger:  #DC2626;  --danger-bg:  #FEF2F2;
	--purple:  #7C3AED;  --purple-bg:  #F5F3FF;

	/* === Priority（紧急度统一） === */
	--p0: #B91C1C; --p0-bg: #FEE2E2;
	--p1: #B45309; --p1-bg: #FEF3C7;
	--p2: #1D4ED8; --p2-bg: #EFF6FF;
	--p3: #475569; --p3-bg: #F1F5F9;

	/* === Chart === */
	--chart-bar:    #3B82F6;
	--chart-grid:   #E5E7EB;
	--chart-anxiety:#F59E0B;
	--chart-confuse:#3B82F6;
	--chart-expect: #10B981;
	--chart-stress: #EF4444;

	/* === Radius / Spacing / Shadow === */
	--r-sm: 6px; --r: 8px; --r-md: 10px; --r-lg: 12px; --r-pill: 999px;
	--shadow-card: 0 1px 2px rgba(15,23,42,.04);

	/* === Type === */
	--font: "PingFang SC","Microsoft YaHei","Inter",system-ui,-apple-system,sans-serif;
}
```

---

## 3. 色彩系统

### 3.1 基础色

| 用途 | Token | 取值 |
| --- | --- | --- |
| 页面背景 | `--bg` | `#F7F8FA` |
| 卡片背景 | `--card` | `#FFFFFF` |
| 次级表面（表头/场景项底） | `--surface-2` | `#F8FAFC` |
| 分隔线（行间） | `--divider` | `#F1F5F9` |
| 边框 | `--border` | `#E5E7EB` |
| 强边框（hover） | `--border-strong` | `#CBD5E1` |

### 3.2 文本色

| 用途 | Token | 取值 |
| --- | --- | --- |
| 主文本（标题/数值） | `--text` | `#0F172A` |
| 次文本（正文） | `--text-2` | `#475569` |
| 辅助文本（占位符/说明） | `--text-3` | `#94A3B8` |

### 3.3 品牌色

| 用途 | Token | 取值 |
| --- | --- | --- |
| 品牌主色 | `--primary` | `#6366F1` |
| 品牌副色 | `--primary-2` | `#8B5CF6` |
| AI 渐变 | `--gradient-ai` | `linear-gradient(90deg,#6366F1,#8B5CF6)` |
| 深色按钮 | `--dark` | `#0F172A` |

### 3.4 语义色

| 语义 | 文字 | 背景 | 用途 |
| --- | --- | --- | --- |
| info（蓝） | `#2563EB` | `#EFF6FF` | 进行中、信息提示 |
| success（绿） | `#059669` | `#ECFDF5` | 已完成、正向标签 |
| warn（黄） | `#B45309` | `#FEF3C7` | 提示卡、轻警告 |
| danger（红） | `#DC2626` | `#FEF2F2` | 痛点、错误 |
| purple（紫） | `#7C3AED` | `#F5F3FF` | 分析中、紫色主题 |

### 3.5 优先级色（紧急度语义，全站统一）

| 等级 | 文字 | 背景 |
| --- | --- | --- |
| **P0 紧急** | `#B91C1C` | `#FEE2E2` |
| **P1 重要** | `#B45309` | `#FEF3C7` |
| **P2 次要** | `#1D4ED8` | `#EFF6FF` |
| **P3 观望** | `#475569` | `#F1F5F9` |

<aside>
⚠️

在所有页面（多访谈洞察机会点列表 / RICE 优先级表）保持同一套 P0–P3 配色，避免歧义。

</aside>

### 3.6 图表色

| 用途 | 取值 |
| --- | --- |
| 柱/条主色 | `#3B82F6` |
| 网格线 | `#E5E7EB`（1px dashed） |
| 情绪-焦虑 | `#F59E0B` |
| 情绪-困惑 | `#3B82F6` |
| 情绪-期待 | `#10B981` |
| 情绪-压力 | `#EF4444` |

---

## 4. 字体规范

字体族：`"PingFang SC", "Microsoft YaHei", "Inter", system-ui, -apple-system, sans-serif`

| 层级 | 字号 | 字重 | 行高 | 颜色 |
| --- | --- | --- | --- | --- |
| 页面标题 | 22–24px | 600 | 1.4 | `--text` |
| 区块标题 | 16–18px | 600 | 1.5 | `--text` |
| 卡片标题 | 14–15px | 500–600 | 1.5 | `--text` |
| 数据大数字 | 28–32px | 700 | 1.2 | `--text` |
| 正文 | 14px | 400 | 1.6 | `--text-2` |
| 辅助文字 | 12–13px | 400 | 1.5 | `--text-3` |
| 表格表头 | 13px | 500 | 1.5 | `--text-2` |
| 标签文字 | 12px | 500 | 1.2 | 见组件 |
| 按钮文字 | 14px | 500–600 | 1 | 白/深 |

建议引入 Inter 字体提升英文/数字观感：

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 5. 间距规范

采用 **4px 基准网格**，常用值：`4 / 8 / 12 / 16 / 20 / 24 / 32 / 40`。

| 场景 | 取值 |
| --- | --- |
| 页面外边距（左右） | 24–32px |
| 卡片内边距 | 20–24px |
| 卡片之间间距 | 16–20px |
| 区块上下间距 | 32–40px |
| 表单字段上下间距 | 16–20px |
| 标签到输入框 | 6–8px |
| 表格行高 | 48–56px |
| 单元格左右 padding | 16px |
| 图标与文字间距 | 8px |
| 按钮高度 / 左右 padding | 36–40px / 16–20px |

---

## 6. 卡片组件

```
背景：var(--card)
边框：1px solid var(--border)
圆角：var(--r-lg) = 12px
阴影：var(--shadow-card) = 0 1px 2px rgba(15,23,42,.04)
内边距：20–24px
hover：边框色 → var(--border-strong)（可选）
```

### 卡片变体

- **指标卡 `.if-metric`**：左文（标签 + 大数字）+ 右图标方块（40×40，圆角 10px，浅彩底+深彩 icon）。
- **项目卡**：标题 + 元信息行 + 进度条（高 6px，圆角 999px）+ 百分比。
- **Section 区块卡 `.if-section`**：白底大卡，承载一整个语义模块（标题在顶部，padding 24px）。
- **提示卡 `.if-tip`**：黄底 `--warn-bg`，圆角 10px，左侧 💡 emoji。
- **公式说明卡 `.if-formula`**：蓝底 `#EFF4FF`，两列 grid 显示术语定义。

---

## 7. 按钮组件

| 类型 | 背景 | 文字 | 边框 | 用途 |
| --- | --- | --- | --- | --- |
| 主按钮（深色） | `var(--dark)` | `#FFF` | none | 页面级主要操作 |
| AI 主按钮（渐变） | `var(--gradient-ai)` | `#FFF` | none | AI 触发型操作 |
| 次按钮（描边） | `#FFF` | `var(--text)` | `1px solid var(--border)` | 上传/取消 |
| 次级填充（导出格式） | `var(--divider)` | `var(--text-2)` | none | Markdown / CSV / Notion |
| 文字按钮 | 透明 | `var(--primary)` | none | 链接型 |
| 行内图标按钮 | 透明 → `var(--divider)` | `var(--text-3)` → `var(--text)` | none | 表格 ✎ 编辑 |

通用属性：

- 高度 40px（主）/ 38px（次）/ 36px（小）
- 圆角 8–10px
- 字号 14px / 字重 500
- 带图标按钮：图标 16px，与文字间距 6–8px
- hover：主按钮亮度 +5%；渐变按钮 opacity 0.92；次按钮边框转 `--border-strong`

---

## 8. 标签 / 胶囊 / 徽章

### 8.1 状态标签 `.if-tag`

```
高度：22–24px / padding 2–4px 8–10px
圆角：6px（方角）
字号：12px / 500
```

| 状态 | class | 文字色 | 背景色 |
| --- | --- | --- | --- |
| 已完成 | `.tag-done` | `--success` | `--success-bg` |
| 分析中 | `.tag-running` | `--purple` | `--purple-bg` |
| 信息 | `.tag-info` | `--info` | `--info-bg` |
| 警示 | `.tag-warn` | `--danger` | `--danger-bg` |

### 8.2 计数徽章 `.if-count`

胶囊形（圆角 999px），用于「8 次」等次数显示。背景 `#EFF4FF`，文字 `#4F46E5`，12px / 500。

### 8.3 需求标签胶囊 `.if-pill`

胶囊形，三档尺寸（用于词云）：

- `.sm`：padding 4px 12px / 13px / 500
- `.md`：padding 6px 16px / 15px / 600
- `.lg`：padding 8px 20px / 17px / 600

背景 `#EEF2FF`，文字 `#4F46E5`。

### 8.4 优先级胶囊 `.if-priority.p0/p1/p2/p3`

胶囊形，22px 高，padding 2px 10px，12px / 500，配色见 §3.5。

---

## 9. 表格组件

### 9.1 标准列表表格

用于「项目看板 - 最近分析」等：

```
容器：白底卡片 / 1px solid var(--border) / 圆角 12px
表头背景：#FFF / 字 13px / 500 / var(--text-2) / 下边框 1px var(--border)
单元格：14px / 400 / var(--text) / 行高 48–56px / 左右 padding 16px
行间分隔：1px var(--divider)
状态列：嵌入 .if-tag
```

### 9.2 数值表 `.if-table-numeric`

用于 RICE 评分表等数值密集场景：

- 表头背景使用 `--surface-2`，与白底列表表格区分。
- **数字列必须**：`font-variant-numeric: tabular-nums; text-align: right;`
- 文本列左对齐，状态/操作列居中。
- 表格右上可放公式注释（13px / `--text-2`，乘号用 `×` 字符）。

---

## 10. 数据指标卡

用于项目看板顶部的 4 个数字卡。

```
卡片：白底 / 1px var(--border) / 圆角 12px / padding 20px
左侧：
	标签：14px / 500 / var(--text-2)
	大数字：30–32px / 700 / var(--text)
	单位：16px / 400 / 与数字间距 4px
右侧图标块：
	40×40 / 圆角 10px / 浅彩底 + 同色系 20px 图标
	颜色变体：.icon.blue/.red/.green/.purple
栅格：桌面 4 等分；平板 2 等分；移动 1 列
```

---

## 11. 内容块组件

### 11.1 引用块 `.if-quote`（用户原话）

```
背景：#EFF4FF
左边框：4px solid var(--primary)
圆角：8px / padding 12px 14px
左上 ❝ 引号：var(--primary)
正文：14px / 400 / var(--text-2) / 行高 1.6
```

### 11.2 嵌入式机会点 `.if-opp-inline`

绿底块，用于嵌入痛点卡内：

```
背景：var(--success-bg) / 左边框 4px solid #10B981 / 圆角 8px / padding 12px 14px
标题「产品机会点」：12px / 600 / #047857
正文：14px / 400 / #065F46
```

### 11.3 三色机会点卡 `.if-opp.green/blue/purple`

独立 Section 内的整宽彩色卡：

| 类别 | 底色 | 左边框 | 标题色 | 正文色 |
| --- | --- | --- | --- | --- |
| green | `#ECFDF5` | `#10B981` | `#047857` | `#065F46` |
| blue | `#EFF6FF` | `#3B82F6` | `#1D4ED8` | `#1E3A8A` |
| purple | `#F5F3FF` | `#8B5CF6` | `#6D28D9` | `#4C1D95` |

圆角 10px / padding 16px 18px / 卡间距 12px。

### 11.4 痛点卡 `.if-pain`

复合组件：标题行（左标题 + 右严重度）/ 引用块 / 嵌入机会点。

**严重程度圆点组件**：

```
5 个圆点 / 直径 10px / 间距 3px
已点亮：background:#EF4444
未点亮：background:#FEE2E2
右侧文字 "x/5"：12px / 500 / #EF4444
```

### 11.5 用户原话证据 `.if-evidence.blue/purple/red`

左边框彩色（蓝/紫/红）的引用列表，用于按维度区分：

| 主题 | 边框色 | 标题色 |
| --- | --- | --- |
| 关于项目选择 | `#3B82F6` | `#1D4ED8` |
| 关于技术表达 | `#8B5CF6` | `#6D28D9` |
| 关于面试焦虑 | `#EF4444` | `#B91C1C` |

### 11.6 显性 / 隐性需求列表 `.if-need-list`

带项目符号的列表：

- 显性：实心圆点 `var(--text)` / 5px
- 隐性 `.implicit`：实心圆点 `var(--purple)` / 5px

字号 14px / 400 / `var(--text-2)` / 行高 1.8 / 项间距 8px。

### 11.7 使用场景项 `.if-scene`

```
背景：var(--surface-2) / 边框 1px var(--border) / 圆角 10px
padding：14px 16px / 字号 14px
```

### 11.8 用户画像 `.if-profile`

双列键值对：

```
display:grid; grid-template-columns:1fr 1fr; row-gap:20px; column-gap:32px;
键：13px / 500 / var(--text-3)
值：14–15px / 500 / var(--text)
```

### 11.9 情绪倾向卡 `.if-emotion`

4 等分网格，每卡水平居中：

```
标签：13px / 500 / 同色系
百分比：22–24px / 700 / 同色系
圆角：10px / padding 16px
变体：.anxiety / .confused / .expect / .stress
```

### 11.10 阶段分布条 `.if-stage`

横向单行：左标签（80px）+ 中进度条（高 8px，深色填充）+ 右人数（48px 右对齐）。填充宽度按「该项 / 最大值 * 100%」计算。

### 11.11 聚类结果卡 `.if-cluster`

2 列网格，每卡含「标题 + 计数徽章 + 引用 + 嵌入机会点」。

### 11.12 机会点列表项 `.if-opp-item.p0/p1/p2`

按优先级整块上色（不带左边框），用于多访谈洞察的机会点列表：

- p0：绿底（如继续保留状态语义）或红底（统一紧急度后）
- 标题 15px / 600，副信息「优先级：P0」12px / 500

### 11.13 核心发现 `.if-finding`

蓝底块，每行 ✓ 起首的关键陈述：

```
背景：#EFF4FF / 圆角 10px / padding 14px 16px
行：display:flex; gap:8px; ✓ 颜色 #3B82F6
文字：14px / 500 / var(--p2) / 行高 1.7
```

---

## 12. 报告导出页特有：三栏布局 + TOC

### 12.1 三栏布局

```
display:grid;
grid-template-columns: 220px 1fr 260px;
gap: 20px;
max-width: 1280px; margin: 0 auto;
```

### 12.2 报告大纲 TOC `.if-toc`

- 列表项：padding 10px 14px / 圆角 8px / 14px / 500 / `var(--text-2)`
- hover：背景 `var(--divider)`
- **激活项 `.active`**：背景 `var(--dark)` / 文字 `#FFF`
- **子项 `.sub`**：13px / `var(--text-3)` / 左 padding 30px

### 12.3 报告预览区

文档式排版：

- 报告 H1：22px / 700
- 节标题：18px / 700 / 上 24px 下 12px
- 子节标题：15px / 600 / 上 16px 下 8px
- 正文：14px / 400 / `var(--text-2)` / 行高 1.7 / 段距 12px
- 嵌入痛点卡使用 `.if-pain.embedded`（去掉外框 padding）
- 嵌入小型 RICE 表使用 `.if-table-numeric`（仅保留 产品机会点 / RICE 分数 / 优先级 三列）

### 12.4 导出设置面板

- 分组标题：13px / 500 / `var(--text-2)` / 下间距 6px
- 下拉框：38px 高，圆角 8px，边框 `var(--border)`
- 复选框：16×16，圆角 4px，已选填充 `var(--dark)` + 白对勾
- 主按钮整宽，次级按钮（Markdown/CSV/Notion）使用 `.if-btn-secondary`

---

## 13. 数据可视化规范

统一用 **Plotly**，不用 Streamlit 原生图表。

### 13.1 横向条形图（高频痛点）

```python
import plotly.graph_objects as go

fig = go.Figure(go.Bar(
	x=[8,7,6,5,4],
	y=["项目方向不清晰","AI 技术表达困难","简历缺少量化","面试技术焦虑","作品集结构混乱"],
	orientation="h",
	marker=dict(color="#3B82F6"),
))
fig.update_layout(
	margin=dict(l=10,r=10,t=10,b=10), height=260,
	plot_bgcolor="#fff", paper_bgcolor="#fff",
	xaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False,
				   tickfont=dict(color="#94A3B8", size=12)),
	yaxis=dict(autorange="reversed",
				   tickfont=dict(color="#334155", size=14)),
	bargap=0.45,
)
```

### 13.2 纵向柱状图（RICE 分数）

```python
fig = go.Figure(go.Bar(
	x=names_truncated, y=scores,
	marker=dict(color="#3B82F6"),
	hovertext=names_full, hoverinfo="text+y",
))
fig.update_layout(
	margin=dict(l=10,r=10,t=10,b=10), height=300,
	plot_bgcolor="#fff", paper_bgcolor="#fff",
	yaxis=dict(range=[0,16], dtick=4, gridcolor="#E5E7EB", griddash="dash",
				   tickfont=dict(color="#94A3B8", size=12), zeroline=False),
	xaxis=dict(tickfont=dict(color="#475569", size=12)),
	bargap=0.5,
)
```

### 13.3 饼图 / 环形图（情绪分布）

```python
fig = go.Figure(go.Pie(
	labels=["焦虑","困惑","压力","期待"],
	values=[35,30,20,15],
	marker=dict(colors=["#F59E0B","#3B82F6","#EF4444","#10B981"]),
	hole=0,  # 0=饼图；0.5=环形
	textinfo="label+percent",
	textfont=dict(size=13),
))
fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=260, showlegend=False)
```

---

## 14. 完整 CSS 实现（可直接落到 Streamlit）

```python
import streamlit as st

st.markdown("""
<style>
/* 1) Tokens */
:root{
  --bg:#F7F8FA; --card:#FFFFFF; --surface-2:#F8FAFC;
  --divider:#F1F5F9; --border:#E5E7EB; --border-strong:#CBD5E1;
  --text:#0F172A; --text-2:#475569; --text-3:#94A3B8;
  --primary:#6366F1; --primary-2:#8B5CF6; --dark:#0F172A;
  --gradient-ai:linear-gradient(90deg,#6366F1,#8B5CF6);
  --info:#2563EB; --info-bg:#EFF6FF;
  --success:#059669; --success-bg:#ECFDF5;
  --warn:#B45309; --warn-bg:#FEF3C7;
  --danger:#DC2626; --danger-bg:#FEF2F2;
  --purple:#7C3AED; --purple-bg:#F5F3FF;
  --p0:#B91C1C; --p0-bg:#FEE2E2;
  --p1:#B45309; --p1-bg:#FEF3C7;
  --p2:#1D4ED8; --p2-bg:#EFF6FF;
  --p3:#475569; --p3-bg:#F1F5F9;
  --r:8px; --r-md:10px; --r-lg:12px; --r-pill:999px;
  --shadow-card:0 1px 2px rgba(15,23,42,.04);
  --font:"PingFang SC","Microsoft YaHei","Inter",system-ui,-apple-system,sans-serif;
}

/* 2) Page */
.stApp{ background:var(--bg); font-family:var(--font); color:var(--text); }
.block-container{ max-width:1200px; padding-top:2rem; padding-bottom:2rem; }

/* 3) Cards */
.if-card{ background:var(--card); border:1px solid var(--border); border-radius:var(--r-lg);
          padding:20px; box-shadow:var(--shadow-card); }
.if-section{ background:#fff; border:1px solid var(--border); border-radius:var(--r-lg);
             padding:24px; margin-bottom:20px; }
.if-section-title{ font-size:16px; font-weight:600; color:var(--text); margin-bottom:16px; }
.if-section-title.danger::before{ content:"⊘"; color:var(--danger); margin-right:8px; }

/* 4) Buttons */
.stButton>button{ background:var(--dark); color:#fff; border:none; border-radius:var(--r-md);
                  height:40px; padding:0 18px; font-weight:500; }
.stButton>button:hover{ background:#1e293b; color:#fff; }
.if-btn-ai{ display:inline-flex; align-items:center; gap:8px; background:var(--gradient-ai);
            color:#fff!important; padding:10px 20px; border-radius:var(--r-md);
            font-weight:600; text-decoration:none; }
.if-btn-ai:hover{ opacity:.92; }
.if-btn-secondary{ display:flex; align-items:center; justify-content:center; gap:8px;
                   width:100%; height:38px; background:#F1F5F9; color:#334155;
                   border-radius:var(--r); font-size:14px; font-weight:500;
                   text-decoration:none; }
.if-btn-secondary:hover{ background:#E5E7EB; }
.if-icon-btn{ display:inline-flex; align-items:center; justify-content:center;
              width:24px; height:24px; border-radius:6px; color:var(--text-3); cursor:pointer; }
.if-icon-btn:hover{ background:var(--divider); color:var(--text); }

/* 5) Metrics */
.if-metric{ display:flex; justify-content:space-between; align-items:flex-start; }
.if-metric .label{ color:var(--text-2); font-size:14px; font-weight:500; }
.if-metric .value{ font-size:30px; font-weight:700; margin-top:8px; }
.if-metric .unit{ font-size:16px; font-weight:400; margin-left:4px; }
.if-metric .icon{ width:40px; height:40px; border-radius:var(--r-md);
                  display:flex; align-items:center; justify-content:center; font-size:20px; }
.icon.blue{ background:var(--info-bg); color:var(--info); }
.icon.red{ background:var(--danger-bg); color:var(--danger); }
.icon.green{ background:var(--success-bg); color:var(--success); }
.icon.purple{ background:var(--purple-bg); color:var(--purple); }

/* 6) Tags / Pills */
.if-tag{ display:inline-block; padding:2px 10px; border-radius:var(--r); font-size:12px; font-weight:500; }
.tag-done{ background:var(--success-bg); color:var(--success); }
.tag-running{ background:var(--purple-bg); color:var(--purple); }
.tag-info{ background:var(--info-bg); color:var(--info); }
.tag-warn{ background:var(--danger-bg); color:var(--danger); }
.if-count{ display:inline-block; padding:2px 10px; border-radius:var(--r-pill);
           background:var(--info-bg); color:#4F46E5; font-size:12px; font-weight:500; }
.if-pill{ display:inline-block; padding:4px 12px; border-radius:var(--r-pill);
          background:#EEF2FF; color:#4F46E5; font-size:13px; font-weight:500;
          margin:0 8px 8px 0; }
.if-pill.sm{ padding:4px 12px; font-size:13px; }
.if-pill.md{ padding:6px 16px; font-size:15px; font-weight:600; }
.if-pill.lg{ padding:8px 20px; font-size:17px; font-weight:600; }
.if-priority{ display:inline-block; padding:2px 10px; border-radius:var(--r-pill);
              font-size:12px; font-weight:500; }
.if-priority.p0{ background:var(--p0-bg); color:var(--p0); }
.if-priority.p1{ background:var(--p1-bg); color:var(--p1); }
.if-priority.p2{ background:var(--p2-bg); color:var(--p2); }
.if-priority.p3{ background:var(--p3-bg); color:var(--p3); }

/* 7) Quote / Opportunity */
.if-quote{ background:#EFF4FF; border-left:4px solid var(--primary);
           border-radius:var(--r); padding:12px 14px; color:#334155; font-size:14px; margin:12px 0; }
.if-quote::before{ content:"❝ "; color:var(--primary); font-weight:600; }
.if-opp-inline{ background:var(--success-bg); border-left:4px solid #10B981;
                border-radius:var(--r); padding:12px 14px; }
.if-opp-inline .t{ font-size:12px; font-weight:600; color:#047857; margin-bottom:4px; }
.if-opp-inline .d{ font-size:14px; color:#065F46; }
.if-opp{ border-radius:var(--r-md); padding:16px 18px; margin-bottom:12px; border-left:4px solid; }
.if-opp .t{ font-size:15px; font-weight:600; margin-bottom:4px; }
.if-opp .d{ font-size:14px; line-height:1.6; }
.if-opp.green{ background:var(--success-bg); border-color:#10B981; }
.if-opp.green .t{ color:#047857; } .if-opp.green .d{ color:#065F46; }
.if-opp.blue{ background:var(--info-bg); border-color:#3B82F6; }
.if-opp.blue .t{ color:#1D4ED8; } .if-opp.blue .d{ color:#1E3A8A; }
.if-opp.purple{ background:var(--purple-bg); border-color:#8B5CF6; }
.if-opp.purple .t{ color:#6D28D9; } .if-opp.purple .d{ color:#4C1D95; }

/* 8) Pain card */
.if-pain{ border:1px solid var(--border); border-radius:var(--r-lg); padding:20px; margin-bottom:16px; }
.if-pain.embedded{ border:none; padding:8px 0 16px; margin-bottom:0; }
.if-pain-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.if-pain-title{ font-size:15px; font-weight:600; }
.if-severity{ display:inline-flex; align-items:center; gap:6px; font-size:12px; color:var(--text-3); }
.if-severity .dots{ display:inline-flex; gap:3px; }
.if-severity .dot{ width:10px; height:10px; border-radius:var(--r-pill); background:#FEE2E2; }
.if-severity .dot.on{ background:#EF4444; }
.if-severity .score{ color:#EF4444; font-weight:500; }

/* 9) Lists & needs */
.if-scene{ background:var(--surface-2); border:1px solid var(--border); border-radius:var(--r-md);
           padding:14px 16px; font-size:14px; color:#334155; margin-bottom:12px; }
.if-need-list{ list-style:none; padding:0; margin:0; }
.if-need-list li{ position:relative; padding-left:16px; margin-bottom:8px;
                  font-size:14px; color:#334155; line-height:1.8; }
.if-need-list li::before{ content:""; position:absolute; left:0; top:11px;
                          width:5px; height:5px; border-radius:var(--r-pill); background:var(--text); }
.if-need-list.implicit li::before{ background:var(--purple); }

/* 10) Profile */
.if-profile{ display:grid; grid-template-columns:1fr 1fr; row-gap:20px; column-gap:32px; }
.if-profile .k{ font-size:13px; font-weight:500; color:var(--text-3); margin-bottom:6px; }
.if-profile .v{ font-size:14px; font-weight:500; }

/* 11) Emotion */
.if-emotion-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.if-emotion{ border-radius:var(--r-md); padding:16px; text-align:center; }
.if-emotion .l{ font-size:13px; font-weight:500; }
.if-emotion .v{ font-size:22px; font-weight:700; margin-top:4px; }
.if-emotion.anxiety{ background:var(--warn-bg); color:var(--warn); }
.if-emotion.confused{ background:var(--info-bg); color:var(--info); }
.if-emotion.expect{ background:var(--success-bg); color:var(--success); }
.if-emotion.stress{ background:var(--danger-bg); color:var(--danger); }

/* 12) Stage bar */
.if-stage{ display:flex; align-items:center; gap:12px; margin-bottom:16px; }
.if-stage .label{ width:80px; font-size:14px; font-weight:500; color:#334155; }
.if-stage .track{ flex:1; height:8px; background:var(--divider); border-radius:var(--r-pill); overflow:hidden; }
.if-stage .fill{ height:100%; background:var(--dark); border-radius:var(--r-pill); }
.if-stage .num{ width:48px; text-align:right; font-size:13px; font-weight:500; color:var(--text-2); }

/* 13) Cluster grid + opportunity list */
.if-cluster-grid{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.if-cluster{ border:1px solid var(--border); border-radius:var(--r-lg); padding:16px; background:#fff; }
.if-cluster-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.if-cluster-title{ font-size:15px; font-weight:600; }
.if-opp-item{ border-radius:var(--r); padding:12px 14px; margin-bottom:10px; }
.if-opp-item .t{ font-size:15px; font-weight:600; }
.if-opp-item .meta{ font-size:12px; font-weight:500; margin-top:2px; }
.if-opp-item.p0{ background:var(--p0-bg); }
.if-opp-item.p0 .t{ color:var(--p0); } .if-opp-item.p0 .meta{ color:#DC2626; }
.if-opp-item.p1{ background:var(--p1-bg); }
.if-opp-item.p1 .t{ color:var(--p1); } .if-opp-item.p1 .meta{ color:#D97706; }
.if-opp-item.p2{ background:var(--p2-bg); }
.if-opp-item.p2 .t{ color:var(--p2); } .if-opp-item.p2 .meta{ color:#2563EB; }

/* 14) Numeric table */
.if-table-numeric{ width:100%; border-collapse:separate; border-spacing:0;
  background:#fff; border:1px solid var(--border); border-radius:var(--r-lg);
  overflow:hidden; font-size:14px; }
.if-table-numeric thead th{ background:var(--surface-2); color:var(--text-2);
  font-weight:500; font-size:13px; padding:12px 16px; text-align:left;
  border-bottom:1px solid var(--border); }
.if-table-numeric tbody td{ padding:0 16px; height:56px;
  border-bottom:1px solid var(--divider); font-variant-numeric:tabular-nums; }
.if-table-numeric tbody tr:last-child td{ border-bottom:none; }
.if-table-numeric .num{ text-align:right; }
.if-table-numeric .muted{ color:var(--text-2); }
.if-table-numeric .center{ text-align:center; }
.if-table-caption{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:12px; }
.if-table-caption .formula{ font-size:13px; color:var(--text-2); font-variant-numeric:tabular-nums; }

/* 15) Formula info */
.if-formula{ background:#EFF4FF; border-radius:var(--r-md); padding:16px 20px; margin-top:16px; }
.if-formula .h{ font-size:13px; font-weight:600; color:var(--p2); margin-bottom:8px; }
.if-formula .grid{ display:grid; grid-template-columns:1fr 1fr; row-gap:8px; column-gap:24px; }
.if-formula .grid .k{ font-size:13px; font-weight:600; color:var(--p2); display:inline; }
.if-formula .grid .v{ font-size:13px; color:#334155; display:inline; }

/* 16) Tip */
.if-tip{ background:var(--warn-bg); color:var(--warn); border-radius:var(--r-md);
         padding:12px 14px; font-size:13px; line-height:1.6; }

/* 17) TOC + Report */
.if-toc{ list-style:none; padding:0; margin:0; }
.if-toc li{ padding:10px 14px; border-radius:var(--r); font-size:14px;
            font-weight:500; color:var(--text-2); cursor:pointer; }
.if-toc li:hover{ background:var(--divider); }
.if-toc li.active{ background:var(--dark); color:#fff; }
.if-toc li.sub{ font-size:13px; color:var(--text-3); padding-left:30px; font-weight:400; }
.if-toc li.sub:hover{ background:var(--surface-2); color:var(--text-2); }

.if-finding{ background:#EFF4FF; border-radius:var(--r-md); padding:14px 16px; }
.if-finding .row{ display:flex; gap:8px; align-items:flex-start;
                  font-size:14px; font-weight:500; color:var(--p2);
                  line-height:1.7; margin-bottom:6px; }
.if-finding .row::before{ content:"✓"; color:#3B82F6; font-weight:700; }

.if-mini-cluster{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.if-mini-cluster .item{ background:#fff; border:1px solid var(--border);
  border-radius:var(--r); padding:10px 12px; }
.if-mini-cluster .item .t{ font-size:14px; font-weight:600; }
.if-mini-cluster .item .m{ font-size:12px; color:var(--text-3); margin-top:2px; }

/* 18) Inputs */
.stTextInput>div>div>input, .stTextArea textarea,
.stSelectbox>div>div, .stDateInput input{
  border-radius:var(--r-md)!important; border:1px solid var(--border)!important;
  background:#fff!important;
}

/* 19) DataFrame skin */
.stDataFrame{ border:1px solid var(--border); border-radius:var(--r-lg); overflow:hidden; }
.stDataFrame thead tr th{ background:#fff!important; color:var(--text-2)!important;
  font-weight:500!important; font-size:13px!important;
  border-bottom:1px solid var(--border)!important; }
.stDataFrame tbody tr td{ font-size:14px!important; color:var(--text)!important;
  border-bottom:1px solid var(--divider)!important; }
</style>
""", unsafe_allow_html=True)
```

---

## 15. Streamlit 主题配置

`.streamlit/config.toml`：

```toml
[theme]
base = "light"
primaryColor = "#6366F1"
backgroundColor = "#F7F8FA"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#0F172A"
font = "sans serif"
```

---

## 16. 渲染示例片段

### 16.1 数据指标卡（4 等分）

```python
cols = st.columns(4)
metrics = [
	("已分析访谈", 12, "份", "blue", "📄"),
	("识别痛点", 48, "个", "red", "⊘"),
	("需求标签", 26, "个", "green", "🏷"),
	("平均分析耗时", 3, "分钟", "purple", "⏱"),
]
for col,(label,value,unit,color,icon) in zip(cols, metrics):
	col.markdown(f'''
	<div class="if-card if-metric">
	  <div>
	    <div class="label">{label}</div>
	    <div class="value">{value}<span class="unit">{unit}</span></div>
	  </div>
	  <div class="icon {color}">{icon}</div>
	</div>
	''', unsafe_allow_html=True)
```

### 16.2 痛点卡

```python
def render_pain(title, severity, quote, opp):
	dots = ''.join(['<span class="dot on"></span>']*severity
	              + ['<span class="dot"></span>']*(5-severity))
	return f'''
	<div class="if-pain">
	  <div class="if-pain-head">
	    <div class="if-pain-title">{title}</div>
	    <div class="if-severity">严重程度
	      <span class="dots">{dots}</span>
	      <span class="score">{severity}/5</span>
	    </div>
	  </div>
	  <div class="if-quote">{quote}</div>
	  <div class="if-opp-inline">
	    <div class="t">产品机会点</div>
	    <div class="d">{opp}</div>
	  </div>
	</div>'''

st.markdown(render_pain(
	"不知道如何选择 AI 产品经理作品集项目", 5,
	"我不知道作品集应该做什么项目，感觉大家都在做聊天机器人。",
	"提供基于个人背景的项目推荐和作品集结构模板。"
), unsafe_allow_html=True)
```

### 16.3 情绪倾向 4 卡

```python
st.markdown("""
<div class="if-emotion-grid">
  <div class="if-emotion anxiety"><div class="l">焦虑</div><div class="v">65%</div></div>
  <div class="if-emotion confused"><div class="l">困惑</div><div class="v">80%</div></div>
  <div class="if-emotion expect"><div class="l">期待</div><div class="v">45%</div></div>
  <div class="if-emotion stress"><div class="l">压力</div><div class="v">70%</div></div>
</div>
""", unsafe_allow_html=True)
```

### 16.4 需求标签词云

```python
def size_class(freq, mx):
	r = freq / mx
	if r >= 0.7: return "lg"
	if r >= 0.4: return "md"
	return "sm"

tags = [("作品集指导",10),("AI 技术",9),("简历优化",8),("面试准备",8),
        ("项目经验",6),("RAG",5),("Agent",5),("求职焦虑",4)]
mx = max(f for _,f in tags)
html = "".join(f'<span class="if-pill {size_class(f,mx)}">{t}</span>' for t,f in tags)
st.markdown(html, unsafe_allow_html=True)
```

### 16.5 RICE 数值表

```python
rows = [
	("自动提取用户痛点","访谈整理耗时",8,4,0.8,2,12.8,"p0","P0"),
	("自动生成需求标签","需求难以聚类",7,4,0.7,2,9.8,"p0","P0"),
	("自动生成洞察报告","报告整理耗时",6,5,0.8,3,8.0,"p1","P1"),
	("技术简历翻译助手","AI 技术表达困难",7,4,0.7,3,6.5,"p1","P1"),
	("AI 作品集项目推荐","项目方向不清晰",8,5,0.6,4,6.0,"p1","P1"),
	("智能面试模拟训练","面试技术焦虑",5,4,0.6,4,3.8,"p2","P2"),
]

head = "<tr>" + "".join(f"<th>{c}</th>" for c in
	["产品机会点","对应痛点","Reach","Impact","Confidence","Effort","RICE 分数","优先级","操作"]) + "</tr>"
body = ""
for name,pain,r,i,c,e,score,cls,label in rows:
	body += (f'<tr><td>{name}</td><td class="muted">{pain}</td>'
	         f'<td class="num">{r}</td><td class="num">{i}</td>'
	         f'<td class="num">{c}</td><td class="num">{e}</td>'
	         f'<td class="num">{score:.1f}</td>'
	         f'<td class="center"><span class="if-priority {cls}">{label}</span></td>'
	         f'<td class="center"><span class="if-icon-btn">✎</span></td></tr>')
st.markdown(f'<table class="if-table-numeric"><thead>{head}</thead><tbody>{body}</tbody></table>',
            unsafe_allow_html=True)
```

---

## 17. 页面 → 组件映射表

| 页面 | 主用组件 |
| --- | --- |
| 项目看板 | 4 × `.if-metric`  • 项目卡 + 标准列表表格（含 `.if-tag`） |
| 访谈文本输入 | textarea + 复选框 + AI 渐变按钮 + `.if-tip`  • 受访者表单 |
| 结构化洞察 | `.if-section` × N + `.if-profile`  • `.if-scene`  • `.if-pain`  • `.if-emotion`  • `.if-pill`  • `.if-evidence`  • `.if-opp` |
| 多访谈洞察 | 横向条形图 + 饼图 + 词云 `.if-pill`  • `.if-cluster`  • `.if-stage`  • `.if-opp-item` |
| RICE 优先级 | 纵向柱状图 + `.if-table-numeric`  • `.if-priority`  • `.if-formula` |
| 报告导出 | 三栏布局 + `.if-toc`  • 报告预览（嵌入 `.if-pain.embedded` / `.if-finding` / `.if-mini-cluster` / 小型 numeric 表）+ 导出设置面板 |

---

## 18. 复刻原则（给 AI Coding Tool 的硬性约束）

1. **颜色只能从 `:root` tokens 取**，不要凭印象写颜色。
2. **不要使用 Streamlit 原生 widget 样式做关键视觉**（`st.metric` / `st.progress` / `st.bar_chart` 视觉差距大），统一用 HTML class + Plotly。
3. **图表配色严格映射**：柱/条 `#3B82F6`；情绪四色按 `--chart-anxiety/confuse/expect/stress`。
4. **优先级配色全站统一**用 §3.5 紧急度表，不再混用「绿色 = P0」的状态语义。
5. **数字列必须使用** `font-variant-numeric: tabular-nums; text-align: right;`。
6. **乘号用** `×`（U+00D7），不要用字母 `x`。
7. **圆角分级**：胶囊 999px / 大卡 12px / 中等块 10px / 小块 8px / 标签 6px。
8. **字体引入 Inter**（英文/数字），中文用 PingFang SC / Microsoft YaHei。
9. **页面最大宽度 1200px**（报告导出页 1280px），整体居中。
10. **空态、加载态**未在截图中体现，复刻时按相同 token 体系自行扩展，保持视觉语言一致。