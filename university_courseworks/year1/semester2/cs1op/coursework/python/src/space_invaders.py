"""
Space Invaders waves, ballistics and collisions without any widgets.

Translation of the game-logic half of ``SpaceInvadersMinigame.java``:
the 800x600 field, three enemy types in rows of eight, wave-scaled
speed and shooting per difficulty, the saucer march with edge drops,
bullet-versus-ship collision boxes, three mini-lives with wave respawn,
and the wave-clear / victory / defeat endings. The view runs ``tick``
on a tkinter timer; tests drive ``tick`` directly.
"""

import random

import game_settings
import sound_manager
from game_settings import Difficulty


GW = 800
GH = 600
PW = 34
PH = 26
ES = 32
PBW = 4
PBH = 14
EBW = 5
EBH = 10
PLAYER_SPEED = 8
P_BULLET_SPEED = 13
E_BULLET_SPEED = 5
SHOOT_COOLDOWN_MS = 180
PLAYER_Y = GH - 60
ANIM_TICKS = 22
ENEMY_DROP = 18
HIT_MESSAGE_TICKS = 160

WAVES_FOR_EXP = ((200, 5), (350, 10), (float("inf"), 15))
SI_WIN_EXP = 100


class EnemyType:
    """
    The three enemy kinds.
    """

    UFO = "UFO"
    SPACECRAFT = "SPACECRAFT"
    ALIEN = "ALIEN"


class Enemy:
    """
    One invader at floating-point coordinates.
    """

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind


class PlayerBullet:
    """
    One upward player shot.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class EnemyBullet:
    """
    One downward enemy shot.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


def total_waves_for_exp(exp):
    """
    Wave count from the player's EXP: 5 up to 200, 10 up to 350, else 15.
    """
    for limit, waves in WAVES_FOR_EXP:
        if exp <= limit:
            return waves
    return 15


def wave_speed(wave, difficulty=None):
    """
    Saucer speed for a wave and difficulty, cycling every five waves.
    """
    level = difficulty if difficulty is not None else game_settings.get_difficulty()
    step = (wave - 1) % 5
    if level == Difficulty.EASY:
        return 0.0 + step * 0.4
    if level == Difficulty.HARD:
        return 2.0 + step * 0.5
    return 1.0 + step * 0.5


def wave_shoot_chance(wave, difficulty=None):
    """
    Per-enemy per-tick shot probability for a wave and difficulty.
    """
    level = difficulty if difficulty is not None else game_settings.get_difficulty()
    step = (wave - 1) % 5
    if level == Difficulty.EASY:
        return 0.0
    if level == Difficulty.HARD:
        return 0.002 + step * 0.0004
    return 0.0008 + step * 0.00016


