from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random
from typing import Iterable


Cell = tuple[int, int]


@dataclass(frozen=True)
class BallColor:
    id: int
    name: str
    rgb: tuple[int, int, int]


COLORS: tuple[BallColor, ...] = (
    BallColor(0, "red", (255, 22, 24)),
    BallColor(1, "blue", (22, 46, 255)),
    BallColor(2, "green", (0, 218, 32)),
    BallColor(3, "yellow", (255, 235, 0)),
    BallColor(4, "violet", (220, 0, 238)),
    BallColor(5, "cyan", (0, 224, 238)),
    BallColor(6, "orange", (255, 122, 0)),
)


@dataclass(frozen=True)
class MoveResult:
    moved: bool
    removed: int = 0
    spawned: int = 0
    new_record: bool = False
    message: str = ""


class GameState:
    rows = 9
    cols = 9
    line_length = 5
    spawn_count = 3
    initial_count = 5

    def __init__(self, seed: int | None = None, best_score: int = 0) -> None:
        self._seed = seed
        self.rng = random.Random(seed)
        self.board: list[list[int | None]] = []
        self.next_colors: list[int] = []
        self.score = 0
        self.best_score = max(0, best_score)
        self.selected: Cell | None = None
        self.game_over = False
        self.message = "请选择小球"
        self._undo_stack: list[tuple[list[list[int | None]], list[int], int, Cell | None, bool, str]] = []
        self.reset(seed=seed)

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            self._seed = seed
            self.rng.seed(seed)
        elif self._seed is not None:
            self.rng.seed(self._seed)

        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.next_colors = self._random_colors(self.spawn_count)
        self.score = 0
        self.selected = None
        self.game_over = False
        self.message = "请选择小球"
        self._undo_stack.clear()
        self._place_random(self._random_colors(self.initial_count))
        self._remove_lines(self._find_all_lines())
        self._update_game_over()

    @property
    def challenger_leads(self) -> bool:
        return self.score > self.best_score

    def commit_best_score(self) -> bool:
        if self.score > self.best_score:
            self.best_score = self.score
            return True
        return False

    def color_at(self, cell: Cell) -> int | None:
        row, col = cell
        return self.board[row][col]

    def in_bounds(self, cell: Cell) -> bool:
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols

    def empty_cells(self) -> list[Cell]:
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.board[row][col] is None
        ]

    def occupied_cells(self) -> list[Cell]:
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.board[row][col] is not None
        ]

    def select(self, cell: Cell | None) -> None:
        if cell is None or not self.in_bounds(cell) or self.color_at(cell) is None:
            self.selected = None
            self.message = "请选择小球"
            return
        self.selected = cell
        self.message = "请选择目标格"

    def handle_cell_click(self, cell: Cell) -> MoveResult:
        if self.game_over:
            return MoveResult(False, message="游戏结束，按 N 重新开始")
        if not self.in_bounds(cell):
            return MoveResult(False, message="")

        if self.color_at(cell) is not None:
            self.select(cell)
            return MoveResult(False, message="已选中")

        if self.selected is None:
            self.message = "请选择小球"
            return MoveResult(False, message=self.message)

        return self.move(self.selected, cell)

    def move(self, start: Cell, end: Cell) -> MoveResult:
        if self.game_over:
            return MoveResult(False, message="游戏结束，按 N 重新开始")
        if not self.in_bounds(start) or not self.in_bounds(end):
            return MoveResult(False, message="超出棋盘")
        if self.color_at(start) is None:
            return MoveResult(False, message="没有选中小球")
        if self.color_at(end) is not None:
            return MoveResult(False, message="目标格已有小球")
        if not self.has_path(start, end):
            self.message = "没有通路"
            return MoveResult(False, message=self.message)

        self._push_undo()
        color = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]] = color
        self.selected = None

        removed_cells = self._find_lines_from(end)
        removed = self._remove_lines(removed_cells)
        spawned = 0
        new_record = False

        if removed:
            new_record = self._add_score(removed)
            self.message = f"消除 {removed} 个小球"
        else:
            spawned_cells = self._place_random(self.next_colors)
            spawned = len(spawned_cells)
            spawn_lines: set[Cell] = set()
            for cell in spawned_cells:
                spawn_lines.update(self._find_lines_from(cell))
            removed = self._remove_lines(spawn_lines)
            if removed:
                new_record = self._add_score(removed)
                self.message = f"消除 {removed} 个小球"
            else:
                self.message = "请选择小球"
            self.next_colors = self._random_colors(self.spawn_count)

        self._update_game_over()
        return MoveResult(True, removed=removed, spawned=spawned, new_record=new_record, message=self.message)

    def undo(self) -> bool:
        if not self._undo_stack:
            self.message = "没有可撤销的步骤"
            return False
        board, next_colors, score, selected, game_over, message = self._undo_stack.pop()
        self.board = [row[:] for row in board]
        self.next_colors = next_colors[:]
        self.score = score
        self.selected = selected
        self.game_over = game_over
        self.message = message
        return True

    def has_path(self, start: Cell, end: Cell) -> bool:
        return bool(self.find_path(start, end))

    def find_path(self, start: Cell, end: Cell) -> list[Cell]:
        if start == end:
            return []
        queue: deque[Cell] = deque([start])
        visited = {start}
        came_from: dict[Cell, Cell] = {}

        while queue:
            current = queue.popleft()
            for neighbor in self._neighbors(current):
                if neighbor in visited:
                    continue
                if neighbor == end:
                    came_from[neighbor] = current
                    path = [neighbor]
                    while path[-1] != start:
                        path.append(came_from[path[-1]])
                    path.reverse()
                    return path
                if self.color_at(neighbor) is None:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        return []

    def _neighbors(self, cell: Cell) -> Iterable[Cell]:
        row, col = cell
        for drow, dcol in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = (row + drow, col + dcol)
            if self.in_bounds(neighbor):
                yield neighbor

    def _random_colors(self, count: int) -> list[int]:
        return [self.rng.randrange(len(COLORS)) for _ in range(count)]

    def _place_random(self, colors: Iterable[int]) -> list[Cell]:
        colors_to_place = list(colors)
        empties = self.empty_cells()
        self.rng.shuffle(empties)
        placed: list[Cell] = []
        for color, cell in zip(colors_to_place, empties):
            row, col = cell
            self.board[row][col] = color
            placed.append(cell)
        return placed

    def _find_all_lines(self) -> set[Cell]:
        cells: set[Cell] = set()
        for cell in self.occupied_cells():
            cells.update(self._find_lines_from(cell))
        return cells

    def _find_lines_from(self, cell: Cell) -> set[Cell]:
        color = self.color_at(cell)
        if color is None:
            return set()

        matches: set[Cell] = set()
        for drow, dcol in ((1, 0), (0, 1), (1, 1), (1, -1)):
            line = [cell]
            row, col = cell
            while True:
                row += drow
                col += dcol
                candidate = (row, col)
                if not self.in_bounds(candidate) or self.color_at(candidate) != color:
                    break
                line.append(candidate)

            row, col = cell
            while True:
                row -= drow
                col -= dcol
                candidate = (row, col)
                if not self.in_bounds(candidate) or self.color_at(candidate) != color:
                    break
                line.append(candidate)

            if len(line) >= self.line_length:
                matches.update(line)
        return matches

    def _remove_lines(self, cells: Iterable[Cell]) -> int:
        unique_cells = set(cells)
        for row, col in unique_cells:
            self.board[row][col] = None
        return len(unique_cells)

    def _add_score(self, removed: int) -> bool:
        previous_score = self.score
        self.score += removed * removed
        return previous_score <= self.best_score < self.score

    def _update_game_over(self) -> None:
        if not self.empty_cells():
            self.game_over = True
            self.message = "游戏结束，按 N 重新开始"

    def _push_undo(self) -> None:
        self._undo_stack.append(
            (
                [row[:] for row in self.board],
                self.next_colors[:],
                self.score,
                self.selected,
                self.game_over,
                self.message,
            )
        )
        self._undo_stack = self._undo_stack[-1:]
