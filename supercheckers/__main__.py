import click

import supercheckers as sc


@click.command()
def main():
    state = sc.GameState()
    board = sc.Board()
    player_1 = sc.ConsolePlayer(sc.Team.ONE)
    player_2 = sc.ConsolePlayer(sc.Team.TWO)
    with sc.Game(state, board, player_1, player_2) as game:
        while game.is_active:
            game.take_turn()


if __name__ == "__main__":
    main()
