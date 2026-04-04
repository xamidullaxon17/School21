#!/usr/bin/env python3
"""
Rogue 1980 Game Launcher
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        import curses
        from rogue_game.game_controller import GameController
        
        def main(stdscr):
            """Main game entry point"""
            try:
                # Configure curses
                curses.curs_set(0)  # Hide cursor
                stdscr.nodelay(True)  # Non-blocking input
                stdscr.keypad(True)  # Enable special keys
                
                # Initialize and run game
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
        
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
