# 提示词工作室 · Image Prompt Studio

面向 Codex 的对话式图像提示词插件。调用后先选择 **MOSS、Krea 2 或 Anima**，再选择规则和任务；已经说明模型和内容时可以直接开始。

支持从想法写词、看图反推、扩写改写、失败结果修复、跨模型转换，以及 MOSS 文字与 Layout 排版。使用当前对话模型，不需要另配 LLM API 密钥。

## 可选规则

| 编号 | 模型 | 规则 | 公开包状态 |
|---|---|---|---|
| M1 | MOSS | 官方 Prompt Enhancer | 已内置 |
| M2 | MOSS | Moeblack 社区专项 | 可选，本地按需导入 |
| K1 | Krea 2 | 官方轻量扩写 | 已内置 |
| K2 | Krea 2 | AI-KSK Prompt Suite | 可选，本地按需导入 |
| A1 | Anima | AI-KSK Prompt Crafter | 可选，本地按需导入 |
| A2 | Anima | Yu1Ko 精简与布局 | 已内置 |
| A3 | Anima | 社区 V4 体系，含六个模块 | 已内置 |

默认使用 M1、K1、A2；导入更多规则后可用编号或方案名称切换。各上游规则按需读取，不把多份模板叠加。

## 安装

在支持插件管理的 Codex CLI 中运行：

```shell
codex plugin marketplace add cOkieeman/image-prompt-studio
codex plugin add image-prompt-studio@image-prompt-studio
```

然后在新消息或新聊天中检查插件；若应用列表尚未刷新，重启应用。插件显示名为 **提示词工作室**。也可以在应用的插件管理界面中从已添加的市场安装。

## 使用

```text
使用 $image-prompt-studio，显示菜单。

用提示词工作室，MOSS，写一个雨夜便利店场景。

A2，Anima Aesthetic，帮我反推这张参考图。

K1，把这段提示词扩写一下，保留人物、服装和构图。

同一个画面，分别给我 MOSS、Krea 2、Anima 三版。
```

参考图请直接附在消息中。生成结果可复制到 ComfyUI 对应文本条件节点；本插件不会因请求提示词而自动提交生图、训练或修改工作流。

## 可选规则

M2 使用 CC BY-NC-ND 4.0，K2 与 A1 的检查快照没有独立许可证。公开仓库提供其来源与导入器，不捆绑这三套正文。导入后的文件只保存在本地，并被 Git 忽略。

选择一个未导入方案时，插件会从原仓库取得规则。也可以在插件目录内手动运行（Python 3.11+，仅标准库）：

```shell
python scripts/import_rulepacks.py --list
python scripts/import_rulepacks.py M2 K2 A1
```

使用 uv 时可以将上述 python 命令替换为 `uv run scripts/import_rulepacks.py ...`。导入器会保留上游文件，不覆盖已有规则，也不执行下载内容。使用条件以各上游声明为准。

## 项目结构与校验

- `.agents/plugins/marketplace.json`：GitHub 市场入口。
- `plugins/image-prompt-studio/`：可安装插件。
- `skills/image-prompt-studio/`：唯一菜单与路由入口，位于插件目录下。
- `rulepacks/`：原样保留的第三方规则，位于插件目录下。

```shell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 plugins/image-prompt-studio/rulepacks/moss-image-prompt-enhancer/scripts/test_compile_prompt.py
```

源码入口、导入器与打包文件采用 MIT；内置第三方规则保留 Apache-2.0 或 MIT 许可，详见 [第三方来源与许可](plugins/image-prompt-studio/THIRD_PARTY_NOTICES.md)。代码和格式校验不代表已验证出图效果。
