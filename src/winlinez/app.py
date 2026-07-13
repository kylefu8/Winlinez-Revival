from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
import os
from pathlib import Path
import sys
import webbrowser

import pygame

from . import __version__
from .game import COLORS, Cell, GameState
from .records import HighScoreStore


WINDOW_SIZE = (940, 604)
REPO_URL = "https://github.com/kylefu8/Winlinez-Revival"
REPO_LABEL = "github.com/kylefu8/Winlinez-Revival"
AUTHOR_LABEL = "kylefu8"
APP_TITLE = f"Winlinez Revival v{__version__}"
APP_ICON_FILENAME = "winlinez-icon.png"
FPS = 60
MOVE_MS_PER_CELL = 60
MOVE_MIN_DURATION_MS = 140
CELL_SIZE = 54
BOARD_ORIGIN = (225, 82)
BOARD_SIZE = CELL_SIZE * GameState.cols
LEFT_STAGE = pygame.Rect(16, 82, 207, 486)
RIGHT_STAGE = pygame.Rect(714, 82, 210, 486)

WINDOW_GRAY = (192, 192, 192)
CELL_GRAY = (196, 194, 196)
LIGHT = (242, 242, 242)
MID = (142, 142, 142)
DARK = (42, 42, 42)
INK = (26, 26, 26)
BLUE = (16, 72, 154)
GOLD = (247, 208, 33)
GOLD_DARK = (122, 86, 9)
SILVER = (212, 216, 216)
NEON_GREEN = (83, 244, 78)
BG_TOP = (18, 19, 25)
BG_BOTTOM = (42, 34, 55)
PANEL_BG = (36, 38, 47)
PANEL_BG_2 = (48, 51, 62)
PANEL_BORDER = (94, 101, 118)
CELL_BG = (48, 50, 59)
CELL_HOVER = (58, 61, 72)
CELL_BORDER = (83, 88, 102)
TEXT_LIGHT = (242, 245, 252)
TEXT_MUTED = (178, 184, 197)
ACCENT_CYAN = (54, 220, 255)
ACCENT_MAGENTA = (255, 88, 220)
ACCENT_GOLD = (255, 214, 84)
LINK_BLUE = (111, 213, 255)


@dataclass(frozen=True)
class Button:
    rect: pygame.Rect
    action: str


@dataclass
class MoveAnimation:
    path: list[Cell]
    color_id: int
    started_at: int
    duration_ms: int


@dataclass(frozen=True)
class Theme:
    key: str
    name_zh: str
    name_en: str
    bg_top: tuple[int, int, int]
    bg_bottom: tuple[int, int, int]
    panel_bg: tuple[int, int, int]
    panel_bg_2: tuple[int, int, int]
    panel_border: tuple[int, int, int]
    cell_bg: tuple[int, int, int]
    cell_alt: tuple[int, int, int]
    cell_border: tuple[int, int, int]
    cell_highlight: tuple[int, int, int]
    text_light: tuple[int, int, int]
    text_muted: tuple[int, int, int]
    accent_primary: tuple[int, int, int]
    accent_secondary: tuple[int, int, int]
    accent_gold: tuple[int, int, int]
    link: tuple[int, int, int]


THEMES = (
    Theme(
        key="neon",
        name_zh="霓虹夜",
        name_en="Neon",
        bg_top=BG_TOP,
        bg_bottom=BG_BOTTOM,
        panel_bg=PANEL_BG,
        panel_bg_2=PANEL_BG_2,
        panel_border=PANEL_BORDER,
        cell_bg=CELL_BG,
        cell_alt=(43, 45, 54),
        cell_border=CELL_BORDER,
        cell_highlight=CELL_HOVER,
        text_light=TEXT_LIGHT,
        text_muted=TEXT_MUTED,
        accent_primary=ACCENT_CYAN,
        accent_secondary=ACCENT_MAGENTA,
        accent_gold=ACCENT_GOLD,
        link=LINK_BLUE,
    ),
    Theme(
        key="ocean",
        name_zh="深海蓝",
        name_en="Ocean",
        bg_top=(8, 22, 33),
        bg_bottom=(19, 47, 66),
        panel_bg=(20, 42, 56),
        panel_bg_2=(28, 57, 73),
        panel_border=(63, 116, 137),
        cell_bg=(27, 54, 68),
        cell_alt=(31, 61, 76),
        cell_border=(62, 99, 116),
        cell_highlight=(82, 207, 222),
        text_light=(235, 249, 250),
        text_muted=(157, 193, 201),
        accent_primary=(62, 226, 214),
        accent_secondary=(92, 162, 255),
        accent_gold=(255, 207, 92),
        link=(105, 220, 238),
    ),
    Theme(
        key="amber",
        name_zh="暖金棕",
        name_en="Amber",
        bg_top=(30, 20, 16),
        bg_bottom=(67, 38, 31),
        panel_bg=(55, 38, 32),
        panel_bg_2=(72, 49, 40),
        panel_border=(133, 91, 70),
        cell_bg=(65, 48, 42),
        cell_alt=(73, 53, 45),
        cell_border=(112, 79, 65),
        cell_highlight=(255, 175, 85),
        text_light=(255, 244, 229),
        text_muted=(205, 181, 158),
        accent_primary=(255, 151, 72),
        accent_secondary=(255, 102, 130),
        accent_gold=(255, 210, 105),
        link=(255, 183, 115),
    ),
)


def clamp(value: int) -> int:
    return max(0, min(255, value))


def blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        clamp(round(a[0] + (b[0] - a[0]) * t)),
        clamp(round(a[1] + (b[1] - a[1]) * t)),
        clamp(round(a[2] + (b[2] - a[2]) * t)),
    )


