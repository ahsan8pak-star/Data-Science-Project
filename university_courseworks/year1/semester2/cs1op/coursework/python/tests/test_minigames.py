"""
Pong and Space Invaders match logic, driven tick by tick.

Both states run without widgets: seeded doubles remove randomness,
and sounds stay silent, so collisions, scoring, waves and endings are
pinned exactly as the Java computes them.
"""

import random

import pytest

import game_settings
import sound_manager
from game_settings import Difficulty
from pong_game import (
    BALL_BASE,
    BS,
    GH,
    GW,
    LEFT_X,
    PH,
    PONG_WIN_EXP,
    PW,
    RIGHT_X,
    PongState,
    win_score_for_exp,
)
from space_invaders import (
    EBH,
    EBW,
    ES,
    GH as SI_GH,
    GW as SI_GW,
    PBH,
    PBW,
    PLAYER_Y,
    PW as SI_PW,
    EnemyBullet,
    EnemyType,
    InvadersState,
    PlayerBullet,
    total_waves_for_exp,
    wave_shoot_chance,
    wave_speed,
)


def test_pong_win_exp_reward_is_fifty():
    assert PONG_WIN_EXP == 50


def test_win_score_table():
    assert win_score_for_exp(0) == 3
    assert win_score_for_exp(200) == 3
    assert win_score_for_exp(201) == 5
    assert win_score_for_exp(350) == 5
    assert win_score_for_exp(351) == 7


def test_pong_constructor_scales_target_to_exp():
    assert PongState("P", 0).win_score == 3
    assert PongState("P", 300).win_score == 5
    assert PongState("P", 400).win_score == 7


def test_pong_paddle_clamps_in_play():
    state = PongState()
    state.left_y = 0
    state.keys = {"up"}
    state.move_player_paddle()
    assert state.left_y == 0
    state.left_y = GH - PH
    state.keys = {"down"}
    state.move_player_paddle()
    assert state.left_y == GH - PH


def test_pong_ball_bounces_off_walls():
    state = PongState()
    state.ball_y = 1
    state.vel_y = -5
    state.move_ball()
    assert state.ball_y == 0
    assert state.vel_y == 5
    state.ball_y = GH - BS - 1
    state.vel_y = 5
    state.move_ball()
    assert state.ball_y == GH - BS
    assert state.vel_y == -5


def test_pong_left_paddle_reflects_with_angle():
    state = PongState()
    state.left_y = 250
    state.ball_x = LEFT_X + PW
    state.ball_y = 250 + PH / 2 - BS / 2
    state.vel_x = -BALL_BASE
    state.vel_y = 0.0
    state.move_ball()
    assert state.vel_x == BALL_BASE
    assert state.ball_x == LEFT_X + PW
    assert state.vel_y == 0.0


def test_pong_off_centre_hit_angles_away():
    state = PongState()
    state.left_y = 250
    state.ball_x = LEFT_X + PW
    state.ball_y = 250
    state.vel_x = -BALL_BASE
    state.move_ball()
    assert state.vel_x == BALL_BASE
    assert state.vel_y < 0


def test_pong_hit_cooldown_fires_once_per_contact():
    backend = sound_manager.get_backend()
    state = PongState()
    state.left_y = 250
    state.ball_x = LEFT_X + PW
    state.ball_y = 250 + PH / 2 - BS / 2
    state.vel_x = -BALL_BASE
    backend.played.clear()
    state.move_ball()
    first = len(backend.played)
    state.ball_x = LEFT_X + PW
    state.vel_x = -BALL_BASE
    state.move_ball()
    assert len(backend.played) == first


def test_pong_scores_and_serves_with_pause():
    state = PongState(rng=random.Random(5))
    state.ball_x = -BS - 1
    state.vel_x = -BALL_BASE
    state.check_score()
    assert state.right_score == 1
    assert state.ball_x == GW / 2.0
    assert state.paused
    assert state.resume_due
    state.unpause()
    assert not state.paused


def test_pong_first_to_target_ends_match():
    state = PongState()
    state.win_score = 2
    state.left_score = 1
    state.ball_x = GW + 1
    state.vel_x = BALL_BASE
    state.check_score()
    assert state.game_ended
    assert state.player_won
    assert state.end_msg == "PLAYER WINS!"
    assert not state.active


def test_pong_cpu_win_message():
    state = PongState()
    state.win_score = 1
    state.ball_x = -BS - 1
    state.check_score()
    assert state.game_ended
    assert not state.player_won
    assert state.end_msg == "CPU WINS!"


def test_pong_ai_reacts_tracks_and_recentres():
    game_settings.set_difficulty(Difficulty.HARD)
    state = PongState(rng=random.Random(0))
    state.vel_x = BALL_BASE
    state.ball_y = 500
    state.right_y = 0
    for _ in range(30):
        state.move_ai()
    assert state.right_y > 0
    state.vel_x = -BALL_BASE
    state.right_y = 0
    for _ in range(200):
        state.move_ai()
    assert state.right_y == GH // 2 - PH // 2


def test_pong_ai_manual_override():
    state = PongState()
    state.right_y = 300
    state.keys = {"i"}
    state.move_ai()
    assert state.right_y == 300 - 8
    state.keys = {"k"}
    state.move_ai()
    assert state.right_y == 300


def test_pong_ai_tables_by_difficulty():
    state = PongState()
    game_settings.set_difficulty(Difficulty.EASY)
    assert (state.ai_speed(), state.ai_dead_zone(), state.ai_reaction_delay()) == (3, 55, 12)
    assert state.ai_miss_chance() == 0.30
    game_settings.set_difficulty(Difficulty.NORMAL)
    assert (state.ai_speed(), state.ai_dead_zone(), state.ai_reaction_delay()) == (5, 18, 6)
    game_settings.set_difficulty(Difficulty.HARD)
    assert (state.ai_speed(), state.ai_dead_zone(), state.ai_reaction_delay()) == (7, 5, 2)
    assert state.ai_miss_chance() == 0.01


