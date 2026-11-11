---
name: danlogo-leicastyle
description: >-
  DanLogo · Leica Style 徕卡风格：借鉴徕卡与德国功能主义的设计思想——一个精确、只留本质、一体成形的主体，加上一处有人的温度的签名；签名摘掉，主体依然认得出，几十年不过时。
  按九个阶段推进：简报 → 概念（每轮 5 套）→ 原型（每个概念 ≥3 套）→ 图形精修 → 定稿（定制字 + 配色）→ 体系 → 场景 → 提案 → 总结。
  Use this skill when the user wants to design, redesign, refine, extend or present a logo, wordmark, 标志, 字标, 中英文组合标,
  品牌视觉, VI or brand identity in a Leica-like, German-precision spirit — 徕卡, 德味, 德式, 精密, 精工, 极简, 克制, 工业设计,
  Leica, German design, Braun, Dieter Rams, precision, engineered minimalism — when they name danlogo-leicastyle,
  or when they continue a project whose decisions.md names it. For a logo request that names no style, use it unless another
  installed danlogo style fits better; if several danlogo styles are installed, ask the user which one first.
---

# DanLogo · Leica Style 徕卡风格

> 快门落下的那一声：短、准、轻，然后安静。

danlogo 系列的徕卡风格方向。它规定**气质和质量**，不规定形状、颜色或工艺。它的思想来自徕卡的产品与标志、乌尔姆设计学院与博朗的功能主义、系统识别和制造者印记的传统：高级感来自「准」和「少」，温度来自一处签名。它从 EonPoint 方案 C 反向拆解而来（`cases/`），但每个新品牌都要从自己身上长出新的形。徕卡（Leica）是 Leica Camera AG 的商标，本 skill 与该公司无关。

## 先读

开始任何项目之前，按顺序读完前三章风格章；第四章到第 6 阶段再读：

1. `references/philosophy.md` —— 思想坐标：为什么这样设计
2. `references/style-dna.md` —— 风格基因、旋钮与试金石：看起来是什么气质
3. `references/creative-methods.md` —— 创意方法与防同质化：每次怎么想出新的
4. `references/style-extension.md` —— 风格延展：体系、场景、提案长什么样（第 6–8 阶段）

`references/exemplars.md`（参照作品）和 `cases/index.md`（已用过的母题）**等第 2 阶段列完候选母题再读**，用它们划掉惯性答案和撞题的母题——先读会被它们带着走。完整案例只在需要参照“做到什么程度”时读，并且只借方法、不借形式。其余文件在对应阶段读（见下表）。

## 三层要求

| 层 | 内容 | 能否改变 |
|---|---|---|
| 质量关卡（系列共用） | `references/quality-gates.md` | 每个项目都必须通过 |
| 风格基因（本风格） | `style-dna.md` + `philosophy.md` 的自检 | 默认遵守；用户明确要求调整时照做，并记入 decisions.md |
| 创意自由区 | 母题、签名的落法与形式、成形方式、几何、力度、色温、材料与工艺、构图 | 每个项目重新推导；至少两个“旋钮”与所有已有案例明显不同 |

四句提醒：
- **首先是一个抽象的主体，不是一张图。** 主体是一个完整的几何形——一笔等宽的线，或一块实的面——只由直线和一种（最多两种）半径的圆弧组成，第一眼读成一个精确的图形。它可以同时读出品牌名的首字母，但必须是**元素先于字**：线和弧按比例与基准画出，字母是构造出来的，不是写出来的。不画具体的动物、植物、器物、建筑、风景和人——那会变成图标库里的象形图。（这是本风格对 `quality-gates.md`「首先是图形」的预设例外，经 skill 作者确认；细则见 `style-dna.md` 基因 9。）
- **一个主体加一处签名，别无他物。** 整个标志通常只有两件：主体和签名。一张速写如果要写十几行以上的代码，多半已经太复杂。
- **按气质判断，不按元素判断。** 案例里的具体形状、颜色、工艺都是那个品牌的答案，不是本风格的规定。
- **精确与温度要同时在场。** 只有精确、没有签名，就和任何一家工程公司没有区别；签名只有一处，摘掉它主体仍认得出。签名也不限于案例里的那一种（颜色只是其中之一）。

## 九个阶段

细则、编号规则、出口条件见 `references/workflow.md`。每个阶段都以用户的明确确认结束；用户可以随时回退、增加、修改、合并。

