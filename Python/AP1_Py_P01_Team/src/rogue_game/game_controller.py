import random, sys, os, time, math

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from rogue_game.domain.entities import GameSession, Enemy, Room, Item, Door
from rogue_game.domain.enums   import GameState, ItemType, ItemSubtype, KeyColor, EnemyType
from rogue_game.domain.game_logic import CombatSystem
from rogue_game.domain.level_generation import LevelGenerator, PathFinding
from rogue_game.presentation.renderer import (GameRenderer, Renderer3D,
                                               MenuRenderer, InventoryRenderer,
                                               LeaderboardRenderer)
from rogue_game.presentation.input import InputManager, DialogManager
from rogue_game.data_layer.save_manager import SaveManager


class GameController:
    TURN_SPEED_3D  = math.pi / 8   # radians per key press (turn left/right)
    MOVE_STEP_3D   = 0.5           # tiles per step in 3D

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.game_state = GameState.MENU
        self.session = None
        self.running = True

        self.renderer       = GameRenderer(stdscr)
        self.renderer_3d    = Renderer3D(stdscr)
        self.menu_renderer  = MenuRenderer(stdscr)
        self.inv_renderer   = InventoryRenderer(stdscr)
        self.lb_renderer    = LeaderboardRenderer(stdscr)
        self.input_manager  = InputManager(stdscr)
        self.dialog_manager = DialogManager(stdscr)
        self.save_manager   = SaveManager()

        self.turn_count = 0

    # Main loop
    def run(self):
        frame_time = 1.0 / 60.0
        try:
            while self.running:
                t0 = time.time()
                try:
                    if self.game_state == GameState.MENU:
                        self._handle_menu()
                    elif self.game_state == GameState.PLAYING:
                        self._handle_game()
                    elif self.game_state == GameState.PLAYING_3D:
                        self._handle_game_3d()
                    elif self.game_state == GameState.GAME_OVER:
                        self._handle_game_over()
                    elif self.game_state == GameState.INVENTORY:
                        self._handle_inventory()
                except Exception as e:
                    import traceback; traceback.print_exc(file=sys.stderr)
                elapsed = time.time() - t0
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)
        except KeyboardInterrupt:
            self.running = False

    # Menu
    def _handle_menu(self):
        choice = self.menu_renderer.render_main_menu()
        if   choice == '1': self._new_game()
        elif choice == '2': self._load_game()
        elif choice == '3': self._show_leaderboard()
        elif choice == '4': self.running = False

    def _new_game(self):
        self.session = GameSession()
        self.session.seed = random.randint(1, 1_000_000)
        self._load_level(1)
        self.input_manager.stdscr.nodelay(True)
        self.input_manager.stdscr.keypad(True)
        self.game_state = GameState.PLAYING

    def _load_game(self):
        self.session = self.save_manager.load_game()
        if self.session:
            self._load_level(self.session.current_level_number)
            self.game_state = GameState.PLAYING
        else:
            self.dialog_manager.show_message("Info", "No saved game found!")
            self.game_state = GameState.MENU

    def _show_leaderboard(self):
        self.lb_renderer.show_leaderboard(self.save_manager.get_leaderboard())
        self.game_state = GameState.MENU

    # Level loading
    def _load_level(self, level_number: int):
        level_seed = (self.session.seed * level_number) % (2**31 - 1)
        generator  = LevelGenerator(seed=level_seed)
        modifier   = self.session.difficulty.difficulty_modifier

        if level_number not in self.session.levels:
            self.session.current_level = generator.generate_level(
                level_number, difficulty_modifier=modifier)
            self.session.levels[level_number] = self.session.current_level
        else:
            self.session.current_level = self.session.levels[level_number]

        start_room = self.session.current_level.get_room(
            self.session.current_level.starting_room_id)
        if start_room:
            self.session.character.x = start_room.x + start_room.width  // 2
            self.session.character.y = start_room.y + start_room.height // 2
        self.session.character.sync_view_pos()

    # 2D game loop
    def _handle_game(self):
        self.renderer.render(self.session)
        key = self.input_manager.get_key()
        if key is not None:
            self._handle_player_action_2d(key)
            if self.session.is_running():
                self._process_enemy_turns()
        self._check_win_lose()
        self._update_effects()

    def _handle_player_action_2d(self, key: int):
        if key < 0 or key >= 256:
            return
        try:
            char = chr(key)
        except (ValueError, OverflowError):
            return

        if   char.lower() == 'w': self._try_move(0, -1)
        elif char.lower() == 's': self._try_move(0,  1)
        elif char.lower() == 'a': self._try_move(-1, 0)
        elif char.lower() == 'd': self._try_move(1,  0)
        elif char.lower() == 'h': self._use_weapon()
        elif char.lower() == 'j': self._use_food()
        elif char.lower() == 'k': self._use_elixir()
        elif char.lower() == 'e': self._use_scroll()
        elif char.lower() == 'i': self.game_state = GameState.INVENTORY
        elif key == 9:             # TAB → switch to 3D
            self.session.character.sync_view_pos()
            self.game_state = GameState.PLAYING_3D
        elif key == 27:            # ESC
            self.save_manager.save_game(self.session)
            self.game_state = GameState.MENU
        elif char.lower() == 'q': self.running = False

    # 3D game loop
    def _handle_game_3d(self):
        self.renderer_3d.render(self.session)
        key = self.input_manager.get_key()
        if key is not None:
            self._handle_player_action_3d(key)
            if self.session.is_running():
                self._process_enemy_turns()
        self._check_win_lose()
        self._update_effects()

    def _handle_player_action_3d(self, key: int):
        if key < 0 or key >= 256:
            return
        try:
            ch = chr(key)
        except (ValueError, OverflowError):
            return

        player = self.session.character

        if ch.lower() == 'a':    # turn left
            player.view_angle -= self.TURN_SPEED_3D
            player.view_angle %= 2 * math.pi

        elif ch.lower() == 'd':  # turn right
            player.view_angle += self.TURN_SPEED_3D
            player.view_angle %= 2 * math.pi

        elif ch.lower() == 'w':  # move forward
            self._try_move_3d(math.cos(player.view_angle),
                               math.sin(player.view_angle))

        elif ch.lower() == 's':  # move backward
            self._try_move_3d(-math.cos(player.view_angle),
                               -math.sin(player.view_angle))

        elif ch.lower() == 'h': self._use_weapon()
        elif ch.lower() == 'j': self._use_food()
        elif ch.lower() == 'k': self._use_elixir()
        elif ch.lower() == 'e': self._use_scroll()
        elif key == 9:           # TAB → back to 2D
            self.game_state = GameState.PLAYING
        elif key == 27:
            self.save_manager.save_game(self.session)
            self.game_state = GameState.MENU

    def _try_move_3d(self, ddx: float, ddy: float):
        """Move in 3D world (float steps). Sync tile position after."""
        player = self.session.character
        level  = self.session.current_level
        new_vx = player.view_x + ddx * self.MOVE_STEP_3D
        new_vy = player.view_y + ddy * self.MOVE_STEP_3D
        tile_x = int(new_vx)
        tile_y = int(new_vy)
        if level.is_walkable(tile_x, tile_y):
            player.view_x = new_vx
            player.view_y = new_vy
            player.x = tile_x
            player.y = tile_y
            self.session.statistics.tiles_traversed += 1
            self._check_item_pickup()
            self._check_enemy_encounter()

    # 2D movement
    def _try_move(self, dx: int, dy: int):
        char  = self.session.character
        level = self.session.current_level
        nx    = char.x + dx
        ny    = char.y + dy

        # Check for locked door
        door = level.get_door_at(nx, ny)
        if door is not None and not door.is_passable():
            if char.backpack.has_key(door.color):
                char.backpack.consume_key(door.color)
                door.state = door.__class__.__mro__[0].__mro__[0]  # will fix below
                # Open the door
                from rogue_game.domain.enums import DoorState
                door.state = DoorState.OPEN
                return   # don't move, just open
            else:
                color_name = door.color.name
                self.dialog_manager.show_message(
                    "Locked Door",
                    f"This door needs a {color_name} key!")
                return

        if not level.is_walkable(nx, ny):
            return

        char.x = nx
        char.y = ny
        char.sync_view_pos()
        self.session.statistics.tiles_traversed += 1
        self.session.difficulty.turns_this_level += 1
        self._check_item_pickup()
        self._check_enemy_encounter()

    # Item pickup
    def _check_item_pickup(self):
        char     = self.session.character
        location = self.session.current_level.get_location(char.x, char.y)
        if not isinstance(location, Room):
            return
        to_remove = []
        for item in location.items:
            if item.x == char.x and item.y == char.y:
                if char.backpack.add_item(item):
                    to_remove.append(item)
                    if item.item_type == ItemType.TREASURE:
                        self.session.statistics.treasure_collected += item.value
        for item in to_remove:
            location.items.remove(item)

    # Enemy encounter
    def _check_enemy_encounter(self):
        char     = self.session.character
        location = self.session.current_level.get_location(char.x, char.y)
        if not isinstance(location, Room):
            return
        for enemy in location.enemies:
            if enemy.x == char.x and enemy.y == char.y and enemy.is_alive():
                self._combat_with_enemy(enemy)
                break

    def _combat_with_enemy(self, enemy: Enemy):
        char = self.session.character
        # Mimic reveal – skip combat this turn
        if enemy.enemy_type == EnemyType.MIMIC and enemy.is_disguised:
            enemy.is_disguised = False
            return

        while enemy.is_alive() and char.is_alive():
            hit, dmg = CombatSystem.player_attacks_enemy(char, enemy)
            self.session.statistics.attacks_made += 1
            if not enemy.is_alive():
                treasure = CombatSystem.calculate_treasure_reward(enemy)
                self.session.statistics.treasure_collected += treasure
                self.session.statistics.enemies_defeated   += 1
                self.session.difficulty.kills_this_level   += 1
                location = self.session.current_level.get_location(char.x, char.y)
                if isinstance(location, Room) and enemy in location.enemies:
                    location.enemies.remove(enemy)
                break
            hit, dmg = CombatSystem.enemy_attacks_player(enemy, char)
            if hit:
                self.session.statistics.hits_taken             += 1
                self.session.difficulty.damage_taken_this_level += dmg
            if not char.is_alive():
                break

    # Item use
    def _use_weapon(self):
        weapons = []
        for st in [ItemSubtype.SWORD, ItemSubtype.AXE,
                   ItemSubtype.BOW,   ItemSubtype.STAFF]:
            weapons.extend(self.session.character.backpack.get_items_of_type(st))
        if not weapons:
            self.dialog_manager.show_message("Inventory", "No weapons!")
            return
        weapons.append("Unarmed (0)")
        choice = self.dialog_manager.select_item(weapons, "Select Weapon")
        if choice is not None:
            if choice < len(weapons) - 1:
                self.session.character.current_weapon = weapons[choice]
            else:
                self.session.character.current_weapon = None

    def _use_food(self):
        foods = [item for items in self.session.character.backpack.items.values()
                 for item in items if item.item_type == ItemType.FOOD]
        if not foods:
            self.dialog_manager.show_message("Inventory", "No food!"); return
        choice = self.dialog_manager.select_item(foods, "Select Food")
        if choice is not None:
            food = foods[choice]
            self.session.character.heal(food.health_value)
            self.session.statistics.food_consumed += 1
            self.session.difficulty.items_used_this_level += 1
            for items in self.session.character.backpack.items.values():
                if food in items:
                    items.remove(food); break

    def _use_elixir(self):
        elixirs = [item for items in self.session.character.backpack.items.values()
                   for item in items if item.item_type == ItemType.ELIXIR]
        if not elixirs:
            self.dialog_manager.show_message("Inventory", "No elixirs!"); return
        choice = self.dialog_manager.select_item(elixirs, "Select Elixir")
        if choice is not None:
            el = elixirs[choice]
            bonus = el.dexterity_bonus or el.strength_bonus or el.max_health_bonus
            self.session.character.active_elixirs[el.subtype] = (10, bonus)
            if el.subtype == ItemSubtype.HEALTH:
                self.session.character.increase_max_health(bonus)
            self.session.statistics.elixirs_used += 1
            self.session.difficulty.items_used_this_level += 1
            for items in self.session.character.backpack.items.values():
                if el in items:
                    items.remove(el); break

    def _use_scroll(self):
        scrolls = [item for items in self.session.character.backpack.items.values()
                   for item in items if item.item_type == ItemType.SCROLL]
        if not scrolls:
            self.dialog_manager.show_message("Inventory", "No scrolls!"); return
        choice = self.dialog_manager.select_item(scrolls, "Select Scroll")
        if choice is not None:
            sc = scrolls[choice]
            if sc.max_health_bonus:
                self.session.character.increase_max_health(sc.max_health_bonus)
            elif sc.dexterity_bonus:
                self.session.character.dexterity += sc.dexterity_bonus
            elif sc.strength_bonus:
                self.session.character.strength += sc.strength_bonus
            self.session.statistics.scrolls_read += 1
            self.session.difficulty.items_used_this_level += 1
            for items in self.session.character.backpack.items.values():
                if sc in items:
                    items.remove(sc); break

    # Inventory screen
    def _handle_inventory(self):
        self.inv_renderer.show_inventory(self.session.character)
        self.game_state = GameState.PLAYING

    # Enemy AI turns
    def _process_enemy_turns(self):
        char  = self.session.character
        level = self.session.current_level

        for room in level.rooms:
            for enemy in list(room.enemies):
                if not enemy.is_alive():
                    continue

                # Mimic: only reveals / chases if player is very close
                if enemy.enemy_type == EnemyType.MIMIC and enemy.is_disguised:
                    if PathFinding.get_distance(enemy.x, enemy.y, char.x, char.y) <= 2:
                        enemy.is_disguised = False
                    continue

                # Find the room this enemy belongs to (for random movement)
                enemy_room = next((r for r in level.rooms if r.room_id == enemy.room_id), None)

                dist = PathFinding.get_distance(enemy.x, enemy.y, char.x, char.y)
                if dist <= enemy.hostility:
                    enemy.is_chasing = True

                if enemy.is_chasing:
                    path = PathFinding.find_path_to_player(
                        enemy, char, level)
                    if path:
                        nx, ny = path[0]
                        if nx == char.x and ny == char.y:
                            # Enemy reached player – attack
                            hit, dmg = CombatSystem.enemy_attacks_player(enemy, char)
                            if hit:
                                self.session.statistics.hits_taken             += 1
                                self.session.difficulty.damage_taken_this_level += dmg
                        else:
                            enemy.x, enemy.y = nx, ny
                else:
                    # Random movement within own room only
                    if enemy_room is not None:
                        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                        random.shuffle(dirs)
                        for dx, dy in dirs:
                            nx, ny = enemy.x + dx, enemy.y + dy
                            if enemy_room.is_walkable(nx, ny):
                                enemy.x, enemy.y = nx, ny
                                break

    # Effects / win-lose
    def _update_effects(self):
        char = self.session.character
        to_remove = []
        for subtype, (duration, bonus) in list(char.active_elixirs.items()):
            duration -= 1
            if duration <= 0:
                to_remove.append(subtype)
            else:
                char.active_elixirs[subtype] = (duration, bonus)
        for st in to_remove:
            del char.active_elixirs[st]
            if char.health < 1:
                char.health = 1

    def _check_win_lose(self):
        if not self.session.is_running():
            self.game_state = GameState.GAME_OVER
        elif self._player_at_exit():
            self._advance_level()

    def _player_at_exit(self) -> bool:
        exit_room = self.session.current_level.get_room(
            self.session.current_level.exit_room_id)
        if exit_room:
            ex = exit_room.x + exit_room.width  // 2
            ey = exit_room.y + exit_room.height // 2
            return (self.session.character.x == ex and
                    self.session.character.y == ey)
        return False

    def _advance_level(self):
        # Bonus Task 7: update dynamic difficulty before moving on
        self.session.difficulty.update_modifier(self.session.current_level_number)
        self.session.difficulty.reset_for_new_level()

        self.session.advance_to_next_level()
        self.save_manager.save_game(self.session)

        if self.session.has_completed_all_levels():
            self.game_state = GameState.GAME_OVER
        else:
            self._load_level(self.session.current_level_number)

    def _handle_game_over(self):
        self.save_manager.save_highscore(self.session)
        self.menu_renderer.render_game_over(self.session)
        self.session = None
        self.game_state = GameState.MENU
