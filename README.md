# Winlinez Revival

**Winlinez Revival** 是一个 WinLinez / Color Lines 风格的 Windows 便携复刻版。

这个项目的起点很简单，也有一点私人：老版本 Winlinez 在新的 Windows 上已经不太能运行了，但家里的父母依然很喜欢玩这个游戏。于是我重新做了一个不需要安装、不需要 Python、拷贝就能玩的版本，尽量保留熟悉的小球连线节奏，同时让界面、按钮和动画更适合现在的电脑。

## 截图

![游戏主界面](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.2/winlinez-revival-game.png)

![中文说明弹窗](https://github.com/kylefu8/Winlinez-Revival/releases/download/v1.0.2/winlinez-revival-help-zh.png)

## 下载

推荐从 GitHub Release 下载：

[下载 Winlinez Revival 1.0.2](https://github.com/kylefu8/Winlinez-Revival/releases/tag/v1.0.2)

便携包里包含：

```text
Winlinez-Revival.exe
README.txt
```

也可以只下载单独的 `Winlinez-Revival.exe`。这个 exe 是自包含的，不需要安装器，也不需要目标电脑安装 Python。

## 玩法

- 点击一个小球，再点击一个可到达的空格，小球会沿通路移动。
- 横、竖、斜方向连成 5 个或更多同色小球即可消除。
- 消除成功会得分；一次消除越多，分数越高。
- 如果本步没有消除，会补入顶部预告的 3 个小球。
- 当当前分超过最高分时，挑战者会升高，国王会降低。

## 操作

- `重开` / `New`：开始新游戏。
- `结束` / `Quit`：退出游戏。
- `N` 或 `F2`：开始新游戏。
- `U` 或 `Backspace`：撤销上一次有效移动。
- `Esc`：退出游戏。
- `En/中`：切换中英文界面。
- `i`：查看游戏说明。

## 版本与项目地址

软件窗口底部会显示当前版本号和 GitHub 仓库地址。也可以点击 `i` 在说明弹窗里查看作者信息，并点击 GitHub 链接打开项目主页。

## 高分记录

最高分会保存在 exe 同目录的 `winlinez_high_score.json`。

如果只是拷贝游戏给别人玩，拷贝 `Winlinez-Revival.exe` 就够了。如果想保留最高分记录，请把 `winlinez_high_score.json` 也一起拷贝。

## 从源码运行

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_winlinez.py
```

## 构建便携版

```powershell
.\scripts\build_portable.ps1
```

构建完成后会生成：

```text
dist\Winlinez-Revival\Winlinez-Revival.exe
dist\Winlinez-Revival-portable.zip
```

## English

Winlinez Revival is a portable WinLinez / Color Lines style puzzle game for Windows.

It was rebuilt because the old Winlinez no longer runs reliably on newer Windows systems, while it is still loved at home. The goal is to keep the familiar puzzle experience easy to run, easy to share, and pleasant to play on modern PCs.

Download the portable package from the [latest release](https://github.com/kylefu8/Winlinez-Revival/releases/tag/v1.0.2), extract it, and run `Winlinez-Revival.exe`. No installer or Python installation is required.