def load_font(size: int, bold: bool = False) -> pygame.font.Font:
    windows_dir = Path(os.environ.get("WINDIR", r"C:\Windows"))
    candidates = (
        windows_dir / "Fonts" / "msyh.ttc",
        windows_dir / "Fonts" / "simhei.ttf",
        windows_dir / "Fonts" / "simsun.ttc",
        windows_dir / "Fonts" / "tahoma.ttf",
        windows_dir / "Fonts" / "segoeui.ttf",
        windows_dir / "Fonts" / "arial.ttf",
    )
    for candidate in candidates:
        if candidate.exists():
            font = pygame.font.Font(str(candidate), size)
            font.set_bold(bold)
            return font

    font = pygame.font.Font(None, size)
    font.set_bold(bold)
    return font


def asset_path(filename: str) -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return root / "assets" / filename


def draw_bevel(surface: pygame.Surface, rect: pygame.Rect, raised: bool = True, fill=None, width: int = 2) -> None:
    if fill is not None:
        pygame.draw.rect(surface, fill, rect)
    for offset in range(width):
        current = rect.inflate(-offset * 2, -offset * 2)
        top_left = LIGHT if raised else DARK
        bottom_right = DARK if raised else LIGHT
        pygame.draw.line(surface, top_left, current.topleft, current.topright)
        pygame.draw.line(surface, top_left, current.topleft, current.bottomleft)
        pygame.draw.line(surface, bottom_right, current.bottomleft, current.bottomright)
        pygame.draw.line(surface, bottom_right, current.topright, current.bottomright)


def draw_vertical_gradient(
    surface: pygame.Surface,
    rect: pygame.Rect,
    top: tuple[int, int, int],
    bottom: tuple[int, int, int],
) -> None:
    height = max(1, rect.height - 1)
    for y in range(rect.height):
        color = blend(top, bottom, y / height)
        pygame.draw.line(surface, color, (rect.x, rect.y + y), (rect.right - 1, rect.y + y))


def draw_round_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int],
    border: tuple[int, int, int],
    radius: int = 12,
    shadow: bool = True,
) -> None:
    if shadow:
        shadow_rect = rect.move(0, 4).inflate(6, 6)
        shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surface,
            (0, 0, 0, 90),
            shadow_surface.get_rect(),
            border_radius=radius + 4,
        )
        surface.blit(shadow_surface, shadow_rect.topleft)

    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, width=1, border_radius=radius)
    pygame.draw.line(
        surface,
        blend(fill, (255, 255, 255), 0.14),
        (rect.x + radius, rect.y + 1),
        (rect.right - radius, rect.y + 1),
    )


def ease_in_out(t: float) -> float:
    return 0.5 - math.cos(t * math.pi) / 2


TEXT = {
    "zh": {
        "best": "最高分",
        "current": "当前分",
        "next": "下组颜色",
        "new": "重开",
        "quit": "结束",
        "theme": "主题",
        "language": "En/中",
        "info": "i",
        "king": "国王",
        "challenger": "挑战者",
        "game_over": "游戏结束",
        "score": "得分：{score}",
        "restart_hint": "按 N/F2 或点“重开”",
        "info_title": "Winlinez Revival",
        "ok": "确定",
        "status_select_ball": "请选择小球",
        "status_choose_destination": "请选择目标格",
        "status_no_path": "没有通路",
        "status_moving": "移动中",
        "status_game_over": "游戏结束，按 N 重新开始",
        "status_no_undo": "没有可撤销的步骤",
        "status_cleared": "消除 {count} 个小球",
        "info_lines": [
            "这是给喜欢老版 Winlinez 的玩家准备的便携复刻版。",
            "玩法：点击一个小球，再点击可到达的空格，小球会沿通路移动。",
            "目标：让 5 个或更多同色小球在横、竖或斜线连成一线。",
            "消除成功会得分；一次消得越多，分数越高。",
            "如果本步没有消除，会补入顶部预告的 3 个小球。",
            "重开：点“重开”，也可以按 N 或 F2；结束：点“结束”或按 Esc。",
            "撤销：按 U 或 Backspace 可撤销上一次有效移动。",
            "主题：点击顶部“主题”按钮或按 T 切换界面配色。",
            "最高分保存在 exe 同目录的 winlinez_high_score.json。",
            "当当前分超过最高分时，挑战者升高，国王降低。",
            "这个版本是因为老游戏在新系统上不易运行，为家人继续保留那份乐趣。",
        ],
    },
    "en": {
        "best": "Best",
        "current": "Score",
        "next": "Next",
        "new": "New",
        "quit": "Quit",
        "theme": "Theme",
        "language": "En/中",
        "info": "i",
        "king": "King",
        "challenger": "Challenger",
        "game_over": "Game Over",
        "score": "Score: {score}",
        "restart_hint": "Press N/F2 or click New",
        "info_title": "Winlinez Revival",
        "ok": "OK",
        "status_select_ball": "Select a ball",
        "status_choose_destination": "Choose a destination",
        "status_no_path": "No path",
        "status_moving": "Moving",
        "status_game_over": "Game over. Press N to restart",
        "status_no_undo": "Nothing to undo",
        "status_cleared": "{count} balls cleared",
        "info_lines": [
            "A portable remake for players who still love the old Winlinez.",
            "How to play: click a ball, then click a reachable empty cell.",
            "Goal: clear five or more same-color balls in a row, column, or diagonal.",
            "Cleared lines score points; longer lines are worth more.",
            "If no line is cleared, the next three preview balls are added.",
            "Restart: click New, or press N/F2. Quit: click Quit or press Esc.",
            "Undo: press U or Backspace to revert the last valid move.",
            "Theme: click the Theme button or press T to change the colors.",
            "Best score is saved beside the exe as winlinez_high_score.json.",
            "When the challenger beats the best score, the challenger rises and the king drops.",
            "This version exists because the old game no longer runs well on modern Windows, but it is still loved at home.",
        ],
    },
}


