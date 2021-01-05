from trapile import *


@weapon_ready
def attach_low_hp_in_range(marine, lowest_hp_enemy_in_range):
    marine.attack(lowest_hp_enemy_in_range)
    return True

@weapon_cooldown
def move_away_from_enemies(marine, enemies_in_range):
    offset = enemies_in_range.center - marine.position
    opposite_position = marine.position.negative_offset(offset)
    marine.smart(opposite_position)
    return True

@weapon_cooldown
def use_stimpack(marine, enemies_in_range):
    marine.unit(AbilityId.EFFECT_STIM)
    return False


def split(marine, closest_ally):
    pass
