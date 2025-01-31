# Forecast2Caltopo

<!-- This project provides a command-line interface (CLI) for interacting with Avalanche Forecast API utilities. The CLI allows users to fetch avalanche forecasts for a specific geographic point and date and outputs the results as a GeoJSON file. -->

<!-- ## Features

- Fetch avalanche forecasts for a specific point (latitude and longitude).
- Specify a date for the forecast (defaults to today if not provided).
- Save results as a GeoJSON file for further use or visualization. -->

## Prerequisites

- Python 3.10 or later
- Required dependencies (install via `pip`):

```bash
pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

## Usage

### Command-line Arguments

The CLI accepts the following arguments:

| Argument         | Required | Description                                                             |
|------------------|----------|-------------------------------------------------------------------------|
| `--lat` or `--latitude`     | Yes      | Latitude of the point of interest.                                      |
| `--lon` or `--longitude`    | Yes      | Longitude of the point of interest.                                     |
| `--date`         | No       | Date for the forecast in `YYYY-MM-DD` format. Defaults to today.        |
| `--output`       | No       | Output file to save the GeoJSON result. Defaults to `ava_DEM_{forecast date}.json`.      |

### Example Usage

#### Basic Usage

Fetch the avalanche forecast for a point and save the result to the default output file:

```bash
python3 run.py --lat 39.69507 --long -105.902
```

#### Specify a Date and Output File

Fetch the forecast for a specific date and save the result to a custom file:

```bash
python3 run.py --latitude 39.69507 --longitude -105.902 --date 2025-01-11 --output forecast.json
```

## Configuration File

The `config.json` file provides customizable settings for the CLI and its utilities. Below is an explanation of the configuration options:

    - colors: Defines the hexadecimal color codes for different avalanche risk levels.
    - color_mapping: Specifies the mapping of risk levels to colors for different scenarios.
    - slide_slopes: Defines the range of slopes (in degrees) considered prone to avalanches.
    - elevations: Categorizes elevation levels into alpine (alp), treeline (tln), and below treeline (btl).
    - unit: The unit system used for measurements (f for Fahrenheit, c for Celsius).
    - regions: Forecast Rose's  directions (e.g., north, southeast) to their respective angular ranges.
    - likelihood_mapping: Assigns numerical values to likelihood descriptors from forecasts.
    - round_destructive_up: A boolean value indicating whether to round destructive potential values up.

<!--
```json
{
    "colors": {
        "yellow": "FFFF00",
        "orange": "FF8000",
        "red": "FF0000",
        "black": "000000"
    },
    "color_mapping": [
        ["yellow", "black", "black", "black"],
        ["yellow", "black", "black", "black"],
        ["yellow", "black", "black", "black"],
        ["yellow", "red", "black", "black"],
        ["yellow", "orange", "black", "black"]
    ],
    "slide_slopes": [25, 90],
    "elevations": {
        "alp": [11500, 99999],
        "tln": [10500, 11500],
        "btl": [0, 10500]
    },
    "unit": "f",
    "regions": {
        "n": [338, 23],
        "ne": [23, 68],
        "e": [68, 113],
        "se": [113, 158],
        "s": [158, 203],
        "sw": [203, 248],
        "w": [248, 293],
        "nw": [293, 338]
    },
    "likelihood_mapping": {
        "unlikely": 0,
        "possible": 1,
        "likely": 2,
        "verylikely": 3,
        "certain": 4
    },
    "round_destructive_up": true
}
```
-->

## Output

The CLI generates a GeoJSON file containing the avalanche forecast information. The file can be used for visualization or integration with GIS tools like Caltopo.

<!-- 
## Error Handling

- If the latitude or longitude is invalid, the program will report an error.
- If no region is found for the specified point, an error message will be displayed.
- If the forecast or regions cannot be fetched, the program will notify the user. -->

<!-- ## Development

### File Structure

- `run.py`: The main script providing the CLI functionality.
- `src/`: Contains utility modules for interacting with the Avalanche Forecast API. -->

<!-- ### Testing

Run the script with various inputs to ensure all arguments and functionalities work as expected. For example:

- Missing or invalid arguments.
- Validating output GeoJSON files for different points and dates. -->
<!-- 
## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

Feel free to contribute by submitting issues or pull requests! -->


<!-- layer for each quadrant
color config for quardant

layers for treeline splits
treeline split elevation band width config
treeline split color config -->