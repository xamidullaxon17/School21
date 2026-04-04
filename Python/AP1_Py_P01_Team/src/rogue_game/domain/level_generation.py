import random, sys, os
from collections import deque
from typing import List, Tuple, Set, Dict, Optional

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from rogue_game.domain.entities import Room, Corridor, Level, Enemy, Item, Character, Door
from rogue_game.domain.enums import EnemyType, ItemType, ItemSubtype, KeyColor
from rogue_game.domain.game_logic import LevelDifficulty, GameRules

KEY_COLOR_SUBTYPES = {
    KeyColor.RED:    ItemSubtype.KEY_RED,
    KeyColor.GREEN:  ItemSubtype.KEY_GREEN,
    KeyColor.BLUE:   ItemSubtype.KEY_BLUE,
    KeyColor.YELLOW: ItemSubtype.KEY_YELLOW,
}


class LevelGenerator:
    MIN_ROOM_WIDTH  = 5
    MIN_ROOM_HEIGHT = 5
    MAX_ROOM_WIDTH  = 12
    MAX_ROOM_HEIGHT = 12
    GRID_SIZE        = 3
    SECTION_WIDTH    = 30
    SECTION_HEIGHT   = 20

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.seed = seed

    def generate_level(self, level_number: int,
                       difficulty_modifier: float = 1.0) -> Level:
        level = Level(level_number=level_number)

        rooms = self._generate_rooms()
        level.rooms = rooms

        corridors = self._generate_corridors(rooms)
        level.corridors = corridors

        level.room_connections = self._build_room_connections(rooms, corridors)

        level.starting_room_id = rooms[0].room_id
        level.exit_room_id     = rooms[-1].room_id
        rooms[0].is_starting_room = True
        rooms[-1].is_exit_room    = True

        self._generate_doors_and_keys(level)

        self._populate_level(level, level_number, difficulty_modifier)
        return level

    def _generate_rooms(self) -> List[Room]:
        rooms = []
        room_id = 0
        for grid_y in range(self.GRID_SIZE):
            for grid_x in range(self.GRID_SIZE):
                w = random.randint(self.MIN_ROOM_WIDTH,  self.MAX_ROOM_WIDTH)
                h = random.randint(self.MIN_ROOM_HEIGHT, self.MAX_ROOM_HEIGHT)
                sx = grid_x * self.SECTION_WIDTH
                sy = grid_y * self.SECTION_HEIGHT
                x = sx + random.randint(1, max(1, self.SECTION_WIDTH  - w - 1))
                y = sy + random.randint(1, max(1, self.SECTION_HEIGHT - h - 1))
                rooms.append(Room(room_id=room_id, grid_x=grid_x, grid_y=grid_y,
                                  x=x, y=y, width=w, height=h))
                room_id += 1
        return rooms


    def _generate_corridors(self, rooms: List[Room]) -> List[Corridor]:
        corridors = []
        corridor_id = 0
        room_map = {(r.grid_x, r.grid_y): r for r in rooms}

        visited = set()
        connections = []

        def dfs(gx, gy):
            visited.add((gx, gy))
            neighbors = [(gx+1,gy),(gx-1,gy),(gx,gy+1),(gx,gy-1)]
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if 0 <= nx < self.GRID_SIZE and 0 <= ny < self.GRID_SIZE:
                    if (nx, ny) not in visited:
                        connections.append(((gx, gy), (nx, ny)))
                        dfs(nx, ny)

        dfs(0, 0)

        for (x1,y1),(x2,y2) in connections:
            r1, r2 = room_map[(x1,y1)], room_map[(x2,y2)]
            tiles = self._generate_corridor_tiles(r1, r2)
            corridors.append(Corridor(corridor_id=corridor_id,
                                      room1_id=r1.room_id, room2_id=r2.room_id,
                                      tiles=tiles))
            corridor_id += 1
        return corridors

    def _generate_corridor_tiles(self, r1: Room, r2: Room) -> List[Tuple[int,int]]:
        tiles = []
        cx1 = r1.x + r1.width  // 2
        cy1 = r1.y + r1.height // 2
        cx2 = r2.x + r2.width  // 2
        cy2 = r2.y + r2.height // 2
        x, y = cx1, cy1
        dx = 1 if cx2 > x else -1
        while x != cx2:
            tiles.append((x, y))
            x += dx
        dy = 1 if cy2 > y else -1
        while y != cy2:
            tiles.append((x, y))
            y += dy
        tiles.append((x, y))
        return tiles

    def _build_room_connections(self, rooms, corridors) -> Dict[int, List[int]]:
        conn = {r.room_id: [] for r in rooms}
        for c in corridors:
            conn[c.room1_id].append(c.room2_id)
            conn[c.room2_id].append(c.room1_id)
        return conn

    # ------------------------------------------------------------------
    # Bonus Task 6 – doors + keys + softlock check
    # ------------------------------------------------------------------
    def _generate_doors_and_keys(self, level: Level) -> None:
        """Place at most 3 locked doors on corridors, put keys in reachable rooms."""
        colors = [KeyColor.RED, KeyColor.GREEN, KeyColor.BLUE, KeyColor.YELLOW]
        random.shuffle(colors)

        # Candidate corridors: all except the one directly connecting
        # starting room to any neighbour (we don't want to lock the first exit)
        start_id = level.starting_room_id
        candidate_corridors = [
            c for c in level.corridors
            if c.room1_id != start_id and c.room2_id != start_id
        ]

        placed = 0
        for corridor in candidate_corridors:
            if placed >= 3:
                break
            if not corridor.tiles:
                continue

            color = colors[placed]
            # Mid-tile of corridor becomes the door
            mid_idx = len(corridor.tiles) // 2
            dx, dy = corridor.tiles[mid_idx]

            # BFS: rooms reachable from start WITHOUT using this corridor
            reachable_without = self._rooms_reachable_without_corridor(
                level, start_id, corridor.corridor_id)

            # Key must be in a reachable room (not exit room, not the locked side)
            key_rooms = [
                r for r in level.rooms
                if r.room_id in reachable_without
                and not r.is_starting_room
                and not r.is_exit_room
            ]
            if not key_rooms:
                continue   # would cause softlock → skip

            # Place door
            door = Door(x=dx, y=dy, color=color)
            level.doors.append(door)

            # Place key in a random accessible room
            key_room = random.choice(key_rooms)
            for _ in range(20):
                kx = random.randint(key_room.x + 1, key_room.x + key_room.width  - 2)
                ky = random.randint(key_room.y + 1, key_room.y + key_room.height - 2)
                if key_room.is_walkable(kx, ky):
                    key_item = Item(item_type=ItemType.KEY,
                                    subtype=KEY_COLOR_SUBTYPES[color],
                                    x=kx, y=ky)
                    key_room.items.append(key_item)
                    break

            placed += 1

    def _rooms_reachable_without_corridor(self, level: Level,
                                          start_id: int,
                                          excluded_corridor_id: int) -> Set[int]:
        """BFS on room graph ignoring one corridor."""
        reachable = set()
        queue = deque([start_id])
        reachable.add(start_id)
        # Build adjacency skipping excluded corridor
        adj: Dict[int, List[int]] = {r.room_id: [] for r in level.rooms}
        for c in level.corridors:
            if c.corridor_id == excluded_corridor_id:
                continue
            adj[c.room1_id].append(c.room2_id)
            adj[c.room2_id].append(c.room1_id)

        while queue:
            node = queue.popleft()
            for nb in adj[node]:
                if nb not in reachable:
                    reachable.add(nb)
                    queue.append(nb)
        return reachable

    # ------------------------------------------------------------------
    # Populate with enemies and items
    # ------------------------------------------------------------------
    def _populate_level(self, level: Level, level_number: int,
                        difficulty_modifier: float) -> None:
        enemy_count = LevelDifficulty.get_enemy_count(level_number, difficulty_modifier)
        non_start   = [r for r in level.rooms if not r.is_starting_room]

        for _ in range(enemy_count):
            room   = random.choice(non_start)
            enemy  = self._create_enemy(level_number, difficulty_modifier)
            for _ in range(10):
                ex = random.randint(room.x+1, room.x+room.width-2)
                ey = random.randint(room.y+1, room.y+room.height-2)
                if room.is_walkable(ex, ey):
                    enemy.x = ex; enemy.y = ey; enemy.room_id = room.room_id
                    room.enemies.append(enemy)
                    break

        drop_rate = LevelDifficulty.get_item_droprate(level_number, difficulty_modifier)
        for room in level.rooms:
            if room.is_starting_room:
                continue
            if random.random() < 0.3:
                treasure = self._create_treasure(level_number)
                for _ in range(10):
                    tx = random.randint(room.x+1, room.x+room.width-2)
                    ty = random.randint(room.y+1, room.y+room.height-2)
                    if room.is_walkable(tx, ty):
                        treasure.x = tx; treasure.y = ty
                        room.items.append(treasure)
                        break

            if random.random() < drop_rate:
                item = GameRules.create_random_item(level_number)
                if item:
                    for _ in range(10):
                        ix = random.randint(room.x+1, room.x+room.width-2)
                        iy = random.randint(room.y+1, room.y+room.height-2)
                        if room.is_walkable(ix, iy):
                            item.x = ix; item.y = iy
                            room.items.append(item)
                            break

    def _create_enemy(self, level_number: int,
                      modifier: float = 1.0) -> Enemy:
        # Mimic only appears from level 5+
        choices = [EnemyType.ZOMBIE, EnemyType.VAMPIRE, EnemyType.GHOST,
                   EnemyType.OGRE, EnemyType.SNAKE_MAGE]
        if level_number >= 5:
            choices.append(EnemyType.MIMIC)

        enemy_type = random.choice(choices)
        health, dex, strength = LevelDifficulty.scale_enemy_stats(
            enemy_type, level_number, modifier)

        hostility_base = {
            EnemyType.ZOMBIE:     5,
            EnemyType.VAMPIRE:    8,
            EnemyType.GHOST:      4,
            EnemyType.OGRE:       5,
            EnemyType.SNAKE_MAGE: 8,
            EnemyType.MIMIC:      2,   # low hostility
        }
        hostility = hostility_base[enemy_type] + level_number // 3

        enemy = Enemy(enemy_type=enemy_type, health=health, max_health=health,
                      dexterity=dex, strength=strength, hostility=hostility)

        # Mimic starts disguised
        if enemy_type == EnemyType.MIMIC:
            enemy.is_disguised = True
            enemy.disguise_item_type = random.choice(["Food", "Scroll", "Elixir"])

        return enemy

    def _create_treasure(self, level_number: int) -> Item:
        value = random.randint(10 + level_number*5, 50 + level_number*10)
        return Item(item_type=ItemType.TREASURE, value=value)


class PathFinding:
    @staticmethod
    def find_path_to_player(enemy: Enemy, player: Character,
                            level: Level) -> List[Tuple[int,int]]:
        # Find the room this enemy belongs to
        enemy_room = None
        for room in level.rooms:
            if room.room_id == enemy.room_id:
                enemy_room = room
                break

        queue = deque([(enemy.x, enemy.y, [])])
        visited = {(enemy.x, enemy.y)}
        while queue:
            x, y, path = queue.popleft()
            if x == player.x and y == player.y:
                return path
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                nx, ny = x+dx, y+dy
                if (nx, ny) in visited:
                    continue
                # Stay within the enemy's room only
                if enemy_room and not enemy_room.is_walkable(nx, ny):
                    continue
                if not enemy_room and not level.is_walkable(nx, ny):
                    continue
                visited.add((nx, ny))
                queue.append((nx, ny, path+[(nx, ny)]))
        return []

    @staticmethod
    def get_distance(x1, y1, x2, y2) -> int:
        return abs(x1-x2) + abs(y1-y2)
