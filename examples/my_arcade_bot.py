import random
from sys import platform
from typing import (Any, Dict, List, Optional, Set,  # mypy type checking
                    Tuple, Union)

import sc2
from sc2 import Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.player import Bot
from sc2.position import Point2, Point3
from sc2.unit import Unit
from sc2.units import Units

import ning

"""
To play an arcade map, you need to download the map first.

Open the StarCraft2 Map Editor through the Battle.net launcher, in the top left go to
File -> Open -> (Tab) Blizzard -> Log in -> with "Source: Map/Mod Name" search for your desired map, in this example "Marine Split Challenge-LOTV" map created by printf
Hit "Ok" and confirm the download. Now that the map is opened, go to "File -> Save as" to store it on your hard drive.
Now load the arcade map by entering your map name below in
sc2.maps.get("YOURMAPNAME") without the .SC2Map extension


Map info:
You start with 30 marines, level N has 15+N speed banelings on creep

Type in game "sling" to activate zergling+baneling combo
Type in game "stim" to activate stimpack


Improvements that could be made:
- Make marines constantly run if they have a ling/bane very close to them
- Split marines before engaging
"""


class MarineSplitChallenge(sc2.BotAI):
    async def on_step(self, iteration):
        units = self.units(UnitTypeId.MARINE)
        # do marine micro vs zerglings
        for unit in units:
            attack_range = unit.ground_range
            others_in_range = [u for u in units if u !=
                               unit and unit.target_in_range(u, -attack_range/3)]
            if others_in_range:
                closest_ally = min(
                    others_in_range, key=lambda u: u.distance_to_squared(unit))
                if random.random() < 0.2:
                    ning.split(unit, closest_ally)

            enemies_in_range = self.enemy_units.filter(
                lambda u: unit.target_in_range(u))
            if enemies_in_range:
                # attack (or move towards) zerglings / banelings
                if unit.weapon_cooldown <= self._client.game_step / 2:
                    # attack lowest hp enemy if any enemy is in range
                    # Use stimpack
                    if (
                        self.already_pending_upgrade(UpgradeId.STIMPACK) == 1
                        and not unit.has_buff(BuffId.STIMPACK)
                        and unit.health > 10
                    ):
                        ning.use_stimpack(unit, enemies_in_range)

                    # attack baneling first
                    filtered_enemies_in_range = enemies_in_range.of_type(
                        UnitTypeId.BANELING)

                    if not filtered_enemies_in_range:
                        filtered_enemies_in_range = enemies_in_range.of_type(
                            UnitTypeId.ZERGLING)
                    # attack lowest hp unit
                    lowest_hp_enemy_in_range = min(
                        filtered_enemies_in_range, key=lambda u: u.health)
                    ning.attach_low_hp_in_range(unit, lowest_hp_enemy_in_range)
                    continue
                else:
                    # move away from zergling / banelings
                    ning.move_away_from_enemies(unit, enemies_in_range)

    async def on_start(self):
        await self.chat_send("Edit this message for automatic chat commands.")
        self._client.game_step = 4  # do actions every X frames instead of every 8th


def main():
    sc2.run_game(
        sc2.maps.get("Marine Split Challenge"),
        [Bot(Race.Terran, MarineSplitChallenge())],
        realtime=True,
        rgb_render_config={
            'window_size': (800, 600),
            'minimap_size': (200, 200),
        } if platform == 'linux' else None,
        save_replay_as="Example.SC2Replay",
    )


if __name__ == "__main__":
    main()
