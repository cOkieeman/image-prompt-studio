# 第三方来源与许可

记录日期：2026-10-20。菜单、路由、打包、导入器与测试为本项目新增内容；下列规则继续归原作者所有，不标为本项目原创。

## 随公开包原样保留

| 方案 | 来源 | 许可文件 |
|---|---|---|
| M1 | [OpenMOSS/MOSS-Image](https://github.com/OpenMOSS/MOSS-Image/tree/main/skills/moss-image-prompt-enhancer) | [Apache-2.0](rulepacks/moss-image-prompt-enhancer/LICENSE) |
| K1 | [krea-ai/krea-2](https://github.com/krea-ai/krea-2/tree/main/docs) 的 prompting.md、expansion.txt | [Apache-2.0](rulepacks/krea-official/LICENSE.md) |
| A2 | [Yu1Ko/Anima-Prompt](https://github.com/Yu1Ko/Anima-Prompt) | [MIT，Copyright 2026 Yu1Ko](rulepacks/anima-yu1ko/LICENSE) |
| A3 | [adventyhwh/comfy-anima-skill-share/v4](https://github.com/adventyhwh/comfy-anima-skill-share/tree/main/v4) 六个模块 | [MIT，Copyright 2026 adventyhwh](rulepacks/anima-v4/LICENSE) |

M1 同目录的 USERGUIDE_ZH.md 来自 OpenMOSS；共用 moss-recaptioner.txt 逐字摘自该指南的 Caption Prompt。K1 的 GUIDE.md 为本项目新增入口；prompting.md、expansion.txt 和 LICENSE.md 为上游文件。

## 仅列目录，用户按需本地取得

| 方案 | 来源 | 本次检查情况 |
|---|---|---|
| M2 | [Moeblack/moss-image-prompt-skill](https://github.com/Moeblack/moss-image-prompt-skill) | 作者声明 CC BY-NC-ND 4.0；正文、README、CHANGELOG 和 LICENSE 不在公开包中 |
| K2 | [AI-KSK/krea2-prompt-suite](https://github.com/AI-KSK/krea2-prompt-suite) | 检查快照未附独立许可证，未在公开包中复制正文 |
| A1 | [AI-KSK/anima-prompt-crafter-skill](https://github.com/AI-KSK/anima-prompt-crafter-skill) | 检查快照未附独立许可证，未在公开包中复制正文 |

导入器仅下载到用户本地并保留原文；这些路径被仓库 .gitignore 排除。本项目 MIT 许可不改变第三方条款，也不授予这些可选包的再分发许可。