MESSAGE_KEYS = {
    "请选择小球": "status_select_ball",
    "请选择目标格": "status_choose_destination",
    "没有通路": "status_no_path",
    "移动中": "status_moving",
    "游戏结束，按 N 重新开始": "status_game_over",
    "没有可撤销的步骤": "status_no_undo",
}


class WinlinezApp:
    def __init__(self) -> None:
        pygame.init()
        icon = pygame.image.load(asset_path(APP_ICON_FILENAME))
        pygame.display.set_icon(pygame.transform.smoothscale(icon, (64, 64)))
        pygame.display.set_caption(APP_TITLE)
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.score_store = HighScoreStore()
        self.game = GameState(best_score=self.score_store.load())
        self.running = True
        self.language = "zh"
        self.theme_index = 0
        self.info_open = False
        self.king_flash_until = 0
        self.moving: MoveAnimation | None = None
        self.font = load_font(18)
        self.small_font = load_font(14)
        self.title_font = load_font(20, bold=True)
        self.digit_font = load_font(24, bold=True)
        self.label_font = load_font(28, bold=True)
        self.info_title_font = load_font(24, bold=True)
        self.info_font = load_font(15)
        self.buttons = [
            Button(pygame.Rect(226, 25, 70, 38), "new"),
            Button(pygame.Rect(306, 25, 70, 38), "quit"),
            Button(pygame.Rect(652, 25, 64, 38), "language"),
            Button(pygame.Rect(726, 25, 38, 38), "info"),
            Button(pygame.Rect(584, 25, 58, 38), "theme"),
        ]
        self.info_ok_rect = pygame.Rect(430, 444, 80, 34)
        self.info_link_rect = pygame.Rect(0, 0, 0, 0)

    @property
    def theme(self) -> Theme:
        return THEMES[self.theme_index]

    def run(self) -> int:
        while self.running:
            self._handle_events()
            self._update_animation()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        return 0

    def draw(self) -> None:
        self.screen.fill(WINDOW_GRAY)
        self._draw_outer_frame()
        self._draw_top_panel()
        self._draw_character_stage(LEFT_STAGE, king=True)
        self._draw_character_stage(RIGHT_STAGE, king=False)
        self._draw_board()
        self._draw_status_bar()
        if self.game.game_over:
            self._draw_game_over()
        if self.info_open:
            self._draw_info_dialog()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self._handle_key(event.key, getattr(event, "unicode", ""), getattr(event, "scancode", None))
            elif event.type == pygame.TEXTINPUT:
                self._handle_text_input(getattr(event, "text", ""))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_key(self, key: int, text: str = "", scancode: int | None = None) -> None:
        if self.info_open:
            if key in (pygame.K_ESCAPE, pygame.K_i):
                self.info_open = False
            return

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self._quit()
        elif key == pygame.K_i:
            self.info_open = True
        elif key == pygame.K_t:
            self._cycle_theme()
        elif self._is_new_game_key(key, text, scancode):
            self._new_game()
        elif key in (pygame.K_BACKSPACE, pygame.K_u):
            if self.moving is None:
                self.game.undo()

    def _handle_text_input(self, text: str) -> None:
        if self._is_new_game_key(pygame.K_UNKNOWN, text):
            self._new_game()

    def _is_new_game_key(self, key: int, text: str = "", scancode: int | None = None) -> bool:
        if key in (pygame.K_F2, pygame.K_n):
            return True
        if text.casefold() in ("n", "ｎ"):
            return True
        return scancode in (17, 59)

    def _new_game(self) -> None:
        self._commit_record_if_needed()
        self.game.reset()
        self.moving = None
        self.game.message = "请选择小球"

    def _quit(self) -> None:
        self._commit_record_if_needed()
        self.running = False

    def _commit_record_if_needed(self) -> bool:
        if self.game.commit_best_score():
            self.score_store.save(self.game.best_score)
            return True
        return False

    def _handle_click(self, pos: tuple[int, int]) -> None:
        if self.info_open:
            if self.info_link_rect.collidepoint(pos):
                self._open_repo()
                return
            if self.info_ok_rect.collidepoint(pos):
                self.info_open = False
            return

        for button in self.buttons:
            if button.rect.collidepoint(pos):
                if button.action == "new":
                    self._new_game()
                elif button.action == "quit":
                    self._quit()
                elif button.action == "language":
                    self.language = "en" if self.language == "zh" else "zh"
                elif button.action == "info":
                    self.info_open = True
                elif button.action == "theme":
                    self._cycle_theme()
                return

        if self.moving is not None:
            return

        cell = self._cell_from_pos(pos)
        if cell is not None:
            self._handle_board_click(cell)

    def _handle_board_click(self, cell: Cell) -> None:
        if self.game.game_over:
            return

        if self.game.color_at(cell) is not None:
            self.game.select(cell)
            return

        if self.game.selected is None:
            self.game.message = "请选择小球"
            return

        path = self.game.find_path(self.game.selected, cell)
        if not path:
            self.game.message = "没有通路"
            return

        color_id = self.game.color_at(self.game.selected)
        if color_id is None:
            self.game.selected = None
            return

        duration = max(MOVE_MIN_DURATION_MS, (len(path) - 1) * MOVE_MS_PER_CELL)
        self.moving = MoveAnimation(path=path, color_id=color_id, started_at=pygame.time.get_ticks(), duration_ms=duration)
        self.game.message = "移动中"

    def _cycle_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(THEMES)
        self.game.message = f"theme:{self.theme.key}"

    def _update_animation(self) -> None:
        if self.moving is None:
            return

        now = pygame.time.get_ticks()
        if now - self.moving.started_at < self.moving.duration_ms:
            return

        start = self.moving.path[0]
        end = self.moving.path[-1]
        self.moving = None
        result = self.game.move(start, end)
        if result.new_record:
            self._trigger_king_effect()
        if self.game.game_over:
            self._commit_record_if_needed()

    def _cell_from_pos(self, pos: tuple[int, int]) -> Cell | None:
        x, y = pos
        ox, oy = BOARD_ORIGIN
        if not (ox <= x < ox + BOARD_SIZE and oy <= y < oy + BOARD_SIZE):
            return None
        col = (x - ox) // CELL_SIZE
        row = (y - oy) // CELL_SIZE
        return (row, col)

    def _cell_rect(self, cell: Cell) -> pygame.Rect:
        row, col = cell
        return pygame.Rect(BOARD_ORIGIN[0] + col * CELL_SIZE, BOARD_ORIGIN[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def _cell_center(self, cell: Cell) -> tuple[int, int]:
        return self._cell_rect(cell).center

    def _draw_outer_frame(self) -> None:
        theme = self.theme
        draw_vertical_gradient(self.screen, self.screen.get_rect(), theme.bg_top, theme.bg_bottom)
        outer = pygame.Rect(6, 8, WINDOW_SIZE[0] - 12, WINDOW_SIZE[1] - 14)
        pygame.draw.rect(self.screen, theme.panel_border, outer, width=1, border_radius=14)

    def _draw_top_panel(self) -> None:
        theme = self.theme
        panel = pygame.Rect(16, 14, 908, 60)
        draw_round_panel(self.screen, panel, theme.panel_bg, theme.panel_border, radius=13)

        self._draw_text(self._text("best"), (36, 36), self.small_font, theme.text_muted)
        self._draw_score_box(pygame.Rect(100, 26, 104, 36), self.game.best_score, theme.accent_gold)

        for button in self.buttons:
            self._draw_button(button)

        self._draw_text(self._text("next"), (390, 36), self.small_font, theme.text_muted)
        for index, color_id in enumerate(self.game.next_colors):
            rect = pygame.Rect(446 + index * 46, 24, 40, 40)
            draw_round_panel(
                self.screen,
                rect,
                blend(theme.panel_bg, (0, 0, 0), 0.35),
                theme.panel_border,
                radius=9,
                shadow=False,
            )
            self._draw_ball(rect.center, COLORS[color_id].rgb, radius=11)

        self._draw_text(self._text("current"), (778, 36), self.small_font, theme.text_muted)
        self._draw_score_box(pygame.Rect(818, 26, 90, 36), self.game.score, theme.accent_primary)

    def _draw_button(self, button: Button) -> None:
        theme = self.theme
        hover = button.rect.collidepoint(pygame.mouse.get_pos())
        fill = theme.panel_bg_2 if hover else blend(theme.panel_bg, (0, 0, 0), 0.15)
        border = {
            "new": theme.accent_primary,
            "quit": (255, 122, 138),
            "theme": theme.accent_primary,
            "language": theme.accent_gold,
            "info": theme.accent_secondary,
        }.get(button.action, theme.panel_border)
        draw_round_panel(self.screen, button.rect, fill, border, radius=9, shadow=False)
        font = self.small_font if button.action == "theme" else self.font
        label = font.render(self._button_label(button.action), True, theme.text_light)
        self.screen.blit(label, label.get_rect(center=button.rect.center))
        if button.action == "theme":
            pygame.draw.line(
                self.screen,
                theme.accent_secondary,
                (button.rect.x + 12, button.rect.bottom - 5),
                (button.rect.right - 12, button.rect.bottom - 5),
                2,
            )

    def _draw_score_box(self, rect: pygame.Rect, score: int, accent: tuple[int, int, int] | None = None) -> None:
        theme = self.theme
        accent = accent or theme.accent_primary
        fill = blend(theme.panel_bg, (0, 0, 0), 0.72)
        draw_round_panel(self.screen, rect, fill, blend(accent, (255, 255, 255), 0.15), radius=8, shadow=False)
        inner = rect.inflate(-10, -8)
        text = self.digit_font.render(str(score), True, theme.text_light)
        glow = self.digit_font.render(str(score), True, accent)
        self.screen.blit(glow, glow.get_rect(midright=(inner.right - 5, inner.centery + 1)))
        self.screen.blit(text, text.get_rect(midright=(inner.right - 6, inner.centery)))

    def _draw_status_bar(self) -> None:
        theme = self.theme
        rect = pygame.Rect(16, 574, 908, 22)
        draw_round_panel(self.screen, rect, theme.panel_bg, theme.panel_border, radius=8, shadow=False)
        self._draw_text(self._status_text(self.game.message), (28, 577), self.small_font, theme.text_muted)
        footer = self._footer_text()
        footer_surface = self.small_font.render(footer, True, blend(theme.text_muted, theme.accent_primary, 0.35))
        self.screen.blit(footer_surface, footer_surface.get_rect(midright=(rect.right - 14, rect.centery + 1)))

    def _draw_board(self) -> None:
        theme = self.theme
        board_frame = pygame.Rect(BOARD_ORIGIN[0] - 2, BOARD_ORIGIN[1] - 2, BOARD_SIZE + 4, BOARD_SIZE + 4)
        draw_round_panel(
            self.screen,
            board_frame,
            blend(theme.panel_bg, (0, 0, 0), 0.4),
            theme.panel_border,
            radius=10,
        )

        hidden_cell = self.moving.path[0] if self.moving else None
        hovered_cell = None
        if self.moving is None and not self.info_open and not self.game.game_over:
            hovered_cell = self._cell_from_pos(pygame.mouse.get_pos())
        for row in range(GameState.rows):
            for col in range(GameState.cols):
                cell = (row, col)
                rect = self._cell_rect(cell)
                cell_rect = rect.inflate(-4, -4)
                fill = theme.cell_bg if (row + col) % 2 == 0 else theme.cell_alt
                selected = self.game.selected == cell and self.moving is None
                hovered = hovered_cell == cell
                if hovered:
                    fill = blend(fill, theme.accent_primary, 0.16)
                border = theme.accent_gold if selected else theme.accent_primary if hovered else theme.cell_border
                border_width = 2 if selected or hovered else 1
                pygame.draw.rect(self.screen, fill, cell_rect, border_radius=8)
                pygame.draw.rect(self.screen, border, cell_rect, width=border_width, border_radius=8)
                pygame.draw.line(
                    self.screen,
                    blend(fill, theme.cell_highlight, 0.4),
                    (cell_rect.x + 7, cell_rect.y + 1),
                    (cell_rect.right - 7, cell_rect.y + 1),
                )

                color_id = self.game.board[row][col]
                if color_id is not None and cell != hidden_cell:
                    self._draw_ball(rect.center, COLORS[color_id].rgb, selected=selected)

        if self.moving is not None:
            center, bounce = self._moving_ball_position(self.moving)
            self._draw_ball(center, COLORS[self.moving.color_id].rgb, radius=18, y_bounce=bounce, moving=True)

    def _moving_ball_position(self, animation: MoveAnimation) -> tuple[tuple[int, int], int]:
        elapsed = pygame.time.get_ticks() - animation.started_at
        progress = max(0.0, min(0.999, elapsed / animation.duration_ms))
        segment_count = max(1, len(animation.path) - 1)
        segment_float = progress * segment_count
        segment_index = min(segment_count - 1, int(segment_float))
        local_t = ease_in_out(segment_float - segment_index)
        start = self._cell_center(animation.path[segment_index])
        end = self._cell_center(animation.path[segment_index + 1])
        x = round(start[0] + (end[0] - start[0]) * local_t)
        y = round(start[1] + (end[1] - start[1]) * local_t)
        bounce = round(abs(math.sin((segment_float % 1) * math.pi)) * 13)
        return (x, y), bounce

    def _draw_character_stage(self, rect: pygame.Rect, king: bool) -> None:
        theme = self.theme
        draw_round_panel(
            self.screen,
            rect,
            blend(theme.panel_bg, (0, 0, 0), 0.68),
            theme.panel_border,
            radius=12,
        )
        inner = rect.inflate(-8, -8)
        draw_vertical_gradient(
            self.screen,
            inner,
            blend(theme.bg_top, (0, 0, 0), 0.25),
            blend(theme.bg_bottom, theme.panel_bg_2, 0.35),
        )
        pygame.draw.rect(self.screen, theme.panel_border, inner, width=1, border_radius=9)
        glow_color = theme.accent_gold if king else theme.accent_secondary
        pygame.draw.line(self.screen, glow_color, (inner.x + 18, inner.y + 14), (inner.right - 18, inner.y + 14), 1)

        phase = pygame.time.get_ticks() / 260
        if king:
            self._draw_king_character(rect, phase, self._character_y_offset(king=True))
            label = self._text("king")
        else:
            self._draw_challenger_character(rect, phase, self._character_y_offset(king=False))
            label = self._text("challenger")

        label_surface = self.label_font.render(label, True, theme.text_light)
        shadow = self.label_font.render(label, True, (74, 74, 74))
        label_rect = label_surface.get_rect(center=(rect.centerx, rect.bottom - 78))
        self.screen.blit(shadow, label_rect.move(2, 2))
        self.screen.blit(label_surface, label_rect)

    def _character_y_offset(self, king: bool) -> int:
        if not self.game.challenger_leads:
            return 0
        return 118 if king else -158

    def _draw_king_character(self, rect: pygame.Rect, phase: float, body_offset: int = 0) -> None:
        bob = round(math.sin(phase) * 3)
        pedestal = self._pedestal_rect_for_offset(pygame.Rect(rect.centerx - 35, rect.bottom - 305, 70, 202), body_offset)
        self._draw_pedestal(pedestal)

        body_center = (rect.centerx - 5, rect.y + 134 + body_offset + bob)
        pygame.draw.ellipse(self.screen, (202, 0, 0), pygame.Rect(body_center[0] - 45, body_center[1] - 28, 74, 92))
        pygame.draw.ellipse(self.screen, (255, 38, 16), pygame.Rect(body_center[0] - 38, body_center[1] - 22, 56, 74))
        pygame.draw.rect(self.screen, (105, 0, 0), pygame.Rect(body_center[0] - 44, body_center[1] + 35, 70, 12))
        pygame.draw.circle(self.screen, (255, 234, 115), (body_center[0] + 14, body_center[1] + 18), 8)
        pygame.draw.circle(self.screen, (190, 128, 0), (body_center[0] + 14, body_center[1] + 18), 8, 2)

        head = (body_center[0] - 3, body_center[1] - 8)
        pygame.draw.circle(self.screen, (255, 42, 20), head, 25)
        pygame.draw.circle(self.screen, (0, 0, 0), (head[0] - 8, head[1] - 2), 7)
        pygame.draw.circle(self.screen, (0, 0, 0), (head[0] + 10, head[1] - 2), 7)
        pygame.draw.circle(self.screen, (255, 255, 255), (head[0] - 10, head[1] - 4), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (head[0] + 8, head[1] - 4), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(head[0] - 12, head[1] + 13, 24, 8))
        for tooth in range(4):
            pygame.draw.line(self.screen, (0, 0, 0), (head[0] - 6 + tooth * 5, head[1] + 13), (head[0] - 6 + tooth * 5, head[1] + 20))

        self._draw_crown((head[0], head[1] - 31), scale=1.25)
        self._draw_scepter((body_center[0] + 55, body_center[1] + 4 + bob))

        if self.king_flash_until > pygame.time.get_ticks():
            for index in range(8):
                angle = phase * 0.8 + index * math.tau / 8
                pos = (
                    round(body_center[0] + math.cos(angle) * 58),
                    round(body_center[1] - 18 + math.sin(angle) * 52),
                )
                self._draw_sparkle(pos, 5)

    def _draw_challenger_character(self, rect: pygame.Rect, phase: float, body_offset: int = 0) -> None:
        bob = round(math.sin(phase + 1.4) * 3)
        pedestal = self._pedestal_rect_for_offset(pygame.Rect(rect.centerx - 34, rect.bottom - 120, 68, 27), body_offset)
        self._draw_pedestal(pedestal, short=True)

        base_x = rect.centerx + 3
        base_y = rect.bottom - 188 + body_offset + bob
        pygame.draw.ellipse(self.screen, (178, 0, 186), pygame.Rect(base_x - 41, base_y - 16, 82, 82))
        pygame.draw.ellipse(self.screen, (236, 0, 222), pygame.Rect(base_x - 30, base_y - 24, 58, 58))
        pygame.draw.circle(self.screen, (255, 134, 255), (base_x + 8, base_y - 2), 18)
        pygame.draw.circle(self.screen, (0, 0, 0), (base_x, base_y - 5), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), (base_x + 15, base_y - 5), 5)
        pygame.draw.circle(self.screen, (255, 255, 255), (base_x - 1, base_y - 7), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (base_x + 13, base_y - 7), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(base_x + 1, base_y + 15, 20, 7))
        pygame.draw.line(self.screen, (0, 0, 0), (base_x + 10, base_y + 15), (base_x + 10, base_y + 21))

        for foot_x in (-27, 23):
            pygame.draw.ellipse(self.screen, (118, 0, 128), pygame.Rect(base_x + foot_x, base_y + 49, 30, 12))

        sword_x = base_x - 53
        pygame.draw.polygon(
            self.screen,
            SILVER,
            [(sword_x, base_y - 58), (sword_x + 6, base_y - 18), (sword_x, base_y + 8), (sword_x - 6, base_y - 18)],
        )
        pygame.draw.polygon(
            self.screen,
            (255, 255, 255),
            [(sword_x, base_y - 56), (sword_x + 2, base_y - 18), (sword_x, base_y), (sword_x - 2, base_y - 18)],
        )
        pygame.draw.rect(self.screen, GOLD, pygame.Rect(sword_x - 15, base_y + 6, 30, 6))
        pygame.draw.rect(self.screen, GOLD_DARK, pygame.Rect(sword_x - 3, base_y + 12, 6, 22))

        wand_x = base_x + 45
        pygame.draw.line(self.screen, (255, 0, 221), (wand_x, base_y - 54), (wand_x, base_y + 3), 3)
        self._draw_sparkle((wand_x, base_y - 58), 6)

    def _pedestal_rect_for_offset(self, base_rect: pygame.Rect, body_offset: int) -> pygame.Rect:
        bottom = base_rect.bottom
        top = min(bottom - 22, base_rect.y + body_offset)
        return pygame.Rect(base_rect.x, top, base_rect.width, bottom - top)

    def _draw_pedestal(self, rect: pygame.Rect, short: bool = False) -> None:
        pygame.draw.ellipse(self.screen, (72, 72, 72), pygame.Rect(rect.x - 8, rect.bottom - 6, rect.width + 16, 12))
        pygame.draw.rect(self.screen, (185, 190, 190), rect)
        stripe_count = 8 if not short else 5
        for index in range(stripe_count):
            x = rect.x + round(index * rect.width / stripe_count)
            color = blend(SILVER, (255, 255, 255), 0.35 if index % 2 == 0 else 0.0)
            pygame.draw.rect(self.screen, color, pygame.Rect(x, rect.y, max(2, rect.width // (stripe_count * 2)), rect.height))
        pygame.draw.ellipse(self.screen, (230, 232, 232), pygame.Rect(rect.x - 6, rect.y - 7, rect.width + 12, 14))
        pygame.draw.ellipse(self.screen, (120, 125, 125), pygame.Rect(rect.x - 7, rect.bottom - 7, rect.width + 14, 14), 2)

    def _draw_game_over(self) -> None:
        theme = self.theme
        overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        modal = pygame.Rect(318, 216, 304, 126)
        draw_round_panel(self.screen, modal, theme.panel_bg_2, theme.accent_secondary, radius=14)
        title = self.title_font.render(self._text("game_over"), True, theme.text_light)
        self.screen.blit(title, title.get_rect(center=(470, 256)))
        score = self.font.render(self._text("score").format(score=self.game.score), True, theme.accent_gold)
        self.screen.blit(score, score.get_rect(center=(470, 290)))
        hint = self.small_font.render(self._text("restart_hint"), True, theme.text_muted)
        self.screen.blit(hint, hint.get_rect(center=(470, 314)))

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        if font.size(text)[0] <= max_width:
            return [text]

        def split_long(chunk: str) -> list[str]:
            lines: list[str] = []
            current = ""
            for char in chunk:
                candidate = current + char
                if current and font.size(candidate)[0] > max_width:
                    lines.append(current)
                    current = char
                else:
                    current = candidate
            if current:
                lines.append(current)
            return lines

        words = text.split(" ")
        if len(words) == 1:
            return split_long(text)

        lines: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
                continue
            if current:
                lines.extend(split_long(current))
            current = word

        if current:
            lines.extend(split_long(current))
        return lines

    def _draw_info_dialog(self) -> None:
        theme = self.theme
        overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        self.screen.blit(overlay, (0, 0))

        modal = pygame.Rect(105, 58, 730, 500)
        self.info_ok_rect = pygame.Rect(modal.centerx - 40, modal.bottom - 48, 80, 34)
        draw_round_panel(self.screen, modal, theme.panel_bg_2, theme.accent_primary, radius=16)
        title = self.info_title_font.render(self._text("info_title"), True, theme.text_light)
        self.screen.blit(title, title.get_rect(center=(modal.centerx, modal.y + 38)))

        y = modal.y + 78
        max_width = modal.width - 80
        self.info_link_rect = pygame.Rect(0, 0, 0, 0)
        for line in self._info_lines():
            for wrapped in self._wrap_text(line, self.info_font, max_width):
                rendered = self.info_font.render(wrapped, True, theme.text_light)
                self.screen.blit(rendered, (modal.x + 40, y))
                y += 22
            y += 4
        self._draw_info_link((modal.x + 40, y), max_width)

        draw_round_panel(self.screen, self.info_ok_rect, theme.panel_bg, theme.accent_primary, radius=8, shadow=False)
        ok = self.font.render(self._text("ok"), True, theme.text_light)
        self.screen.blit(ok, ok.get_rect(center=self.info_ok_rect.center))

    def _draw_info_link(self, pos: tuple[int, int], max_width: int) -> None:
        theme = self.theme
        x, y = pos
        hover = self.info_link_rect.collidepoint(pygame.mouse.get_pos())
        color = blend(theme.link, (255, 255, 255), 0.22 if hover else 0.0)
        hit_rect: pygame.Rect | None = None
        for wrapped in self._wrap_text(self._repo_link_text(), self.info_font, max_width):
            rendered = self.info_font.render(wrapped, True, color)
            rect = rendered.get_rect(topleft=(x, y))
            self.screen.blit(rendered, rect)
            pygame.draw.line(self.screen, color, (rect.left, rect.bottom + 1), (rect.right, rect.bottom + 1), 1)
            inflated = rect.inflate(8, 6)
            hit_rect = inflated if hit_rect is None else hit_rect.union(inflated)
            y += 22
        self.info_link_rect = hit_rect or pygame.Rect(0, 0, 0, 0)

    def _open_repo(self) -> None:
        webbrowser.open(REPO_URL)

    def _trigger_king_effect(self) -> None:
        self.king_flash_until = pygame.time.get_ticks() + 3200

    def _draw_crown(self, center: tuple[int, int], scale: float = 1.0) -> None:
        cx, cy = center
        points = [
            (-16, 10),
            (-13, -8),
            (-5, 0),
            (0, -13),
            (5, 0),
            (13, -8),
            (16, 10),
        ]
        scaled = [(cx + round(x * scale), cy + round(y * scale)) for x, y in points]
        pygame.draw.polygon(self.screen, GOLD, scaled)
        pygame.draw.polygon(self.screen, GOLD_DARK, scaled, width=2)
        band = pygame.Rect(cx - round(15 * scale), cy + round(6 * scale), round(30 * scale), max(5, round(6 * scale)))
        pygame.draw.rect(self.screen, blend(GOLD, (255, 255, 255), 0.25), band)
        pygame.draw.rect(self.screen, GOLD_DARK, band, width=1)
        for point in scaled[1::2]:
            pygame.draw.circle(self.screen, (255, 40, 40), point, max(2, round(2 * scale)))

    def _draw_scepter(self, base: tuple[int, int]) -> None:
        x, y = base
        pygame.draw.line(self.screen, GOLD, (x, y - 52), (x, y + 64), 5)
        pygame.draw.line(self.screen, GOLD_DARK, (x + 3, y - 48), (x + 3, y + 64), 2)
        self._draw_sparkle((x, y - 60), 12)
        pygame.draw.circle(self.screen, GOLD, (x, y - 60), 5)

    def _draw_sparkle(self, center: tuple[int, int], radius: int) -> None:
        cx, cy = center
        pygame.draw.line(self.screen, GOLD, (cx - radius, cy), (cx + radius, cy), width=2)
        pygame.draw.line(self.screen, GOLD, (cx, cy - radius), (cx, cy + radius), width=2)
        pygame.draw.line(self.screen, GOLD, (cx - radius // 2, cy - radius // 2), (cx + radius // 2, cy + radius // 2), width=1)
        pygame.draw.line(self.screen, GOLD, (cx + radius // 2, cy - radius // 2), (cx - radius // 2, cy + radius // 2), width=1)
        pygame.draw.circle(self.screen, blend(GOLD, (255, 255, 255), 0.45), center, 2)

    def _draw_ball(
        self,
        center: tuple[int, int],
        rgb: tuple[int, int, int],
        radius: int = 18,
        selected: bool = False,
        y_bounce: int = 0,
        moving: bool = False,
    ) -> None:
        ticks = pygame.time.get_ticks()
        cx, cy = center
        pulse = 0
        if selected:
            y_bounce = 7 + round(math.sin(ticks / 120) * 5)
            pulse = round((math.sin(ticks / 100) + 1) * 1.5)
        elif moving:
            pulse = 1

        draw_y = cy - y_bounce
        shadow_width = radius * 2 - max(0, y_bounce)
        shadow_alpha = max(58, 120 - y_bounce * 5)
        shadow = pygame.Surface((radius * 3, radius), pygame.SRCALPHA)
        pygame.draw.ellipse(
            shadow,
            (0, 0, 0, shadow_alpha),
            pygame.Rect((radius * 3 - shadow_width) // 2, 2, shadow_width, max(4, radius // 2)),
        )
        self.screen.blit(shadow, (cx - radius * 3 // 2, cy + radius // 2 + 4))

        actual_radius = radius + pulse
        dark = blend(rgb, (0, 0, 0), 0.45)
        light = blend(rgb, (255, 255, 255), 0.36)
        for step in range(actual_radius, 0, -1):
            t = 1 - (step / actual_radius)
            color = blend(dark, light, t * 0.82)
            pygame.draw.circle(self.screen, color, (cx, draw_y), step)

        pygame.draw.circle(self.screen, blend(rgb, (0, 0, 0), 0.58), (cx, draw_y), actual_radius, 2)
        highlight_center = (cx - actual_radius // 3, draw_y - actual_radius // 3)
        pygame.draw.circle(self.screen, blend((255, 255, 255), rgb, 0.09), highlight_center, max(3, actual_radius // 4))
        pygame.draw.circle(
            self.screen,
            blend((255, 255, 255), rgb, 0.25),
            (highlight_center[0] + 2, highlight_center[1] + 2),
            max(2, actual_radius // 7),
        )

        if selected:
            orbit = ticks / 180
            for index in range(3):
                angle = orbit + index * math.tau / 3
                sparkle = (
                    round(cx + math.cos(angle) * (actual_radius + 8)),
                    round(draw_y + math.sin(angle) * (actual_radius + 5)),
                )
                self._draw_mini_glint(sparkle, COLORS[0].rgb if index == 0 else GOLD)

    def _draw_mini_glint(self, center: tuple[int, int], color: tuple[int, int, int]) -> None:
        cx, cy = center
        pygame.draw.line(self.screen, color, (cx - 3, cy), (cx + 3, cy), 1)
        pygame.draw.line(self.screen, color, (cx, cy - 3), (cx, cy + 3), 1)
        pygame.draw.circle(self.screen, blend(color, (255, 255, 255), 0.25), center, 1)

    def _draw_text(
        self,
        text: str,
        pos: tuple[int, int],
        font: pygame.font.Font,
        color: tuple[int, int, int],
        shadow: tuple[int, int, int] | None = None,
    ) -> None:
        if shadow is not None:
            self.screen.blit(font.render(text, True, shadow), (pos[0] + 1, pos[1] + 1))
        self.screen.blit(font.render(text, True, color), pos)

    def _button_label(self, action: str) -> str:
        return self._text(action)

    def _text(self, key: str):
        return TEXT[self.language][key]

    def _footer_text(self) -> str:
        return f"v{__version__} | {REPO_LABEL}"

    def _info_lines(self) -> list[str]:
        lines = list(self._text("info_lines"))
        if self.language == "zh":
            lines.append(f"版本：v{__version__}")
            lines.append(f"作者：{AUTHOR_LABEL}")
        else:
            lines.append(f"Version: v{__version__}")
            lines.append(f"Author: {AUTHOR_LABEL}")
        return lines

    def _repo_link_text(self) -> str:
        return f"GitHub：{REPO_URL}" if self.language == "zh" else f"GitHub: {REPO_URL}"

    def _status_text(self, message: str) -> str:
        if message.startswith("theme:"):
            name = self.theme.name_zh if self.language == "zh" else self.theme.name_en
            label = "主题" if self.language == "zh" else "Theme"
            return f"{label}：{name}" if self.language == "zh" else f"{label}: {name}"
        if self.language == "zh":
            return message
        if message.startswith("消除 ") and message.endswith(" 个小球"):
            count = message.removeprefix("消除 ").removesuffix(" 个小球")
            return self._text("status_cleared").format(count=count)
        key = MESSAGE_KEYS.get(message)
        if key is not None:
            return self._text(key)
        return message


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="Render one frame and exit.")
    parser.add_argument("--screenshot", type=Path, help="Write a screenshot during smoke rendering.")
    parser.add_argument("--self-test-restart", action="store_true", help="Verify N and F2 restart after game over.")
    args = parser.parse_args(argv)

    if args.smoke or args.self_test_restart:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

    app = WinlinezApp()
    if args.self_test_restart:
        passed = _self_test_restart(app)
        pygame.quit()
        return 0 if passed else 1
    if args.smoke:
        app.draw()
        pygame.display.flip()
        if args.screenshot:
            args.screenshot.parent.mkdir(parents=True, exist_ok=True)
            pygame.image.save(app.screen, args.screenshot)
        pygame.quit()
        return 0
    return app.run()


def _self_test_restart(app: WinlinezApp) -> bool:
    for event in (
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_n, unicode="n", scancode=17),
        pygame.event.Event(pygame.KEYUP, key=pygame.K_F2, unicode="", scancode=59),
        pygame.event.Event(pygame.TEXTINPUT, text="n"),
    ):
        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True
        app.game.message = "游戏结束，按 N 重新开始"
        pygame.event.post(event)
        app._handle_events()
        if app.game.game_over:
            return False
    app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
    app.game.game_over = True
    app._handle_click(app.buttons[0].rect.center)
    if app.game.game_over:
        return False

    app.running = True
    app._handle_click(app.buttons[1].rect.center)
    if app.running:
        return False
    return True


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
