import curses
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_controller import GameController


def main(stdscr):
    """Main game entry point"""
    try:
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        
        game = GameController(stdscr)
        game.run()
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise
    finally:
        curses.curs_set(1)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
