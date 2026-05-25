# Winlinez Revival 1.0.1

## 中文说明

这是 **Winlinez Revival 1.0.1**。这个版本在软件界面里加入了版本号和 GitHub 仓库信息，方便玩家确认自己运行的是哪个版本，也方便从游戏里找到项目主页。

这个项目的起点很简单，也有一点私人：老版本 Winlinez 在新的 Windows 上已经不太能运行了，但家里的父母依然很喜欢玩这个游戏。于是我重新做了一个不需要安装、不需要 Python、拷贝就能玩的版本，尽量保留熟悉的小球连线节奏，同时让界面、按钮和动画更适合现在的电脑。

## 截图

![游戏主界面](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.1/winlinez-revival-game.png)

![中文说明弹窗](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.1/winlinez-revival-help-zh.png)

## 本次更新

- 主界面底部新增版本号和 GitHub 仓库地址。
- `i` 说明弹窗新增版本信息和完整 GitHub 链接。
- README 同步更新为 `v1.0.1` 下载和截图链接。

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

Winlinez Revival 1.0.1 adds visible version and GitHub repository information inside the app.

The footer now shows the version and repository, and the in-game `i` dialog includes the full GitHub link. This makes it easier for players to identify the build and find the project page.

Download `Winlinez-Revival-portable.zip`, extract it, and run `Winlinez-Revival.exe`. No installer or Python installation is required.
