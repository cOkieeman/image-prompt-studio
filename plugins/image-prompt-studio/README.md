# 提示词工作室

调用 `$image-prompt-studio` 或在对话中说“使用提示词工作室，显示菜单”。

支持 MOSS、Krea 2 和 Anima，共七个规则选项。公开包直接包含 M1/K1/A2/A3，M2/K2/A1 可从原作者仓库本地导入。完整选项见 [方案目录](skills/image-prompt-studio/references/catalog.md)。

可用任务：从想法写词、看图反推、扩写改写、根据失败图修复、跨模型转换、文字排版。模型与任务已经明确时跳过菜单。

可选包导入：`python scripts/import_rulepacks.py M2 K2 A1`；查询状态：`python scripts/import_rulepacks.py --list`。Python 3.11+，无第三方依赖。导入内容不覆盖已有文件，也不会自动执行。

本插件使用当前聊天模型，不需要单独的 LLM 服务。生图、训练或修改 ComfyUI 必须另有用户请求。

项目主页与安装说明：[cOkieeman/image-prompt-studio](https://github.com/cOkieeman/image-prompt-studio)。来源与许可：[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
