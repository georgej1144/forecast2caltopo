import uuid
from . import _CONFIG_
from . import models
import datetime
from math import ceil


# new treecover option:
# 80% tree cover is safe assumed max treecover%


def rule_tool(mode:str, range:list[int,int]):
    return mode + '-'.join([str(n) for n in range])

def get_aspect_helpers() -> list[dict]:
    ret = []
    for zone in _CONFIG_.regions.keys():
        ret.append({
            "title": zone.upper(),
            "rule": "sc_" + rule_tool("a",_CONFIG_.regions[zone]) + "c" + _CONFIG_.aspect_shading_color + "p"
        })
    return ret

def get_treecover_helpers():
    ret = []
    for i,zone in enumerate(_CONFIG_.treecover_thresholds.keys()):        
        ret.append({
            "title": f".{zone.upper()}",
            "rule": "sc_" + rule_tool("t", _CONFIG_.treecover_thresholds[zone]) + "c" + _CONFIG_.treecover_shading_colors[i] + "p"
        })
    return ret

def get_treeline_helpers_legacy() -> list[dict]:
    ret = []
    for elev in _CONFIG_.treeline_transitions:
        ret.append({
            "title": f" Elevation Band {elev}",
            "rule": "sc_" + rule_tool("e", [elev-_CONFIG_.treeline_bands_width, elev+_CONFIG_.treeline_bands_width]) + _CONFIG_.unit + "c" + _CONFIG_.treeline_bands_color + "p"
        })
    return ret

def get_helper_layers() -> list[dict]:
    helpers = []
    if _CONFIG_.include_helpers.aspect_layers:
        helpers += get_aspect_helpers()
    if _CONFIG_.include_helpers.treeline_bands_legacy:
        helpers += get_treeline_helpers_legacy()
    if _CONFIG_.include_helpers.treecover_shading:
        helpers += get_treecover_helpers()
    return helpers

def create_geojson(rules:list[dict]):
    rules = rules + get_helper_layers()
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

def treeline_to_elevations(treeline: tuple[int,int]) -> list[list[int,int]]:
    # legacy treeline func
    return {
        "alp": [treeline[1],99999],
        "tln": treeline,
        "btl": [0,treeline[0]]
    }

def format_as_rule(aspect_range, treecover_range, color):
    return  rule_tool("s",_CONFIG_.slide_slopes) + \
            rule_tool("a", aspect_range) + \
            rule_tool("t", treecover_range) + \
            "c" + color + "p"

def format_as_rule_legacy(aspect_range, elevation_range, color):
    return  rule_tool("s",_CONFIG_.slide_slopes) + \
            rule_tool("a", aspect_range) + \
            rule_tool("e", elevation_range) + \
            _CONFIG_.unit + "c" + color + "p"

def danger_to_rule(danger:models.AvalancheProblem, date:datetime.datetime):
    aspects = split_by_elevation(danger.aspectElevations)
    color = danger_to_color(_CONFIG_.likelihood_mapping[danger.likelihood], float(danger.expectedSize.max))
    if _CONFIG_.legacy_treeline:
        elevations = treeline_to_elevations(_CONFIG_.treeline_transitions)
    else:
        treecovers = _CONFIG_.treecover_thresholds
    rule = {
        "title": "",
        "rule": "sc_"
    }
    for key in aspects.keys():
        # per elev, get aspect bounds and 
        aspects[key] = sort_trim_aspects(aspects[key])
        if aspects[key]:
            # dont add rule if doesnt exist for elev
            rule["title"] = f" {danger.type} {date.isoformat()}"
            if _CONFIG_.legacy_treeline:
                rule["rule"] += format_as_rule_legacy(aspects[key], elevations[key], color)
            else:
                rule["rule"] += format_as_rule(aspects[key], treecovers[key], color)
            rule["rule"] += "p"
    return rule

