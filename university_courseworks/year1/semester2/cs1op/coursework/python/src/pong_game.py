"""
Pong physics, CPU AI and scoring without any widgets.

Translation of the game-logic half of ``PongMinigame.java``: the 800x600
logical pitch, paddle and ball geometry, per-difficulty AI tables, the
angle-from-offset reflection with hit cooldowns, point detection and
the first-to-N ending. The view in the same file's sibling class runs
``tick`` on a tkinter timer; tests drive ``tick`` directly.
"""

import random

import game_settings
import sound_manager
from game_settings import Difficulty


GW = 800
GH = 600
PW = 12
PH = 100
BS = 12
PADDLE_STEP = 8
BALL_BASE = 5
LEFT_X = 24
RIGHT_X = GW - 24 - PW

AI_SPEED = {Difficulty.EASY: 3, Difficulty.NORMAL: 5, Difficulty.HARD: 7}
AI_DEAD_ZONE = {Difficulty.EASY: 55, Difficulty.NORMAL: 18, Difficulty.HARD: 5}
AI_REACTION_DELAY = {Difficulty.EASY: 12, Difficulty.NORMAL: 6, Difficulty.HARD: 2}
AI_MISS_CHANCE = {Difficulty.EASY: 0.30, Difficulty.NORMAL: 0.07, Difficulty.HARD: 0.01}

RESET_PAUSE_MS = 750


def win_score_for_exp(exp):
    """
    First-to target from the player's EXP: 3 up to 200, 5 up to 350, else 7.
    """
    if exp <= 200:
        return 3
    if exp <= 350:
        return 5
    return 7


