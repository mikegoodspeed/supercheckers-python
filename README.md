Supercheckers (Python)
======================

[![licence](https://img.shields.io/badge/license-MIT-green)](https://choosealicense.com/licenses/mit/)
[![python](https://img.shields.io/badge/python-3.7-blue)](https://www.python.org)
[![environment](https://img.shields.io/badge/environment-pipenv-blue)](https://pipenv.kennethreitz.org/)
![style](https://img.shields.io/badge/style-black%20%7C%20isort%20%7C%20flake8-blue)
[![typing](https://img.shields.io/badge/typing-mypy-blue)](http://mypy-lang.org)
[![cli](https://img.shields.io/badge/cli-click-blue)](https://click.palletsprojects.com/)
[![build](https://img.shields.io/badge/build-pyinvoke-blue)](https://www.pyinvoke.org)
[![testing](https://img.shields.io/badge/testing-pytest-blue)](https://pytest.org)

------------------------------------------------------------------------------------------------------------------------

Supercheckers is a board game first published in 1986 by 
[Christopher Wroth](https://boardgamegeek.com/boardgamedesigner/2937/christopher-wroth) branded as 
[King's Court](https://boardgamegeek.com/boardgame/5157/kings-court) and published by 
[Golden](https://boardgamegeek.com/boardgamepublisher/247/golden), 
[MW Games](https://boardgamegeek.com/boardgamepublisher/25852/mw-games), 
[Western Publishing Company](https://boardgamegeek.com/boardgamepublisher/5700/western-publishing-company).

Rules
-----

*(From [Board Game Geek](https://boardgamegeek.com/boardgame/5157/kings-court))*

The board is 8x8. The central 4x4 area forms the King's Court. The starting setup places the X and O pieces on the 48
squares surrounding the Court. The opening two moves have both players enter a piece onto the Court from opposing sides
(no jumping yet).

From that point on, a piece must be present on the Court at all times - otherwise the player loses. Pieces move as in
[Checkers](https://boardgamegeek.com/boardgame/2083/checkers) except they all move as Kings (no restrictions on
direction). Jumps are again as in [Checkers](https://boardgamegeek.com/boardgame/2083/checkers), except that you can
jump your own pieces as well (without capturing them, of course).

Installation
------------

You will need at least version 3.7 of [python](https://www.python.org) and 
[pipenv](https://pipenv.kennethreitz.org/en/latest/) to play. 

1. To install `python3` and `pipenv`, use [homebrew](https://github.com/Homebrew/brew) for 
[macOS](https://www.apple.com/macos/).

    ```shell script
    $ brew install python@3
    $ brew install pipenv
    ```

2. Confirm which version you have.

    ```shell script
    $ python3 --version
    ```

3. Clone the repository.

    ```shell script
    $ git clone https://github.com/mikegoodspeed/supercheckers-python.git
    $ cd supercheckers-python
    ```

4. Create the virtual environment.

    ```shell script
    $ pipenv install
    ```

5. Optionally, you can install the virtual environment in **developer mode**.

    ```shell script
    $ pipenv install --dev
    ```

Play
----

To start the game, simply run `supercheckers` or to make sure you're running it in the right environment, use `pipenv`.

```shell script
$ pipenv run supercheckers
```

```
Beginning game...
   A B C D E F G H
  +---------------+
8 |X|O|X|O|X|O|X|O| 8
7 |O|X|O|X|O|X|O|X| 7
6 |X|O# # # # #X|O| 6
5 |O|X# # # # #O|X| 5
4 |X|O# # # # #X|O| 4
3 |O|X# # # # #O|X| 3
2 |X|O|X|O|X|O|X|O| 2
1 |O|X|O|X|O|X|O|X| 1
  +---------------+
   A B C D E F G H
Player X move: c2 c3
   A B C D E F G H
  +---------------+
8 |X|O|X|O|X|O|X|O| 8
7 |O|X|O|X|O|X|O|X| 7
6 |X|O# # # # #X|O| 6
5 |O|X# # # # #O|X| 5
4 |X|O# # # # #X|O| 4
3 |O|X#X# # # #O|X| 3
2 |X|O| |O|X|O|X|O| 2
1 |O|X|O|X|O|X|O|X| 1
  +---------------+
   A B C D E F G H
Player O move: d2 d4
ERROR: For your first two moves, you must slide into the middle.
ERROR: All jumps must be over a piece.
Player O move: d2 d3
   A B C D E F G H
  +---------------+
8 |X|O|X|O|X|O|X|O| 8
7 |O|X|O|X|O|X|O|X| 7
6 |X|O# # # # #X|O| 6
5 |O|X# # # # #O|X| 5
4 |X|O# # # # #X|O| 4
3 |O|X#X#O# # #O|X| 3
2 |X|O| | |X|O|X|O| 2
1 |O|X|O|X|O|X|O|X| 1
  +---------------+
   A B C D E F G H
```

Develop
-------

For development, make sure you are in **developer mode** and activate the `pipenv` environment.

```shell script
$ pipenv shell
```

Supercheckers uses [invoke](https://www.pyinvoke.org) task automation, similar to 
[make](https://www.gnu.org/software/make/) or [rake](https://ruby.github.io/rake/).  You can see available tasks by
asking `invoke`.

```shell script
$ invoke --list
```

```
Available tasks:

  build    Build a package.
  check    Check for style and static typing errors.
  clean    Clean unused files.
  format   Format code to adhere to best style guidelines.
  run      Run the program.
  test     Run tests.
```
