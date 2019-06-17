import argparse
import GameView

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('GAMES_NUMBER',
                        nargs='?',
                        default=20,
                        action="store",
                        help="set the number of games to train the agent")
    args = parser.parse_args()

GameView.GameView(1200, 760).main_menu(int(args.GAMES_NUMBER))
# TODO: scala a 640,480
# GameView.GameView(640, 480).main_menu(int(args.GAMES_NUMBER))
