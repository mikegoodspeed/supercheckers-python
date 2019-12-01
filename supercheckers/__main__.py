import click

import supercheckers as sc


@click.command()
def main():
    player_1 = sc.ConsolePlayer(sc.Team.ONE)
    player_2 = sc.ConsolePlayer(sc.Team.TWO)

    state = sc.GameState(player_1, player_2, sc.Journal(sc.Board()))
    verifier = sc.Verifier(sc.all_rules())
    with sc.Game(state, verifier) as game:
        while game.in_progress:
            game.take_turn()


if __name__ == "__main__":
    main()
