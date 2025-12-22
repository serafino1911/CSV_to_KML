# CSV to KML Converter

A modern, desktop application for converting CSV geospatial data into KML (Keyhole Markup Language) files with contour visualization.

## Features

- **Batch Processing** - Convert multiple CSV files at once
- **Real-time Progress** - Visual progress tracking during conversion
- **Contour Generation** - Automatic contour generation from data points
- **Coordinate Conversion** - Support coordinate transformation
- **Flexible Configuration** - Customizable settings for projections, scales, and columns

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - `pandas` - Data manipulation
  - `matplotlib` - Contour generation
  - `pyproj` - Coordinate projection conversion
  - `numpy` - Numerical operations
  - `tkinter` - GUI framework (usually included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CSV_to_KML.git
cd CSV_to_KML
```

2. Install required dependencies:
```bash
pip install pandas matplotlib pyproj numpy
```

3. Run the application:
```bash
python GUI.py
```

## Usage

### Quick Start

1. **Launch the application** by running `GUI.py`
2. **Select CSV files** using the "Select Files" button
3. **Configure settings** (optional) via the "Configuration" button
4. **Start processing** with the "Start Processing" button
5. **Monitor progress** in the output log

### Configuration Settings

Click the **⚙️ Configuration** button to customize:

- **Levels** - Number of contour levels (default: 400)
- **Variable** - Name of the variable being measured (e.g., "Odor")
- **Projection CSV** - Input coordinate system (default: "utm")
- **TimeZone** - UTM zone specification (e.g., "32 T")
- **Projection KML** - Output coordinate system (default: "WGS84")
- **Static Scale** - Enable/disable static scaling (True/False)
- **Max Scale** - Maximum value for static scale (default: 130)
- **X Column** - Column name for X coordinates (default: "x_km")
- **Y Column** - Column name for Y coordinates (default: "y_km")
- **Value Column** - Column name for data values (default: "value")
- **Saving Folder** - Output directory for generated KML files

### CSV File Format

Your CSV file should contain at least three columns:
- X coordinates (e.g., `x_km` or `X_KM`)
- Y coordinates (e.g., `y_km` or `Y_KM`)
- Data values (e.g., `value` or `VALUE`)

Example:
```csv
x_km,y_km,value
500.5,4500.2,45.3
501.2,4501.8,52.1
502.0,4502.5,48.7
```

## File Structure

```
CSV_to_KML/
├── GUI.py                  # Main application interface
├── main.py                 # Core processing logic
├── configurations/         # Configuration files
│   └── kml_config.py      # KML styling configuration
├── .gitignore             # Git ignore patterns
└── README.md              # This file
```

## Output

The application generates KML files with:
- Color-coded contour polygons based on data values
- Customizable color scales
- Border polygons for data extent
- Compatible with Google Earth and other KML viewers

## Troubleshooting

### Common Issues

**"Column not found" error**
- Check that your CSV column names match the configuration

**"No files selected" warning**
- Make sure to select CSV files before clicking "Start Processing"

**Coordinate conversion errors**
- Verify the TimeZone/UTM zone is correct for your data
- Ensure coordinates are in the expected format

**Application doesn't start**
- Verify all dependencies are installed: `pip list`
- Check Python version: `python --version`

---

**Note**: This application is designed for geospatial data processing and requires properly formatted CSV files with coordinate information.
