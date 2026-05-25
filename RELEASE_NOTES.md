# Winlinez Revival 1.0.2

## 中文说明

这是 **Winlinez Revival 1.0.2**。这个版本让 `i` 说明弹窗里的 GitHub 地址变成可点击链接，并补充了作者信息。玩家可以直接从游戏里打开项目主页，确认来源、查看源码或下载新版。

这个项目的起点很简单，也有一点私人：老版本 Winlinez 在新的 Windows 上已经不太能运行了，但家里的父母依然很喜欢玩这个游戏。于是我重新做了一个不需要安装、不需要 Python、拷贝就能玩的版本，尽量保留熟悉的小球连线节奏，同时让界面、按钮和动画更适合现在的电脑。

## 截图

![游戏主界面](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.2/winlinez-revival-game.png)

![中文说明弹窗](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.2/winlinez-revival-help-zh.png)

## 本次更新

- `i` 说明弹窗新增作者信息。
- `i` 说明弹窗里的 GitHub 地址改为可点击链接。
- 点击 GitHub 链接会使用系统默认浏览器打开项目主页。
- README 同步更新为 `v1.0.2` 下载和截图链接。

## 主要特性

- 单文件 Windows 便携版，不需要安装器，也不需要安装 Python。
- 支持中文和英文界面，可用 `En/中` 按钮切换。
- 经典 9x9 小球连线玩法：点击小球，再点击可到达的空格移动。
- 横、竖、斜方向连成 5 个或更多同色小球即可消除。
- 小球移动、选中状态、消除后的补球都有动态效果。
- 保留国王和挑战者角色：当当前分超过最高分时，挑战者升高，国王降低。
- `i` 按钮内置更详细的中文/英文玩法说明。
- 最高分保存在 exe 同目录的 `winlinez_high_score.json`，方便绿色拷贝。

## 下载

推荐下载 `Winlinez-Revival-portable.zip`。解压后运行：

```text
Winlinez-Revival.exe
```

也可以只下载单独的 `Winlinez-Revival.exe`。如果以后想保留最高分，请把同目录生成的 `winlinez_high_score.json` 一起保存或拷贝。

## English

Winlinez Revival 1.0.2 adds author information and a clickable GitHub link to the in-game `i` dialog.

Clicking the GitHub link opens the project page in the system default browser, making it easier to find the source code, releases, and project information from inside the game.

Download `Winlinez-Revival-portable.zip`, extract it, and run `Winlinez-Revival.exe`. No installer or Python installation is required.
