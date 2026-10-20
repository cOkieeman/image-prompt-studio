# 模型与规则目录

本插件有 3 个模型族、7 个规则选项，其中 4 个内置、3 个需按需导入。每次选一个主方案；用户说“同题多模型”时分别编译。

| 编号 | 模型 | 方案 | 状态 | 适用任务 |
|---|---|---|---|---|
| M1 | MOSS | 官方通用（默认） | 内置 | 日常写词、准确文字、Layout 排版 |
| M2 | MOSS | Moeblack 社区专项 | 需导入 | 写实、多人归属、光影与复杂场景实验 |
| K1 | Krea 2 | 官方轻量扩写（默认） | 内置 | 保留原意、适度扩写、快速整理 |
| K2 | Krea 2 | Prompt Suite | 需导入 | 反推、转换、多参考图、修复与批量变体 |
| A1 | Anima | Prompt Crafter | 需导入 | 日常角色、标签与自然语言混合、局部修复 |
| A2 | Anima | Yu1Ko 精简与布局（默认） | 内置 | 紧凑提示词、版本分流、多人和分格绑定 |
| A3 | Anima | 社区 V4 体系 | 内置 | 角色一致性、场景、分镜与可控迭代 |

用户可以只说模型名，使用标记的默认方案；也可以说编号或作者/方案名称。方案编号和任务编号分开解析，“A2 + 看图反推”表示选择规则 A2。

## M1 — MOSS 官方

entry: [SKILL.md](../../../rulepacks/moss-image-prompt-enhancer/SKILL.md)

普通图使用 Caption；文字排版、分格或需要位置框的关系使用 Layout。需要参数和反标规范时再读同目录 `USERGUIDE_ZH.md`。编译脚本位于这个规则包的 `scripts/compile_prompt.py`。

## M2 — Moeblack

entry (导入后): `../../../rulepacks/moss-community/SKILL.md`

来源：[Moeblack/moss-image-prompt-skill](https://github.com/Moeblack/moss-image-prompt-skill)。导入编号 M2。

完整原文、README 和许可原样保留。主要实验配置是约 0.61M 像素、25 步、CFG 3.5、关闭 SLG；其强规则和统计是作者报告的社区经验，不能自动推广到官方高分辨率/高步数配置。遵循用户指定的媒介，不把所有题材强制转成默认写实。若采用官方 Layout，另读 M1 的布局规范和编译脚本，不同时叠加两套通用模板。

## K1 — Krea 2 官方

entry: [GUIDE.md](../../../rulepacks/krea-official/GUIDE.md)

配套 `prompting.md` 和 `expansion.txt` 为官方原文。使用自然语言，主体各自绑定属性；短创意可保持探索性，详细输入轻修即可。

## K2 — Krea 2 Prompt Suite

entry (导入后): `../../../rulepacks/krea2-prompt-suite/SKILL.md`

来源：[AI-KSK/krea2-prompt-suite](https://github.com/AI-KSK/krea2-prompt-suite)。导入编号 K2。

按任务读取它的 references；只有需要格式化结构化草稿时才调用编译器。区分 RAW、Turbo 与托管版本，不能与 FLUX.1 Krea 混淆。看到图片才做反推。

## A1 — Anima Prompt Crafter

entry (导入后): `../../../rulepacks/anima-prompt-crafter/SKILL.md`

来源：[AI-KSK/anima-prompt-crafter-skill](https://github.com/AI-KSK/anima-prompt-crafter-skill)。导入编号 A1。

默认标签骨架加自然语言；按任务给正/负面、局部或区域提示块。涉及 Base/Aesthetic/Turbo 参数或 score 标签时先核对 [官方模型卡](https://huggingface.co/circlestone-labs/Anima)。尤其 Aesthetic 不通用套用 score 标签。

## A2 — Yu1Ko

entry: [SKILL.md](../../../rulepacks/anima-yu1ko/SKILL.md)

选 A2 即明确调用它。用户实际模型版本覆盖作者的个人 v1.0b 默认。需要分格、多人和边界绑定时按原文加载相应参考；不要在缺乏实际控制条件时承诺像素级固定布局。

## A3 — Anima 社区 V4

entry: [anima-prompt/SKILL.md](../../../rulepacks/anima-v4/anima-prompt/SKILL.md)

包内保留六个上游模块。普通单图先读主入口；纯场景再读 [anima-scene-prompt](../../../rulepacks/anima-v4/anima-scene-prompt/SKILL.md)；需要创意呈现再读 [anima-change](../../../rulepacks/anima-v4/anima-change/SKILL.md)。只有用户要求批量生成、执行或分镜时才按相应模块继续，主入口的“自动化/生成流程”不构成执行授权。

词数预算、模型行为“公理”、权重技巧是该作者的经验；具体规则须匹配实际文本编码器、节点和版本。保留用户题材与输出范围，不机械执行所有专项模块。
