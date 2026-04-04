import curses
import time
from typing import Optional


class InputManager:
    """Handles keyboard input"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        stdscr.nodelay(True)  # Non-blocking input
        stdscr.keypad(True)   # Enable special keys
        self.last_input_time = 0
    
    def get_key(self) -> Optional[int]:
        """Get the next key pressed, return None if no key"""
        try:
            key = self.stdscr.getch()
            if key == -1:
                # No key pressed - add a small delay to prevent CPU spinning
                time.sleep(0.01)
                return None
            return key
        except:
            time.sleep(0.01)
            return None
    
    def wait_for_key(self) -> int:
        """Block until a key is pressed"""
        self.stdscr.nodelay(False)
        key = self.stdscr.getch()
        self.stdscr.nodelay(True)
        return key

class DialogManager:
    """Handles dialog boxes and selections"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
    
    def select_item(self, items: list, title: str = "Select Item") -> Optional[int]:
        """Display selection dialog, return selected index or None"""
        if not items:
            return None
        
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"===== {title} =====", curses.A_BOLD)
        
        for i, item in enumerate(items):
            self.stdscr.addstr(2 + i, 2, f"{i + 1}. {str(item)}")
        
        self.stdscr.addstr(len(items) + 3, 0, "Enter number (or 0 to cancel): ", curses.A_NORMAL)
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        
        while True:
            key = self.stdscr.getch()
            if key >= 0 and key < 256:
                try:
                    choice = int(chr(key))
                    if 1 <= choice <= len(items):
                        self.stdscr.nodelay(True)
                        return choice - 1
                    elif choice == 0:
                        self.stdscr.nodelay(True)
                        return None
                except:
                    pass
    
    def show_message(self, title: str, message: str) -> None:
        """Display a message dialog"""
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"===== {title} =====", curses.A_BOLD)
        
        lines = message.split('\n')
        for i, line in enumerate(lines):
            self.stdscr.addstr(2 + i, 2, line)
        
        self.stdscr.addstr(len(lines) + 3, 0, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)
