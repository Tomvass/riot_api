from cassiopeia import riotapi
from operator import attrgetter, itemgetter

api_key = "FIND-ME-BITCH"

riotapi.set_region("EUW")
riotapi.set_api_key(api_key)
me = riotapi.get_summoner_by_name("Sondjaskysa")
order_dict = {"total": attrgetter("level", "points"),
              "nearest": attrgetter("points_until_next_level")}

ALL_CHAMP_NAMES = set([c.name for c in riotapi.get_champions()])


def check_ingame(summoner=me):
    return riotapi.get_current_game(summoner)


def get_full_masteries(name=me.name, order="total"):
    champs = riotapi.get_summoner_by_name(name).champion_masteries()
    order = order_dict[order] or attrgetter("level", "points")
    return sorted(champs.values(), key=order, reverse=True)


def suggest_easy(name=me.name, limit=1300, check_box=True):
    champs = get_full_masteries(name=name, order="nearest")
    max_level = lambda x: x.points_until_next_level == 0
    unskilled_champs = ALL_CHAMP_NAMES.difference(
        [c.champion.name for c in champs])
    all_champs = {c: (0, 0) for c in unskilled_champs}
    for champ in champs:
        points = champ.points_until_next_level
        if not max_level(champ) and points < limit:
            if champ.chest_granted and check_box:
                pass
            else:
                all_champs[champ.champion.name] = (points, champ.level)

    return sorted(all_champs.items(), key=itemgetter(1))
