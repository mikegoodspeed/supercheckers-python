import click

import supercheckers


@click.command()
def play():
    game = supercheckers.Game()
    game.begin()
    while game.is_active:
        game.take_turn()
    game.end()


if __name__ == "__main__":
    play()
