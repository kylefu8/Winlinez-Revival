# Winlinez Revival 1.0.0

## 中文说明

这是 **Winlinez Revival** 的第一个公开版本。它是一个 WinLinez / Color Lines 风格的 Windows 便携复刻版，目标很简单：让那个很多年前的小球连线游戏，在现在的 Windows 上继续顺手地跑起来。

这个版本的起点也很私人：老版本已经不太能运行了，但家里的父母依然很喜欢玩。于是我重新做了一个不需要安装、不需要 Python、拷贝就能玩的版本，尽量保留熟悉的节奏，也让界面和操作更适合现在的电脑。

## 截图

![游戏主界面](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.0/winlinez-revival-game.png)

![中文说明弹窗](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.0/winlinez-revival-help-zh.png)

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

Winlinez Revival is a portable WinLinez / Color Lines style puzzle game for Windows. It was rebuilt because the old game no longer runs reliably on newer Windows systems, while it is still loved at home.

This release provides a self-contained Windows exe, bilingual Chinese/English UI, animated ball movement, classic line-clearing rules, King and Challenger score effects, and local best-score storage beside the exe.

Download `Winlinez-Revival-portable.zip`, extract it, and run `Winlinez-Revival.exe`. No installer or Python installation is required.