class PongState:
    """
    The whole Pong match: positions, scores and flow flags.
    """

    def __init__(self, player_name="PLAYER", exp=0, rng=None):
        self.rng = rng if rng is not None else random.Random()
        self.player_name = player_name
        self.win_score = win_score_for_exp(exp)
        self.left_y = GH // 2 - PH // 2
        self.right_y = GH // 2 - PH // 2
        self.ball_x = GW / 2.0
        self.ball_y = GH / 2.0
        self.vel_x = BALL_BASE
        self.vel_y = BALL_BASE
        self.left_score = 0
        self.right_score = 0
        self.keys = set()
        self.active = True
        self.paused = False
        self.game_ended = False
        self.player_won = False
        self.end_sound_played = False
        self.end_msg = ""
        self.player_hit_active = False
        self.cpu_hit_active = False
        self.ai_target_y = GH / 2.0
        self.ai_update_tick = 0
        self.resume_due = False

    def ai_speed(self):
        """
        CPU paddle speed for the current difficulty.
        """
        return AI_SPEED[game_settings.get_difficulty()]

    def ai_dead_zone(self):
        """
        CPU paddle dead zone for the current difficulty.
        """
        return AI_DEAD_ZONE[game_settings.get_difficulty()]

    def ai_reaction_delay(self):
        """
        CPU retarget delay in ticks for the current difficulty.
        """
        return AI_REACTION_DELAY[game_settings.get_difficulty()]

    def ai_miss_chance(self):
        """
        Probability the CPU aims at midfield instead of the ball.
        """
        return AI_MISS_CHANCE[game_settings.get_difficulty()]

    def tick(self):
        """
        Advance one frame: paddles, AI, ball and scoring.
        """
        if self.paused or self.game_ended:
            return
        self.move_player_paddle()
        self.move_ai()
        self.move_ball()
        self.check_score()

    def move_player_paddle(self):
        """
        Step the left paddle from the held up/down keys, clamped in play.
        """
        if "up" in self.keys:
            self.left_y = max(0, self.left_y - PADDLE_STEP)
        if "down" in self.keys:
            self.left_y = min(GH - PH, self.left_y + PADDLE_STEP)

    def move_ai(self):
        """
        Step the CPU paddle: manual override, tracking, or recentring.
        """
        if "i" in self.keys:
            self.right_y = max(0, self.right_y - PADDLE_STEP)
            return
        if "k" in self.keys:
            self.right_y = min(GH - PH, self.right_y + PADDLE_STEP)
            return
        if self.vel_x > 0:
            self.ai_update_tick += 1
            if self.ai_update_tick >= self.ai_reaction_delay():
                self.ai_update_tick = 0
                if self.rng.random() < self.ai_miss_chance():
                    self.ai_target_y = GH / 2.0
                else:
                    self.ai_target_y = self.ball_y + BS / 2.0
            mid = self.right_y + PH // 2
            target = int(self.ai_target_y)
            if target < mid - self.ai_dead_zone():
                self.right_y = max(0, self.right_y - self.ai_speed())
            elif target > mid + self.ai_dead_zone():
                self.right_y = min(GH - PH, self.right_y + self.ai_speed())
        else:
            centre = GH // 2 - PH // 2
            if self.right_y < centre:
                self.right_y = min(centre, self.right_y + 2)
            elif self.right_y > centre:
                self.right_y = max(centre, self.right_y - 2)

    def move_ball(self):
        """
        Fly the ball with wall bounces and cooldown-guarded paddle hits.
        """
        self.ball_x += self.vel_x
        self.ball_y += self.vel_y
        if self.ball_y <= 0:
            self.ball_y = 0
            self.vel_y = abs(self.vel_y)
        if self.ball_y >= GH - BS:
            self.ball_y = GH - BS
            self.vel_y = -abs(self.vel_y)
        touching_left = (
            self.vel_x < 0
            and self.ball_x <= LEFT_X + PW
            and self.ball_x >= LEFT_X - abs(self.vel_x)
            and self.ball_y + BS >= self.left_y
            and self.ball_y <= self.left_y + PH
        )
        if touching_left:
            if not self.player_hit_active:
                self.player_hit_active = True
                self.ball_x = LEFT_X + PW
                self.vel_x = -self.vel_x
                self.vel_y = ((self.ball_y + BS / 2.0) - (self.left_y + PH / 2.0)) / (PH / 2.0) * BALL_BASE * 1.5
                sound_manager.play_once(sound_manager.PONG_PLAYER_HIT)
        else:
            self.player_hit_active = False
        touching_right = (
            self.vel_x > 0
            and self.ball_x + BS >= RIGHT_X
            and self.ball_x + BS <= RIGHT_X + PW + abs(self.vel_x)
            and self.ball_y + BS >= self.right_y
            and self.ball_y <= self.right_y + PH
        )
        if touching_right:
            if not self.cpu_hit_active:
                self.cpu_hit_active = True
                self.ball_x = RIGHT_X - BS
                self.vel_x = -self.vel_x
                self.vel_y = ((self.ball_y + BS / 2.0) - (self.right_y + PH / 2.0)) / (PH / 2.0) * BALL_BASE * 1.5
                sound_manager.play_once(sound_manager.PONG_CPU_HIT)
        else:
            self.cpu_hit_active = False

    def check_score(self):
        """
        Award points past the goals and end the match at the target.
        """
        if self.ball_x < -BS:
            self.right_score += 1
            sound_manager.play_once(sound_manager.PONG_CPU_POINT)
            self.reset_ball(-1)
        elif self.ball_x > GW:
            self.left_score += 1
            sound_manager.play_once(sound_manager.PONG_PLAYER_POINT)
            self.reset_ball(1)
        if not self.game_ended and (self.left_score >= self.win_score or self.right_score >= self.win_score):
            self.active = False
            self.game_ended = True
            self.player_won = self.left_score >= self.win_score
            self.end_msg = self.player_name.upper() + " WINS!" if self.player_won else "CPU WINS!"
            if not self.end_sound_played:
                self.end_sound_played = True
                if self.player_won:
                    sound_manager.play_once(sound_manager.PONG_WIN)
                else:
                    sound_manager.play_loop(sound_manager.PONG_LOSE)

    def reset_ball(self, direction):
        """
        Serve from centre with a random angle and a brief pause.

        Sets ``resume_due`` so the view can schedule the unpause; tests
        call ``unpause`` directly.
        """
        self.ball_x = GW / 2.0
        self.ball_y = GH / 2.0
        self.vel_x = direction * BALL_BASE
        self.vel_y = (self.rng.random() - 0.5) * BALL_BASE
        self.ai_target_y = GH / 2.0
        self.player_hit_active = False
        self.cpu_hit_active = False
        self.paused = True
        self.resume_due = True

    def unpause(self):
        """
        End the serve pause.
        """
        self.paused = False
        self.resume_due = False


PONG_WIN_EXP = 50

