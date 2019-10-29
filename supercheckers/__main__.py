import click

import supercheckers


@click.command()
def play():
    with supercheckers.Game.create() as game:
        while game.is_active:
            game.take_turn()


if __name__ == "__main__":
    play()
