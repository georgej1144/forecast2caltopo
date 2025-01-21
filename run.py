import argparse
from src import api_util
from src import util
from src import geojson_util
import datetime
import json
import asyncio

def parse_arguments():
    parser = argparse.ArgumentParser(description="Command-line interface for Avalanche Forecast API utilities.")
    parser.add_argument("--lat","--latitude", type=float, required=True, help="Latitude of the point of interest.")
    parser.add_argument("--lon","--longitude", type=float, required=True, help="Longitude of the point of interest.")
    parser.add_argument("--date", type=str, default=None, help="Date for the forecast in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--output", type=str, default=None, help="Output file to save the GeoJSON result.")
    return parser.parse_args()

client = api_util.avy_forecast_getter()

async def main_helper(client_obj, date):
    forecasts = await client_obj.avy_forecast(date=date)
    regions = await client_obj.avy_regions(date=date)
    return forecasts, regions

def main():
    args = parse_arguments()
    point = (args.lat, args.lon)
        
    if args.date == None:
        date = datetime.datetime.now()
    else:
        try:
            date = datetime.datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.datetime.today()
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
            return

    forecasts, regions = asyncio.run(main_helper(client, date))
    if not forecasts or not regions:
        print("Error: Failed to fetch forecasts or regions.")
        return

    zone_id = util.find_region_for_point(point, regions)
    if not zone_id:
        print(f"Error: No region found for the point {point}.")
        return

    zone_forecast = util.get_specific_avaforecast(forecasts, zone_id)
    if not zone_forecast:
        print(f"Error: No forecast available for zone ID {zone_id}.")
        return

    day_probs = zone_forecast.avalancheProblems.days[0]
    interp = util.interpret_problems(day_probs, date)
    geojson_result = geojson_util.create_geojson(interp)

    filename = args.output if args.output else f"ava_DEM_{date.date().isoformat()}.json"
    with open(filename, "w+") as f:
        json.dump(geojson_result, f)

    print(f"GeoJSON result saved to {filename}.")

if __name__ == "__main__":
    main()