class InvadersState:
    """
    The whole invasion: ship, saucers, bullets, waves and endings.
    """

    def __init__(self, exp=0, rng=None):
        self.rng = rng if rng is not None else random.Random()
        self._now = 0
        self.player_x = GW // 2 - PW // 2
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemy_dir = 1
        self.current_speed = 1.0
        self.current_shoot_chance = 0.0
        self.anim_tick = 0
        self.anim_frame = 0
        self.current_wave = 1
        self.total_waves = total_waves_for_exp(exp)
        self.mini_lives = 3
        self.hit_msg = ""
        self.hit_timer = 0
        self.game_active = True
        self.game_ended = False
        self.player_won = False
        self.end_sound_played = False
        self.game_paused = False
        self.show_msg = True
        self.msg_text = "Press ENTER to start Wave 1 / " + str(self.total_waves)
        self.end_msg = ""
        self.move_left = False
        self.move_right = False
        self.do_shoot = False
        self.last_shoot_ms = -SHOOT_COOLDOWN_MS - 1
        self.ufo_row_present = False
        self.alien_row_present = False

    def advance_clock(self, milliseconds):
        """
        Move the test clock forward, used for the shoot cooldown.
        """
        self._now += milliseconds

    def start_wave_loop(self):
        """
        Open the current wave and dismiss the message overlay.
        """
        self.spawn_wave()
        self.show_msg = False

    def spawn_wave(self):
        """
        Lay out this wave's rows: UFOs always, craft from 6, aliens from 11.
        """
        self.enemies = []
        self.enemy_bullets = []
        self.player_bullets = []
        self.anim_tick = 0
        self.anim_frame = 0
        self.current_speed = wave_speed(self.current_wave)
        self.current_shoot_chance = wave_shoot_chance(self.current_wave)
        self.enemy_dir = 1
        columns = 8
        spacing = GW // (columns + 1)
        self._spawn_row(EnemyType.UFO, columns, spacing, 0)
        if self.current_wave >= 6:
            self._spawn_row(EnemyType.SPACECRAFT, columns, spacing, 1)
        if self.current_wave >= 11:
            self._spawn_row(EnemyType.ALIEN, columns, spacing, 2)
        self.update_loop_sounds()

    def _spawn_row(self, kind, columns, spacing, row_idx):
        for column in range(columns):
            self.enemies.append(Enemy((column + 1) * spacing - ES / 2.0, 45 + row_idx * 54, kind))

    def update_loop_sounds(self):
        """
        Start or stop the UFO and alien loop sounds with row presence.
        """
        has_ufo = any(e.kind == EnemyType.UFO for e in self.enemies)
        has_alien = any(e.kind == EnemyType.ALIEN for e in self.enemies)
        if has_ufo and not self.ufo_row_present:
            sound_manager.play_loop(sound_manager.SI_UFO_FLY)
        elif not has_ufo and self.ufo_row_present:
            sound_manager.stop_sound(sound_manager.SI_UFO_FLY)
        if has_alien and not self.alien_row_present:
            sound_manager.play_loop(sound_manager.SI_ALIEN_SHOOT)
        elif not has_alien and self.alien_row_present:
            sound_manager.stop_sound(sound_manager.SI_ALIEN_SHOOT)
        self.ufo_row_present = has_ufo
        self.alien_row_present = has_alien

    def tick(self):
        """
        Advance one frame: animation, ship, shots, saucers and endings.
        """
        if self.game_paused or self.game_ended or self.show_msg:
            return
        ufo_shot = False
        craft_shot = False
        alien_shot = False
        self.anim_tick += 1
        if self.anim_tick >= ANIM_TICKS:
            self.anim_tick = 0
            self.anim_frame = 1 - self.anim_frame
        if self.move_left and self.player_x > 0:
            self.player_x -= PLAYER_SPEED
        if self.move_right and self.player_x < GW - PW:
            self.player_x += PLAYER_SPEED
        if self.do_shoot and self._now - self.last_shoot_ms > SHOOT_COOLDOWN_MS:
            self.player_bullets.append(PlayerBullet(self.player_x + PW / 2.0 - PBW / 2.0, PLAYER_Y - PBH))
            self.last_shoot_ms = self._now
            sound_manager.play_once(sound_manager.SI_PLAYER_SHOOT)
        self.player_bullets = [b for b in self._fly_player_shots() if b.y >= 0]
        drop = False
        for enemy in self.enemies:
            enemy.x += self.current_speed * self.enemy_dir
            if enemy.x <= 0 or enemy.x + ES >= GW:
                drop = True
        if drop:
            self.enemy_dir = -self.enemy_dir
            for enemy in self.enemies:
                enemy.y += ENEMY_DROP
                enemy.x += self.current_speed * self.enemy_dir
                if enemy.y + ES >= PLAYER_Y:
                    self.trigger_game_over()
                    return
        if self.current_shoot_chance > 0 and self.enemies:
            for enemy in self.enemies:
                if self.rng.random() < self.current_shoot_chance:
                    self.enemy_bullets.append(EnemyBullet(enemy.x + ES / 2.0 - EBW / 2.0, enemy.y + ES))
                    if enemy.kind == EnemyType.UFO and not ufo_shot:
                        sound_manager.play_once(sound_manager.SI_UFO_SHOOT)
                        ufo_shot = True
                    elif enemy.kind == EnemyType.SPACECRAFT and not craft_shot:
                        sound_manager.play_once(sound_manager.SI_SPACECRAFT_SHOOT)
                        craft_shot = True
                    elif enemy.kind == EnemyType.ALIEN and not alien_shot:
                        sound_manager.play_once(sound_manager.SI_ALIEN_SHOOT)
                        alien_shot = True
        for bullet in list(self.enemy_bullets):
            bullet.y += E_BULLET_SPEED
            if bullet.y > GH:
                self.enemy_bullets.remove(bullet)
                continue
            if (bullet.x < self.player_x + PW and bullet.x + EBW > self.player_x
                    and bullet.y < PLAYER_Y + PH and bullet.y + EBH > PLAYER_Y):
                self.enemy_bullets.remove(bullet)
                self.on_player_hit()
                return
        for bullet in list(self.player_bullets):
            for enemy in list(self.enemies):
                if (bullet.x < enemy.x + ES and bullet.x + PBW > enemy.x
                        and bullet.y < enemy.y + ES and bullet.y + PBH > enemy.y):
                    self.player_bullets.remove(bullet)
                    if enemy.kind == EnemyType.UFO:
                        sound_manager.play_once(sound_manager.SI_UFO_DIE)
                    elif enemy.kind == EnemyType.SPACECRAFT:
                        sound_manager.play_once(sound_manager.SI_SPACECRAFT_DIE)
                    else:
                        sound_manager.play_once(sound_manager.SI_ALIEN_DIE)
                    self.enemies.remove(enemy)
                    self.update_loop_sounds()
                    break
        if not self.enemies:
            self.stop_all_enemy_loops()
            if self.current_wave >= self.total_waves:
                if not self.end_sound_played:
                    self.end_sound_played = True
                    self.game_ended = True
                    self.player_won = True
                    self.end_msg = "MISSION COMPLETE!"
                    sound_manager.play_once(sound_manager.SI_WIN)
            else:
                sound_manager.play_once(sound_manager.SI_NEXT_WAVE)
                self.current_wave += 1
                self.show_msg = True
                self.msg_text = ("Wave " + str(self.current_wave - 1) + " cleared!\nPress ENTER for Wave "
                                 + str(self.current_wave) + " / " + str(self.total_waves)
                                 + "   Speed: " + ("%.1f" % wave_speed(self.current_wave)))
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def _fly_player_shots(self):
        for bullet in self.player_bullets:
            bullet.y -= P_BULLET_SPEED
            yield bullet

    def on_player_hit(self):
        """
        Lose a mini-life: respawn the wave, or end defeated at zero.
        """
        self.mini_lives -= 1
        sound_manager.play_once(sound_manager.SI_MINI_LIFE_LOST)
        if self.mini_lives <= 0:
            self.stop_all_enemy_loops()
            if not self.end_sound_played:
                self.end_sound_played = True
                self.game_ended = True
                self.player_won = False
                self.end_msg = "OUT OF MINIGAME LIVES!"
                sound_manager.play_loop(sound_manager.SI_LOSE)
        else:
            self.hit_msg = ("HIT \u2013 " + str(self.mini_lives) + " minigame "
                            + ("life" if self.mini_lives == 1 else "lives") + " remaining")
            self.hit_timer = HIT_MESSAGE_TICKS
            self.enemy_bullets = []
            self.player_bullets = []
            self.spawn_wave()

    def trigger_game_over(self):
        """
        End defeated when the saucers reach the ship line.
        """
        self.stop_all_enemy_loops()
        if not self.end_sound_played:
            self.end_sound_played = True
            self.game_ended = True
            self.player_won = False
            self.end_msg = "WAVE " + str(self.current_wave) + " FAILED"
            sound_manager.play_loop(sound_manager.SI_LOSE)

    def stop_all_enemy_loops(self):
        """
        Silence both saucer loops and forget row presence.
        """
        sound_manager.stop_sound(sound_manager.SI_UFO_FLY)
        sound_manager.stop_sound(sound_manager.SI_ALIEN_SHOOT)
        self.ufo_row_present = False
        self.alien_row_present = False

