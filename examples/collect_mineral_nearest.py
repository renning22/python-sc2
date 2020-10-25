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


class CollectMineral(sc2.BotAI):

    async def on_step(self, iteration):
        print(f'{iteration}')
        marines = self.units(UnitTypeId.MARINE)
        minerals = self.all_units(UnitTypeId.NATURALMINERALS)
        for marine in marines:
            nearest_ones = minerals.closest_n_units(marine, n=1)
            if nearest_ones:
                marine.move(nearest_ones[0])

def main():
    sc2.run_game(
        sc2.maps.get("CollectMineralShards"),
        [Bot(Race.Terran, CollectMineral())],
        rgb_render_config={
            'window_size': (800, 600),
            'minimap_size': (200, 200),
        },
        realtime=True,
    )

if __name__ == "__main__":
    main()
