import curses, math, sys, os
from typing import Tuple, List, Optional

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from rogue_game.domain.entities import GameSession, Level, Room, Character, Enemy, Item, Door
from rogue_game.domain.enums import ItemType, KeyColor, EnemyType


class ColorManager:
    WALL       = 1
    FLOOR      = 2
    PLAYER     = 3
    ENEMY      = 4
    ITEM       = 5
    CORRIDOR   = 6
    EXIT       = 7
    TEXT       = 8
    ENEMY_ZOMBIE  = 9
    ENEMY_VAMPIRE = 10
    ENEMY_GHOST   = 11
    ENEMY_OGRE    = 12
    ENEMY_SNAKE   = 13
    DOOR_RED    = 14
    DOOR_GREEN  = 15
    DOOR_BLUE   = 16
    DOOR_YELLOW = 17
    KEY_COLOR   = 18
    CEILING     = 19
    GROUND      = 20

    @staticmethod
    def init_colors(_):
        try:
            curses.init_pair(ColorManager.WALL,        curses.COLOR_BLUE,    curses.COLOR_BLACK)
            curses.init_pair(ColorManager.FLOOR,       curses.COLOR_WHITE,   curses.COLOR_BLACK)
            curses.init_pair(ColorManager.PLAYER,      curses.COLOR_YELLOW,  curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ENEMY,       curses.COLOR_RED,     curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ITEM,        curses.COLOR_GREEN,   curses.COLOR_BLACK)
            curses.init_pair(ColorManager.CORRIDOR,    curses.COLOR_BLACK,   curses.COLOR_BLACK)
            curses.init_pair(ColorManager.EXIT,        curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(ColorManager.TEXT,        curses.COLOR_WHITE,   curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ENEMY_ZOMBIE,  curses.COLOR_GREEN,  curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ENEMY_VAMPIRE, curses.COLOR_RED,    curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ENEMY_GHOST,   curses.COLOR_WHITE,  curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ENEMY_OGRE,    curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(ColorManager.ENEMY_SNAKE,   curses.COLOR_WHITE,  curses.COLOR_BLACK)
            curses.init_pair(ColorManager.DOOR_RED,    curses.COLOR_RED,     curses.COLOR_BLACK)
            curses.init_pair(ColorManager.DOOR_GREEN,  curses.COLOR_GREEN,   curses.COLOR_BLACK)
            curses.init_pair(ColorManager.DOOR_BLUE,   curses.COLOR_BLUE,    curses.COLOR_BLACK)
            curses.init_pair(ColorManager.DOOR_YELLOW, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
            curses.init_pair(ColorManager.KEY_COLOR,   curses.COLOR_CYAN,    curses.COLOR_BLACK)
            curses.init_pair(ColorManager.CEILING,     curses.COLOR_BLUE,    curses.COLOR_BLACK)
            curses.init_pair(ColorManager.GROUND,      curses.COLOR_WHITE,   curses.COLOR_BLACK)
        except Exception:
            pass

    @staticmethod
    def door_color_pair(color: KeyColor) -> int:
        return {
            KeyColor.RED:    ColorManager.DOOR_RED,
            KeyColor.GREEN:  ColorManager.DOOR_GREEN,
            KeyColor.BLUE:   ColorManager.DOOR_BLUE,
            KeyColor.YELLOW: ColorManager.DOOR_YELLOW,
        }.get(color, ColorManager.WALL)


class GameRenderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        main_h = max(10, self.height - 10)
        status_h = min(10, self.height - main_h)
        try:
            self.main_window   = stdscr.subwin(main_h,   self.width, 0,      0)
            self.status_window = stdscr.subwin(status_h, self.width, main_h, 0)
        except Exception:
            self.main_window   = stdscr
            self.status_window = stdscr
        ColorManager.init_colors(stdscr)

    def render(self, session: GameSession) -> None:
        self.main_window.clear()
        self.status_window.clear()
        if session.current_level:
            vw = self.width
            vh = self.height - 10
            cx = session.character.x - vw // 4
            cy = session.character.y - vh // 3
            cx = max(0, cx); cy = max(0, cy)
            self._render_level(session.character, session.current_level, cx, cy)
        self._render_status_panel(session)
        self.main_window.refresh()
        self.status_window.refresh()

    def _render_level(self, player, level, cx, cy):
        for room in level.rooms:
            self._render_room(room, player, cx, cy)
        for corridor in level.corridors:
            self._render_corridor(corridor, level, cx, cy)
        # Doors
        for door in level.doors:
            self._render_door(door, cx, cy)
        for room in level.rooms:
            for item in room.items:
                if self._is_visible(item.x, item.y, player):
                    self._render_item(item, cx, cy)
            for enemy in room.enemies:
                if enemy.is_alive() and self._is_visible(enemy.x, enemy.y, player):
                    self._render_enemy(enemy, cx, cy)
        # Render exit '>' AFTER enemies/items so it's never overwritten
        mh, mw = self.main_window.getmaxyx()
        for room in level.rooms:
            if room.is_exit_room:
                ex = room.x + room.width  // 2
                ey = room.y + room.height // 2
                sx = ex - cx; sy = ey - cy
                if 0 <= sx < mw and 0 <= sy < mh:
                    self._safe_addch(sx, sy, '>', curses.color_pair(ColorManager.EXIT))
        self._render_player(player, cx, cy)

    def _render_room(self, room, player, cx, cy):
        if not self._is_room_discovered(room, player):
            return
        mh, mw = self.main_window.getmaxyx()
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                sx = x - cx; sy = y - cy
                if sx < 0 or sx >= mw or sy < 0 or sy >= mh:
                    continue
                lx = x - room.x; ly = y - room.y
                is_wall = (lx == 0 or lx == room.width-1 or
                           ly == 0 or ly == room.height-1)
                if is_wall:
                    self._safe_addch(sx, sy, '#', curses.color_pair(ColorManager.WALL))
                else:
                    self._safe_addch(sx, sy, '.', curses.color_pair(ColorManager.FLOOR))
        # Exit '>' is rendered separately in _render_level (after enemies/items)

    def _render_corridor(self, corridor, level, cx, cy):
        if not corridor.tiles:
            return
        mh, mw = self.main_window.getmaxyx()
        corridor_set = set(corridor.tiles)
        for x, y in corridor.tiles:
            sx = x - cx; sy = y - cy
            if sx < 0 or sx >= mw or sy < 0 or sy >= mh:
                continue
            self._safe_addch(sx, sy, ' ', curses.color_pair(ColorManager.FLOOR))
            for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                ax, ay = x+dx, y+dy
                if (ax, ay) in corridor_set:
                    continue
                if any(r.contains_point(ax, ay) for r in level.rooms):
                    continue
                if any((ax, ay) in c.tiles for c in level.corridors if c != corridor):
                    continue
                sax = ax - cx; say = ay - cy
                if 0 <= sax < mw and 0 <= say < mh:
                    self._safe_addch(sax, say, '#', curses.color_pair(ColorManager.WALL))

    def _render_door(self, door: Door, cx, cy):
        mh, mw = self.main_window.getmaxyx()
        sx = door.x - cx; sy = door.y - cy
        if sx < 0 or sx >= mw or sy < 0 or sy >= mh:
            return
        if door.is_passable():
            ch = '_'
        else:
            ch = '+'
        pair = curses.color_pair(ColorManager.door_color_pair(door.color))
        self._safe_addch(sx, sy, ch, pair | curses.A_BOLD)

    def _render_item(self, item: Item, cx, cy):
        chars = {
            ItemType.FOOD:     '%',
            ItemType.ELIXIR:   '!',
            ItemType.SCROLL:   '?',
            ItemType.WEAPON:   '/',
            ItemType.TREASURE: '$',
            ItemType.KEY:      'k',
        }
        ch = chars.get(item.item_type, '*')
        sx = item.x - cx; sy = item.y - cy
        mh, mw = self.main_window.getmaxyx()
        if 0 <= sx < mw and 0 <= sy < mh:
            attr = curses.color_pair(ColorManager.KEY_COLOR) if item.item_type == ItemType.KEY \
                else curses.color_pair(ColorManager.ITEM)
            self._safe_addch(sx, sy, ch, attr)

    def _render_enemy(self, enemy: Enemy, cx, cy):
        ch = enemy.get_display_char()
        color_map = {
            EnemyType.ZOMBIE:     ColorManager.ENEMY_ZOMBIE,
            EnemyType.VAMPIRE:    ColorManager.ENEMY_VAMPIRE,
            EnemyType.GHOST:      ColorManager.ENEMY_GHOST,
            EnemyType.OGRE:       ColorManager.ENEMY_OGRE,
            EnemyType.SNAKE_MAGE: ColorManager.ENEMY_SNAKE,
            EnemyType.MIMIC:      ColorManager.ENEMY_GHOST,
        }
        pair = color_map.get(enemy.enemy_type, ColorManager.ENEMY)
        sx = enemy.x - cx; sy = enemy.y - cy
        mh, mw = self.main_window.getmaxyx()
        if 0 <= sx < mw and 0 <= sy < mh:
            self._safe_addch(sx, sy, ch, curses.color_pair(pair))

    def _render_player(self, player, cx, cy):
        sx = player.x - cx; sy = player.y - cy
        mh, mw = self.main_window.getmaxyx()
        if 0 <= sx < mw and 0 <= sy < mh:
            self._safe_addch(sx, sy, '@',
                             curses.color_pair(ColorManager.PLAYER) | curses.A_BOLD)

    def _render_status_panel(self, session: GameSession):
        char = session.character
        lines = [
            f"Level: {session.current_level_number}/21 | "
            f"HP: {char.health}/{char.max_health} | "
            f"STR: {char.strength} | DEX: {char.get_effective_dexterity()}",
            f"Treasure: {session.statistics.treasure_collected} | "
            f"Enemies: {session.statistics.enemies_defeated} | "
            f"Difficulty: x{session.difficulty.difficulty_modifier:.2f}",
            f"Weapon: {char.current_weapon if char.current_weapon else 'Unarmed'} | "
            f"Items: {sum(len(v) for v in char.backpack.items.values())}/99",
            "",
            "WASD=Move | H=Weapon | J=Food | K=Elixir | E=Scroll | "
            "I=Inventory | TAB=3D Mode | ESC=Menu",
        ]
        mh, mw = self.status_window.getmaxyx()
        for i, line in enumerate(lines):
            if i < mh:
                try:
                    self.status_window.addstr(i, 0, line[:mw-1])
                except curses.error:
                    pass

    def _is_room_discovered(self, room, player) -> bool:
        return True   # show all (fog-of-war is done in visibility check)

    def _is_visible(self, x, y, player) -> bool:
        d = math.sqrt((x - player.x)**2 + (y - player.y)**2)
        return d < 20

    def _safe_addch(self, x, y, char, attr):
        try:
            mh, mw = self.main_window.getmaxyx()
            if 0 <= y < mh and 0 <= x < mw:
                self.main_window.addch(y, x, ord(char) if isinstance(char, str) else char, attr)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Bonus Task 9 – 3-D ray-cast renderer
# ---------------------------------------------------------------------------
# Wall shading chars: nearest → darkest
_SHADE = ['█', '▓', '▒', '░', '·']   # fallback if Unicode unsupported: #Xx-·

def _shade_char(dist: float) -> str:
    idx = min(int(dist / 3), len(_SHADE) - 1)
    return _SHADE[idx]


class Renderer3D:
    """First-person ray-cast renderer using curses."""

    FOV   = math.pi / 3.0   # 60°
    DEPTH = 30.0             # max render distance

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        main_h = max(10, self.height - 10)
        status_h = min(10, self.height - main_h)
        try:
            self.main_window   = stdscr.subwin(main_h,   self.width, 0,      0)
            self.status_window = stdscr.subwin(status_h, self.width, main_h, 0)
        except Exception:
            self.main_window   = stdscr
            self.status_window = stdscr
        ColorManager.init_colors(stdscr)

    def render(self, session: GameSession) -> None:
        self.main_window.clear()
        self.status_window.clear()

        if session.current_level:
            self._render_3d_view(session)
            self._render_minimap(session)

        self._render_status_3d(session)
        self.main_window.refresh()
        self.status_window.refresh()

    def _render_3d_view(self, session: GameSession):
        player = session.character
        level  = session.current_level
        mh, mw = self.main_window.getmaxyx()

        px = player.view_x
        py = player.view_y
        angle = player.view_angle

        half_fov = self.FOV / 2.0

        for col in range(mw):
            ray_angle = angle - half_fov + self.FOV * col / mw
            dist, wall_type = self._cast_ray(level, px, py, ray_angle)

            # Wall height (in rows)
            if dist < 0.001:
                wall_h = mh
            else:
                wall_h = min(mh, int(mh / dist))

            wall_top    = max(0, (mh - wall_h) // 2)
            wall_bottom = min(mh, wall_top + wall_h)

            shade = _shade_char(dist)
            wall_attr = curses.color_pair(ColorManager.WALL)
            if dist < 3:
                wall_attr |= curses.A_BOLD

            # Ceiling
            for row in range(wall_top):
                self._safe_addch3d(col, row, '~',
                                   curses.color_pair(ColorManager.CEILING))
            # Wall
            for row in range(wall_top, wall_bottom):
                self._safe_addch3d(col, row, shade, wall_attr)
            # Floor
            fd = (mh - row) / mh if mh > 0 else 1
            for row in range(wall_bottom, mh):
                fc = _shade_char(self.DEPTH * (1 - row / mh) * 2)
                self._safe_addch3d(col, row, fc,
                                   curses.color_pair(ColorManager.GROUND))

    def _cast_ray(self, level: Level, px: float, py: float,
                  angle: float) -> Tuple:
        """DDA ray casting. Returns (distance, wall_type_str)."""
        ray_dx = math.cos(angle)
        ray_dy = math.sin(angle)

        # Tile position
        map_x = int(px)
        map_y = int(py)

        # Length of ray from one x/y-side to next
        delta_dist_x = abs(1 / ray_dx) if ray_dx != 0 else 1e30
        delta_dist_y = abs(1 / ray_dy) if ray_dy != 0 else 1e30

        # Step and initial side dist
        if ray_dx < 0:
            step_x = -1; side_dist_x = (px - map_x) * delta_dist_x
        else:
            step_x =  1; side_dist_x = (map_x + 1 - px) * delta_dist_x
        if ray_dy < 0:
            step_y = -1; side_dist_y = (py - map_y) * delta_dist_y
        else:
            step_y =  1; side_dist_y = (map_y + 1 - py) * delta_dist_y

        hit = False
        side = 0   # 0 = x-side, 1 = y-side
        wall_type = 'wall'

        for _ in range(int(self.DEPTH * 2)):
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if level.is_wall(map_x, map_y):
                hit = True
                # Check if it's a door
                door = level.get_door_at(map_x, map_y)
                if door:
                    wall_type = 'door_' + door.color.name
                break

        if not hit:
            return self.DEPTH, wall_type

        if side == 0:
            dist = side_dist_x - delta_dist_x
        else:
            dist = side_dist_y - delta_dist_y

        # Fisheye correction: multiply by cos of relative angle
        # (already perpendicular distance from DDA, no extra cos needed)
        return max(0.01, dist), wall_type

    def _render_minimap(self, session: GameSession):
        """Top-right 2D minimap (20×10 chars)."""
        player = session.character
        level  = session.current_level
        mh, mw = self.main_window.getmaxyx()

        map_w = min(40, mw // 3)
        map_h = min(20, mh // 3)
        ox = mw - map_w - 1
        oy = 0

        # Determine world bounding box
        all_x = [t[0] for c in level.corridors for t in c.tiles] + \
                [r.x for r in level.rooms] + [r.x+r.width for r in level.rooms]
        all_y = [t[1] for c in level.corridors for t in c.tiles] + \
                [r.y for r in level.rooms] + [r.y+r.height for r in level.rooms]
        if not all_x:
            return
        world_x1 = min(all_x); world_x2 = max(all_x)
        world_y1 = min(all_y); world_y2 = max(all_y)
        wx_range = max(1, world_x2 - world_x1)
        wy_range = max(1, world_y2 - world_y1)

        def world_to_map(wx, wy):
            mx = ox + int((wx - world_x1) / wx_range * (map_w - 1))
            my = oy + int((wy - world_y1) / wy_range * (map_h - 1))
            return mx, my

        # Draw rooms
        for room in level.rooms:
            for ry in range(room.y, room.y + room.height):
                for rx in range(room.x, room.x + room.width):
                    sx, sy = world_to_map(rx, ry)
                    lx = rx - room.x; ly = ry - room.y
                    is_wall = (lx == 0 or lx == room.width-1 or
                               ly == 0 or ly == room.height-1)
                    ch = '#' if is_wall else '.'
                    pair = ColorManager.WALL if is_wall else ColorManager.FLOOR
                    self._safe_addch3d(sx, sy, ch, curses.color_pair(pair))

        # Corridors
        for corridor in level.corridors:
            for tx, ty in corridor.tiles:
                sx, sy = world_to_map(tx, ty)
                self._safe_addch3d(sx, sy, ' ', curses.color_pair(ColorManager.FLOOR))

        # Exit
        exit_room = level.get_room(level.exit_room_id)
        if exit_room:
            ex = exit_room.x + exit_room.width  // 2
            ey = exit_room.y + exit_room.height // 2
            sx, sy = world_to_map(ex, ey)
            self._safe_addch3d(sx, sy, '>', curses.color_pair(ColorManager.EXIT))

        # Doors
        for door in level.doors:
            sx, sy = world_to_map(door.x, door.y)
            pair = ColorManager.door_color_pair(door.color)
            self._safe_addch3d(sx, sy, '+', curses.color_pair(pair) | curses.A_BOLD)

        # Player arrow based on angle
        arrows = ['→', '↗', '↑', '↖', '←', '↙', '↓', '↘']
        idx = int((player.view_angle % (2*math.pi)) / (2*math.pi) * 8) % 8
        arrow = arrows[idx]
        px_m, py_m = world_to_map(int(player.view_x), int(player.view_y))
        self._safe_addch3d(px_m, py_m, '@',
                           curses.color_pair(ColorManager.PLAYER) | curses.A_BOLD)

    def _render_status_3d(self, session: GameSession):
        char = session.character
        mh, mw = self.status_window.getmaxyx()
        deg = int(math.degrees(char.view_angle) % 360)
        lines = [
            f"Level: {session.current_level_number}/21 | "
            f"HP: {char.health}/{char.max_health} | "
            f"Angle: {deg}°",
            f"Treasure: {session.statistics.treasure_collected} | "
            f"Enemies: {session.statistics.enemies_defeated}",
            f"Weapon: {char.current_weapon if char.current_weapon else 'Unarmed'}",
            "",
            "W=Forward S=Back A=TurnLeft D=TurnRight | "
            "H/J/K/E=Items | TAB=2D Mode | ESC=Menu",
        ]
        for i, line in enumerate(lines):
            if i < mh:
                try:
                    self.status_window.addstr(i, 0, line[:mw-1])
                except curses.error:
                    pass

    def _safe_addch3d(self, x, y, char, attr):
        try:
            mh, mw = self.main_window.getmaxyx()
            if 0 <= y < mh and 0 <= x < mw:
                self.main_window.addch(y, x,
                                       ord(char) if isinstance(char, str) else char,
                                       attr)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Menu, Inventory, Leaderboard (unchanged structure, minor additions)
# ---------------------------------------------------------------------------
class MenuRenderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        ColorManager.init_colors(stdscr)

    def render_main_menu(self) -> str:
        self.stdscr.clear()
        items = ["1. New Game", "2. Continue Game",
                 "3. View Leaderboard", "4. Quit"]
        y = self.height // 2 - len(items) // 2
        try:
            self.stdscr.addstr(y-2, self.width//2-10,
                               "===== ROGUE 1980 =====", curses.A_BOLD)
            for i, item in enumerate(items):
                self.stdscr.addstr(y+i, self.width//2-10, item)
            self.stdscr.addstr(self.height-2, 0, "Press number key to select")
        except curses.error:
            pass
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        while True:
            key = self.stdscr.getch()
            if 0 <= key < 256:
                ch = chr(key)
                if ch in '1234':
                    self.stdscr.nodelay(True)
                    return ch

    def render_game_over(self, session: GameSession) -> None:
        self.stdscr.clear()
        y = self.height // 2 - 5
        try:
            self.stdscr.addstr(y,   self.width//2-15,
                               "===== GAME OVER =====", curses.A_BOLD)
            self.stdscr.addstr(y+2, self.width//2-20,
                               f"Final Level:  {session.statistics.level_reached}")
            self.stdscr.addstr(y+3, self.width//2-20,
                               f"Treasure:     {session.statistics.treasure_collected}")
            self.stdscr.addstr(y+4, self.width//2-20,
                               f"Enemies:      {session.statistics.enemies_defeated}")
            self.stdscr.addstr(y+6, self.width//2-20, "Press any key…")
        except curses.error:
            pass
        self.stdscr.refresh()
        self.stdscr.getch()


class InventoryRenderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

    def show_inventory(self, character: Character) -> None:
        self.stdscr.clear()
        try:
            self.stdscr.addstr(0, 0, "===== INVENTORY =====", curses.A_BOLD)
            y = 2
            for subtype, items in character.backpack.items.items():
                if not items:
                    continue
                name = subtype.name if hasattr(subtype, 'name') else str(subtype)
                self.stdscr.addstr(y, 0, f"{name}: ({len(items)})")
                for i, item in enumerate(items[:15]):
                    self.stdscr.addstr(y+1+i, 2, str(item)[:self.width-4])
                y += len(items[:15]) + 2
            self.stdscr.addstr(self.height-1, 0, "Press any key to close")
        except curses.error:
            pass
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)


class LeaderboardRenderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

    def show_leaderboard(self, highscores: list) -> None:
        self.stdscr.clear()
        sorted_scores = sorted(highscores,
                               key=lambda x: x.get('treasure', 0), reverse=True)
        try:
            self.stdscr.addstr(0, 0, "===== LEADERBOARD =====", curses.A_BOLD)
            self.stdscr.addstr(2, 0,
                f"{'Rank':<5} {'Lvl':<6} {'Treasure':<10} {'Enemies':<10}")
            self.stdscr.addstr(3, 0, "-" * 35)
            for i, s in enumerate(sorted_scores[:self.height-6]):
                line = (f"{i+1:<5} {s.get('level',0):<6} "
                        f"{s.get('treasure',0):<10} "
                        f"{s.get('enemies_defeated',0):<10}")
                self.stdscr.addstr(4+i, 0, line)
            self.stdscr.addstr(self.height-1, 0, "Press any key to return")
        except curses.error:
            pass
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)