| 阶段 | 做什么 | 每轮产出 | 读 |
|---|---|---|---|
| 1 简报 | 用户提供信息；AI 一次性追问缺口（≤10 问） | 简报卡 | `workflow.md` |
| 2 概念 | 拆名字、挖母题；先出 **9 张极简速写拼成一张图**给用户挑，再把挑中的写成概念卡（本质与签名） | 9 张海选速写 → **5 张概念卡**，可改、可加、可合并 | `creative-methods.md`、`philosophy.md` |
| 3 原型 | 每个锁定概念发散图形；三种签名落法都试；每个原型附摘签名的全黑版；先用黑白；**和案例标志并排看**（对照尺） | **每个概念 ≥3 个原型** + 初步查重 | `style-dna.md`、`craft.md`、`scripts/prim.py` |
| 4 图形 | 精修：基准与比例、公差、视觉修正、小尺寸版、构造图 | 精修图形 | `craft.md`、`quality-gates.md` |
| 5 定稿 | 定制字与配色一起做 | 每个图形 2–3 套“字 + 色”组合 + 完整查重 | `craft.md`、`style-dna.md` |
| 6 体系 | 组合、变色、留白、最小尺寸、错误用法、动态；工艺版本 | SVG / PNG 全套 | `deliverables.md`、`style-extension.md` |
| 7 场景 | 按行业选 6–10 个场景 | 场景示意 | `deliverables.md`、`style-extension.md` |
| 8 提案 | 提报文档 + 演讲备注 + 源文件包 + 查重复查 | 提案 | `deliverables.md`、`style-extension.md`、`adapters/` |
| 9 总结 | 主动询问是否用这个项目优化 skill | 修改建议，用户批准后写入 | `workflow.md` 第 9 节 |

## 贯穿全程

- **项目存档**：每个项目一个文件夹和一份 `decisions.md`（第一行写 `skill: danlogo-leicastyle v<版本>`），记录每轮展示了什么、用户原话、锁定和否定了什么。接手已有项目先读它。
- **结构先行**：第 5 阶段之前以黑白审结构；签名先在黑白里成立（收尾、不对称、切口），颜色只是加强。
- **被否就退回，不加东西**：换母题、换主体或换签名的落法，不在原图上加装饰。
- **查重三次**：原型初查、定稿全查、提案前复查（`quality-gates.md`）。
- **亲眼看渲染图**：判断好不好看，一律基于渲染出的图片，包括 16 px 小图。
- **沟通**：用用户的语言。每轮先一句话说做了什么，再编号列方案和一句话理念，给一个推荐和理由，问锁定、修改还是继续。简短反馈先查 `references/feedback-playbook.md`。
- **客户资料只放在项目文件夹里**，不写进 skill。

## 多个 danlogo 风格并存时

用户点名了某个风格，就用那个 skill。项目的 `decisions.md` 写了用哪个 skill，就沿用。都没有指定、又装了多个 danlogo 风格时，先列出已安装的风格，请用户选，再开始。

## 工具与文件

- `scripts/`：通用工具——几何与 SVG 生成（`geom.py`）、多图对比审看图（`sheet.py`）、SVG 转 PNG（`render.sh`）。说明见 `scripts/README.md`。使用时复制到项目的 `src/`。
- `scripts/prim.py`：本风格专用的画法——由直线和真正的圆弧组成的一笔（等宽描边，也能转成实面）、整件的基本形和签名点；画速写和原型时优先用它，不用 `geom.py` 的 `arc_pts`、`clip_poly` 去切形。它还能列出一个标志的件数和用到的半径（对照尺）。
- `examples/eonpoint-precision/src/`：案例的生成代码。学它的工程写法（一套比例驱动全部尺寸、标准版与小尺寸版），不要复用它的造型和字形。
- `adapters/for-claude.md`、`adapters/for-codex.md`：不同 AI 工具在看图、做演示文稿、预览网页上的差异。
- `evals/briefs.md`：用于检验本 skill 不会把所有品牌做成同一个样子的测试简报。

`references/` 中带 `danlogo-core` 标记的五个文件（workflow、quality-gates、craft、deliverables、feedback-playbook）是 danlogo 系列共用章节，所有风格保持一致；本风格专属的是 philosophy、style-dna、creative-methods、style-extension 四章：前三章管标志本身，第四章管体系、场景和提案的审美，让整套设计和标志出自同一种气质。
