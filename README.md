
# Google Trends Analysis

Analyze Google Trends data for keywords, regions, and timeframes. Generates time series and bar plots.

## Features
- Fetch Google Trends data for specific keywords.
- Analyze by geographic region and timeframe.
- Outputs CSV and visualizations.

## Requirements
- **Python**: Python 3.10.9 (likely compatible with Python 3.1x versions).
- **Dependencies**: Install with:
```bash
pip install -r requirements.txt
```

## Configuration
Edit the script to set:
- **Keywords**: `KEYWORDS = ["keyword1", "keyword2", "keyword3"...]`
- **Region**: `GEO` options:
  - `"IT"`: Italy (nationwide)
  - `"IT-52"`: Tuscany
  - `"IT-62"`: Lazio
  - `""`: Worldwide
- **Timeframe**: `TIMEFRAME` options:
  - `'now 1-H'`: Last hour
  - `'now 4-H'`: Last 4 hours
  - `'now 1-d'`: Last day
  - `'now 7-d'`: Last 7 days
  - `'today 1-m'`: Past 30 days
  - `'today 3-m'`: Past 90 days
  - `'today 12-m'`: Past 12 months
  - `'today 5-y'`: Past 5 years
  - `'all'`: Since the beginning of available data.

## Usage
Run the script:
```bash
python marketing.py
```

## Outputs
The `EXAMPLE` folder contains examples of typical outputs.
- **CSV**: Trends data (`GoogleTrends_Mensile.csv`)
- **Plots**: 
  - Line plot (`GoogleTrends_Mensile_Plot.png`)
  - Bar plot (`GoogleTrends_Bar_Plot_Sorted_Averages.png`)

## License
MIT License.
