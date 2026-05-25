from winlinez.game import GameState


def clear_board(game: GameState) -> None:
    game.board = [[None for _ in range(game.cols)] for _ in range(game.rows)]
    game.selected = None
    game.game_over = False
    game.message = ""


def test_path_finds_route_through_empty_cells() -> None:
    game = GameState(seed=1)
    clear_board(game)
    game.board[0][0] = 0

    assert game.has_path((0, 0), (8, 8))
    path = game.find_path((0, 0), (8, 8))
    assert path[0] == (0, 0)
    assert path[-1] == (8, 8)


def test_path_is_blocked_by_occupied_cells() -> None:
    game = GameState(seed=1)
    clear_board(game)
    game.board[1][1] = 0
    for row in range(game.rows):
        for col in range(game.cols):
            if (row, col) != (1, 1):
                game.board[row][col] = 2
    game.board[7][7] = None

    assert not game.has_path((1, 1), (7, 7))


def test_move_clears_horizontal_line_without_spawning() -> None:
    game = GameState(seed=2, best_score=10)
    clear_board(game)
    game.next_colors = [1, 2, 3]
    game.board[0][0] = 0
    game.board[0][1] = 0
    game.board[0][2] = 0
    game.board[0][3] = 0
    game.board[2][4] = 0

    result = game.move((2, 4), (0, 4))

    assert result.moved
    assert result.removed == 5
    assert result.spawned == 0
    assert result.new_record
    assert game.score == 25
    assert game.best_score == 10
    assert game.challenger_leads
    assert all(game.board[0][col] is None for col in range(5))
    assert game.next_colors == [1, 2, 3]


def test_record_is_committed_explicitly() -> None:
    game = GameState(seed=2, best_score=99)
    game.score = 125

    assert game.commit_best_score()
    assert game.best_score == 125

    game.reset()

    assert game.best_score == 125


def test_no_clear_spawns_next_colors_and_refreshes_preview() -> None:
    game = GameState(seed=3)
    clear_board(game)
    game.next_colors = [1, 2, 3]
    game.board[0][0] = 0

    result = game.move((0, 0), (8, 8))

    assert result.moved
    assert result.removed == 0
    assert result.spawned == 3
    assert len(game.occupied_cells()) == 4
    assert game.next_colors != [1, 2, 3]


def test_undo_restores_previous_board_and_score() -> None:
    game = GameState(seed=4)
    clear_board(game)
    game.next_colors = [1, 2, 3]
    game.board[0][0] = 0
    before = [row[:] for row in game.board]

    game.move((0, 0), (8, 8))

    assert game.undo()
    assert game.board == before
    assert game.score == 0
