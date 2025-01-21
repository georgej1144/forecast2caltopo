import uuid
from . import _CONFIG_
from . import models
import datetime
from math import ceil

def create_geojson(rules):
    return {
        "features": [
            {
                "geometry": None,
                "id": str(uuid.uuid4()),
                "type": "Feature",
                "properties": {
                    "alias": rule["rule"],
                    "title": rule["title"],
                    "class": "ConfiguredLayer"
                }
            } for rule in rules
        ],
        "type": "FeatureCollection"
    }

def danger_to_color(likelihood: int, scale_max: int):
    # sub 1 from scale_max for zero index 
    scale_adjusted = scale_max - 1
    if _CONFIG_.round_destructive_up:
        scale_adjusted = ceil(scale_adjusted)
    return _CONFIG_.colors[_CONFIG_.color_mapping[likelihood][int(scale_adjusted)]]

def sort_trim_aspects(aspects:list[str]):
    """
    Returns the start and end aspect
    Return None if aspects is empty for given elev
    """
    if len(aspects) == 0:
        return None
    aspect_regions = [_CONFIG_.regions[asp] for asp in aspects]
    ret = []
    i = 0
    while len(aspect_regions) > 0:
        # reset i if oob
        if i > len(aspect_regions) - 1: i = 0

        if ret == []:
            # if first pass, take init with first element
            ret.append(aspect_regions[i])
            aspect_regions.pop(i)
        
        bound_l, bound_r = aspect_regions[i]
        for j,reg in enumerate(ret):
            reg_l, reg_r = reg
            if bound_l == reg_r:
                # fits after, put i after j (j+1) and delete i
                ret.insert(j+1,aspect_regions[i])
                aspect_regions.pop(i)
                break
            elif bound_r == reg_l:
                # fits before, put i at j (j) and delete i
                ret.insert(j, aspect_regions[i])
                aspect_regions.pop(i)
                break
        i += 1
    return [ret[0][0],ret[-1][-1]]

def split_by_elevation(aspectElevations:list[str]):
    ret = {
        "alp": [],
        "tln": [],
        "btl": []
        }
    for e in aspectElevations:
        div = e.split("_")
        ret[div[1]].append(div[0])
    return ret

def format_as_rule(aspect_range, elevation_range, color):
    return f"s{"-".join([str(e) for e in _CONFIG_.slide_slopes])}" + f"a{"-".join([str(e) for e in aspect_range])}" + f"e{"-".join([str(e) for e in elevation_range])}{_CONFIG_.unit}" + f"c{color}"

def danger_to_rule(danger:models.AvalancheProblem, date:datetime.datetime):
    aspects = split_by_elevation(danger.aspectElevations)
    color = danger_to_color(_CONFIG_.likelihood_mapping[danger.likelihood], float(danger.expectedSize.max))
    rule = {
        "title": "",
        "rule": "sc_"
    }
    for key in aspects.keys():
        # per elev, get aspect bounds and 
        aspects[key] = sort_trim_aspects(aspects[key])
        if aspects[key]:
            # dont add rule if doesnt exist for elev
            rule["title"] = f"{danger.type} {date.isoformat()}"
            rule["rule"] += format_as_rule(aspects[key], _CONFIG_.elevations[key], color)
            rule["rule"] += "p"
    return rule

