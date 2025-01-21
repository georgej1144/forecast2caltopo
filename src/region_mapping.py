from . import models


region_aliases = {
    "frontrange": 1,
    "northfrontrange": 1,
    "northernfrontrange": 1,
    "vail": 1,
    "breck": 1,
    "breckenridge": 1,
    "vailpass": 1,


    "southfrontrange": 2,
    "southernfrontrange": 2,
    "blueskyarea": 2,

    "hahnspeaks": 3,
    "northcentral": 3,
    "hahnspeaksarea": 3,
    "northcentralarea": 3,

    "northwest": 4,
    "northwestern": 4,
    "northwestarea": 4,
    "northwesternarea": 4,
    "sugarloaf": 4,
    "elkmountain": 4,
    "northwestmountains": 4,
    "northwestrange": 4,
    "goremountain": 4,
    "sheephorn": 4,
    "sheephornarea": 4,

    "holycross": 5,
    "holycrossarea": 5,
    "whiteriver": 5,
    "whiteriverforest": 5,
    "beavercreek": 5,
    "mtelbert": 5,

    "gunnison": 6,
    "gunnisonnationalforest": 6,
    "gunnisonforestrange": 6,

    "aspen": 7,
    "aspenrange": 7,
    "crestedbutte": 7,
    "butte": 7,

    "grandmesa": 8,
    "grandmesaarea": 8,
    "westcentral": 8,
    "westcentralarea": 8,

    "grandmesapark": 9,
    "uncompahgrepark": 9,
    "gunnisonnationalpark": 9,

    "pikespeak": 10,
    "dunesrange": 10,
    "southeastarea": 10,
    "southeastrange": 10,

    "sawtootharea": 11,
    "sanluisarea": 11,

    "uncompahgre": 12,
    "uncompahgrearea": 12,
    "twinsisters": 12,
    "twinsistersarea": 12,
    "sneffelsarea": 12,
    "silverton": 12,

    "farsouthrange": 13,
    "southwestrange": 13,
    "farsoutharea": 13,
    "southwestarea": 13,
    "sanjuan": 13,
    "sanjuanforest": 13,
    }


region_name_mapping = {
    1:  "5-13-12-6-10-11-21-22-24-29-30-47-37-36-34-35-31-23",
    2:  "51-33-48",
    3:  "4-14",
    4:  "20-28-26-19-2-3-25",
    5:  "38-40-46-39-52",
    6:  "72-67-73-66",
    7:  "65-44-45-54-55-53-64-56",
    8:  "60-42-59-58-43-57",
    9:  "62-63-74",
    10: "101-69-80-91-78",
    11: "77-81-76-90-82",
    12: "84-83-88-85",
    13: "93-92-100-86-97-98-94-99-95-96-89-87",
    }

def search_for_zone(input:str)-> str|None:
    """
    Given a cleaned user provided phrase, parse the mappings to find the publicName of the desired area

    Returns None if no mapping is found
    """
    try:
        internal_id = region_aliases[input]
    except KeyError:
        internal_id = None
    if internal_id:
        return region_name_mapping[internal_id]
    else:
        return None