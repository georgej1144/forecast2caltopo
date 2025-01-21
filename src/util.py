from . import models
from . import LOGGER
from . import _CONFIG_
from . import geojson_util
from shapely.geometry import Polygon, Point

def clean_input(input):
    """
    Normalize user input to search for a region mapping.
    Normalization is done by stripping all whitespace and punctuation and forcing lowercase
    """
    return "".join(char for char in input if char.isalnum()).lower()

def get_specific_avaforecast(data:list[models.AvalancheForecast], areaId):
    for obj in data:
        if obj.areaId == areaId:
            return obj
    LOGGER.error(f"Zone {areaId} not found in data.")
    return None

def find_region_for_point(point: tuple[float, float], regions: models.RegionFeatureCollection) -> str:
    """
    Finds the region containing the given point.
    :param point: Tuple of (latitude, longitude)
    :param regions: List of Region objects
    :return: The areaId for the region containing the point, or None if not found
    """
    query = Point(point)
    query_lat, query_lon = point

    for region in regions.features:
        # Quick rejection using the bounding box
        min_lon, min_lat, max_lon, max_lat = region.bbox
        if min_lat <= query_lat <= max_lat and min_lon <= query_lon <= max_lon:
            # Check if the point is inside the polygon(s) of the region
            for poly in region.geometry.coordinates:
            
                # flip lat/lon and create Polygon objects for each defined shape
                fixed_poly = Polygon([[coord[1],coord[0]] for coord in poly[0]])
                # print(fixed_poly[0])
                # break # remove

                if query.within(fixed_poly):
                    return region.id

    return None

def interpret_problems(problems: list[models.AvalancheProblem], date):
    """
    Given a list of problems for some day, return a dict of
    the problem to export into DEM Shading rules.
    """
    # init empty object for 
    result = []
    for i,problem in enumerate(problems):
        # init problem rules
        # start with an array for each elevation slice

        result.append(geojson_util.danger_to_rule(problem, date.date()))
        
    return result