# Forecast2Caltopo

<!-- This project provides a command-line interface (CLI) for interacting with Avalanche Forecast API utilities. The CLI allows users to fetch avalanche forecasts for a specific geographic point and date and outputs the results as a GeoJSON file. -->

<!-- ## Features

- Fetch avalanche forecasts for a specific point (latitude and longitude).
- Specify a date for the forecast (defaults to today if not provided).
- Save results as a GeoJSON file for further use or visualization. -->

## Prerequisites

- Python 3.11 or later
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
| `--latitude`     | Yes      | Latitude of the point of interest.                                      |
| `--longitude`    | Yes      | Longitude of the point of interest.                                     |
| `--date`         | No       | Date for the forecast in `YYYY-MM-DD` format. Defaults to today.        |
| `--output`       | No       | Output file to save the GeoJSON result. Defaults to `ava_DEM_{forecast date}.json`.      |

### Example Usage

#### Basic Usage

Fetch the avalanche forecast for a point and save the result to the default output file:

```bash
python run.py --latitude 39.69507 --longitude -105.902
```

#### Specify a Date and Output File

Fetch the forecast for a specific date and save the result to a custom file:

```bash
python run.py --latitude 39.69507 --longitude -105.902 --date 2025-01-11 --output forecast.json
```

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
