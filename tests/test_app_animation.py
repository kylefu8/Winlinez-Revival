import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from winlinez import __version__
from winlinez.app import (
    APP_TITLE,
    AUTHOR_LABEL,
    MOVE_MIN_DURATION_MS,
    MOVE_MS_PER_CELL,
    REPO_LABEL,
    REPO_URL,
    THEMES,
    WinlinezApp,
)


def clear_board(app: WinlinezApp) -> None:
    app.game.board = [[None for _ in range(app.game.cols)] for _ in range(app.game.rows)]
    app.game.selected = None
    app.game.game_over = False
    app.game.message = ""


def test_move_animation_commits_move_when_finished() -> None:
    app = WinlinezApp()
    try:
        clear_board(app)
        app.game.board[0][0] = 0
        app.game.board[0][1] = 0
        app.game.board[0][2] = 0
        app.game.board[0][3] = 0
        app.game.board[2][4] = 0
        app.game.next_colors = [1, 2, 3]
        app.game.select((2, 4))

        app._handle_board_click((0, 4))

        assert app.moving is not None
        assert app.moving.duration_ms == max(MOVE_MIN_DURATION_MS, 2 * MOVE_MS_PER_CELL)
        app.moving.started_at -= app.moving.duration_ms
        app._update_animation()

        assert app.moving is None
        assert all(app.game.board[0][col] is None for col in range(5))
        assert app.game.board[2][4] is None
        assert app.game.score == 25
    finally:
        pygame.quit()


def test_n_starts_new_game_after_game_over() -> None:
    app = WinlinezApp()
    try:
        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True
        app.game.message = "游戏结束，按 N 重新开始"

        app._handle_key(pygame.K_n)

        assert not app.game.game_over
        assert app.game.message == "请选择小球"
    finally:
        pygame.quit()


def test_keyboard_events_restart_after_game_over() -> None:
    app = WinlinezApp()
    try:
        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_n, unicode="n", scancode=17))
        app._handle_events()
        assert not app.game.game_over

        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_F2, unicode="", scancode=59))
        app._handle_events()
        assert not app.game.game_over
    finally:
        pygame.quit()


def test_scancode_restart_after_game_over() -> None:
    app = WinlinezApp()
    try:
        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode="", scancode=17))
        app._handle_events()
        assert not app.game.game_over
    finally:
        pygame.quit()


def test_textinput_restart_after_game_over() -> None:
    app = WinlinezApp()
    try:
        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True
        pygame.event.post(pygame.event.Event(pygame.TEXTINPUT, text="n"))
        app._handle_events()
        assert not app.game.game_over
    finally:
        pygame.quit()


def test_buttons_restart_and_quit() -> None:
    app = WinlinezApp()
    try:
        app.game.board = [[0 for _ in range(app.game.cols)] for _ in range(app.game.rows)]
        app.game.game_over = True

        app._handle_click(app.buttons[0].rect.center)
        assert not app.game.game_over

        app.running = True
        app._handle_click(app.buttons[1].rect.center)
        assert not app.running
    finally:
        pygame.quit()


def test_language_toggle_and_info_dialog() -> None:
    app = WinlinezApp()
    try:
        assert pygame.display.get_caption()[0] == APP_TITLE
        assert f"v{__version__}" in APP_TITLE
        assert app._footer_text() == f"v{__version__} | {REPO_LABEL}"
        assert app._button_label("new") == "重开"
        app._handle_click(app.buttons[2].rect.center)
        assert app.language == "en"
        assert app._button_label("new") == "New"

        app._handle_click(app.buttons[3].rect.center)
        assert app.info_open
        app._handle_click(app.info_ok_rect.center)
        assert not app.info_open
    finally:
        pygame.quit()


def test_theme_button_and_keyboard_cycle_themes() -> None:
    app = WinlinezApp()
    try:
        assert app.theme == THEMES[0]

        theme_button = next(button for button in app.buttons if button.action == "theme")
        app._handle_click(theme_button.rect.center)
        assert app.theme == THEMES[1]
        assert app._status_text(app.game.message) == f"主题：{THEMES[1].name_zh}"

        app.language = "en"
        app._handle_key(pygame.K_t)
        assert app.theme == THEMES[2]
        assert app._status_text(app.game.message) == f"Theme: {THEMES[2].name_en}"
    finally:
        pygame.quit()


def test_all_themes_render() -> None:
    app = WinlinezApp()
    try:
        for index in range(len(THEMES)):
            app.theme_index = index
            app.draw()
    finally:
        pygame.quit()


def test_info_dialog_text_wraps_inside_modal_width() -> None:
    app = WinlinezApp()
    try:
        max_width = 730 - 80
        for language in ("zh", "en"):
            app.language = language
            info_lines = app._info_lines()
            assert any(f"v{__version__}" in line for line in info_lines)
            assert any(AUTHOR_LABEL in line for line in info_lines)
            assert REPO_URL in app._repo_link_text()
            for line in info_lines:
                wrapped = app._wrap_text(line, app.info_font, max_width)
                assert wrapped
                assert all(app.info_font.size(part)[0] <= max_width for part in wrapped)
            assert all(app.info_font.size(part)[0] <= max_width for part in app._wrap_text(app._repo_link_text(), app.info_font, max_width))
    finally:
        pygame.quit()


def test_info_dialog_github_link_opens_browser(monkeypatch) -> None:
    opened: list[str] = []
    app = WinlinezApp()
    try:
        monkeypatch.setattr("winlinez.app.webbrowser.open", lambda url: opened.append(url) or True)
        app.info_open = True
        app.draw()

        assert app.info_link_rect.width > 0
        app._handle_click(app.info_link_rect.center)

        assert opened == [REPO_URL]
        assert app.info_open
    finally:
        pygame.quit()


def test_challenger_lead_moves_characters() -> None:
    app = WinlinezApp()
    try:
        app.game.best_score = 100
        app.game.score = 125

        assert app._character_y_offset(king=True) == 118
        assert app._character_y_offset(king=False) == -158

        app.game.score = 100
        assert app._character_y_offset(king=True) == 0
        assert app._character_y_offset(king=False) == 0
    finally:
        pygame.quit()


def test_pedestal_bottom_stays_fixed_while_top_follows_character() -> None:
    app = WinlinezApp()
    try:
        king_base = pygame.Rect(75, 263, 70, 202)
        king_lowered = app._pedestal_rect_for_offset(king_base, 118)
        assert king_lowered.bottom == king_base.bottom
        assert king_lowered.y == king_base.y + 118
        assert king_lowered.height == king_base.height - 118

        challenger_base = pygame.Rect(784, 448, 68, 27)
        challenger_raised = app._pedestal_rect_for_offset(challenger_base, -158)
        assert challenger_raised.bottom == challenger_base.bottom
        assert challenger_raised.y == challenger_base.y - 158
        assert challenger_raised.height == challenger_base.height + 158
    finally:
        pygame.quit()


def test_new_game_commits_pending_record(tmp_path) -> None:
    app = WinlinezApp()
    try:
        app.score_store.path = tmp_path / "score.json"
        app.game.best_score = 100
        app.game.score = 125

        app._new_game()

        assert app.game.best_score == 125
        assert app.game.score == 0
        assert app.score_store.load() == 125
    finally:
        pygame.quit()