def test_pong_tick_freezes_when_paused_or_ended():
    state = PongState()
    state.paused = True
    before = (state.ball_x, state.ball_y)
    state.tick()
    assert (state.ball_x, state.ball_y) == before
    state.paused = False
    state.game_ended = True
    state.tick()
    assert (state.ball_x, state.ball_y) == before


def test_invaders_waves_table():
    assert total_waves_for_exp(0) == 5
    assert total_waves_for_exp(200) == 5
    assert total_waves_for_exp(201) == 10
    assert total_waves_for_exp(350) == 10
    assert total_waves_for_exp(351) == 15


def test_invaders_speed_and_shoot_formulas():
    assert wave_speed(1, Difficulty.EASY) == 0.0
    assert wave_speed(5, Difficulty.EASY) == 1.6
    assert wave_speed(1, Difficulty.NORMAL) == 1.0
    assert wave_speed(3, Difficulty.NORMAL) == 2.0
    assert wave_speed(1, Difficulty.HARD) == 2.0
    assert wave_speed(6, Difficulty.HARD) == 2.0
    assert wave_shoot_chance(1, Difficulty.EASY) == 0.0
    assert wave_shoot_chance(1, Difficulty.NORMAL) == 0.0008
    assert wave_shoot_chance(5, Difficulty.NORMAL) == pytest.approx(0.0008 + 4 * 0.00016)
    assert wave_shoot_chance(2, Difficulty.HARD) == pytest.approx(0.0024)


def test_invaders_spawn_rows_by_wave():
    state = InvadersState()
    state.current_wave = 1
    state.spawn_wave()
    assert len(state.enemies) == 8
    assert {e.kind for e in state.enemies} == {EnemyType.UFO}
    state.current_wave = 6
    state.spawn_wave()
    assert len(state.enemies) == 16
    state.current_wave = 11
    state.spawn_wave()
    assert len(state.enemies) == 24
    first = state.enemies[0]
    assert first.y == 45
    assert state.enemies[8].y == 45 + 54


def test_invaders_ship_moves_and_clamps():
    state = InvadersState()
    state.show_msg = False
    state.move_left = True
    state.player_x = 4
    state.tick()
    assert state.player_x == 4 - 8 or state.player_x >= 0
    state.player_x = 0
    state.tick()
    assert state.player_x == 0
    state.move_left = False
    state.move_right = True
    state.player_x = SI_GW - SI_PW
    state.tick()
    assert state.player_x == SI_GW - SI_PW


def test_invaders_shoot_cooldown_and_flight():
    state = InvadersState()
    state.show_msg = False
    state.spawn_wave()
    state.do_shoot = True
    state.tick()
    assert len(state.player_bullets) == 1
    first_y = state.player_bullets[0].y
    state.tick()
    assert len(state.player_bullets) == 1
    assert state.player_bullets[0].y < first_y
    state.advance_clock(200)
    state.tick()
    assert len(state.player_bullets) == 2


def test_invaders_player_shot_kills_enemy():
    state = InvadersState()
    state.show_msg = False
    state.spawn_wave()
    target = state.enemies[0]
    state.player_bullets = [PlayerBullet(target.x + 1, target.y + 1)]
    count = len(state.enemies)
    state.tick()
    assert len(state.enemies) == count - 1
    assert not state.player_bullets


def test_invaders_enemy_shot_costs_mini_life_and_respawns():
    state = InvadersState()
    state.show_msg = False
    state.spawn_wave()
    state.enemy_bullets = [EnemyBullet(state.player_x + 1, PLAYER_Y + 1)]
    state.tick()
    assert state.mini_lives == 2
    assert state.hit_timer == 160
    state.tick()
    assert state.hit_timer == 159
    assert state.hit_msg.startswith("HIT \u2013 2 minigame lives")


def test_invaders_third_hit_ends_defeated():
    state = InvadersState()
    state.show_msg = False
    state.spawn_wave()
    state.on_player_hit()
    state.on_player_hit()
    assert state.mini_lives == 1
    state.on_player_hit()
    assert state.mini_lives == 0
    assert state.game_ended
    assert not state.player_won
    assert state.end_msg == "OUT OF MINIGAME LIVES!"


def test_invaders_clearing_final_wave_wins():
    state = InvadersState()
    state.show_msg = False
    state.total_waves = 1
    state.current_wave = 1
    state.spawn_wave()
    state.enemies = []
    state.tick()
    assert state.game_ended
    assert state.player_won
    assert state.end_msg == "MISSION COMPLETE!"


def test_invaders_clearing_early_wave_advances():
    state = InvadersState()
    state.show_msg = False
    state.total_waves = 5
    state.current_wave = 1
    state.spawn_wave()
    state.enemies = []
    state.tick()
    assert not state.game_ended
    assert state.current_wave == 2
    assert state.show_msg
    assert state.msg_text.startswith("Wave 1 cleared!")


def test_invaders_saucers_reaching_the_ship_end_it():
    state = InvadersState()
    state.show_msg = False
    state.spawn_wave()
    for enemy in state.enemies:
        enemy.x = 1
    state.enemy_dir = -1
    for enemy in state.enemies:
        enemy.y = PLAYER_Y - ES
    state.tick()
    assert state.game_ended
    assert state.end_msg == "WAVE 1 FAILED"


def test_invaders_animation_frame_toggles():
    state = InvadersState()
    state.show_msg = False
    state.spawn_wave()
    assert state.anim_frame == 0
    for _ in range(22):
        state.tick()
    assert state.anim_frame == 1

