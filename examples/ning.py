from trapile import *


def move_away(unit, point):
    offset = point - unit.position
    opposite_position = unit.position.negative_offset(offset)
    unit.smart(opposite_position)


@weapon_ready
def attach_low_hp_in_range(marine, lowest_hp_enemy_in_range):
    marine.attack(lowest_hp_enemy_in_range)


@weapon_cooldown
def move_away_from_enemies(marine, enemies_in_range):
    move_away(marine, enemies_in_range.center)


@weapon_cooldown
def use_stimpack(marine, enemies_in_range):
    marine.unit(AbilityId.EFFECT_STIM)


def split(marine, closest_ally):
    move_away(marine, closest_ally.position)
