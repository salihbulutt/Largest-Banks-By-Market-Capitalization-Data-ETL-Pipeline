# :bank: Largest Banks ETL Pipeline
A Python-based ETL (Extract, Transform, Load) pipeline that scrapes data about the world's largest banks from Wikipedia, transforms the market capitalization values into multiple currencies, and stores the results in both CSV and SQLite database formats.

## 📋 Table of Contents

- [Overview](#dart-overview)
- [Features](#sparkles-features)
- [Prerequisites](#package-prerequisites)
- [Installation](#rocket-installation)
- [Usage](#computer-usage)
- [Project Structure](#file_folder-project-structure)
- [Pipeline Workflow](#arrows_counterclockwise-pipeline-workflow)
- [Configuration](#gear-configuration)
- [Output Files](#bar_chart-output-files)
- [Query Examples](#mag-query-examples)
- [Logging](#memo-logging)
- [Contributing](#handshake-contributing)
- [License](#page_facing_up-license)

## :dart: Overview

This project demonstrates a complete ETL pipeline that:
- **Extracts** GDP data from Wikipedia's archived page
- **Transforms** the data from millions to billions USD
- **Loads** the processed data into CSV and SQLite database
- **Logs** every step of the process with timestamps

## :sparkles: Features

- ✅ Web scraping with Beautiful Soup
- ✅ Data transformation and cleaning with Pandas
- ✅ Dual output: CSV and SQLite database
- ✅ Comprehensive logging system
- ✅ SQL query execution capability
- ✅ Error handling and data validation

## :package: Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## :rocket: Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/gdp-etl-pipeline.git
cd gdp-etl-pipeline
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## :computer: Usage

### Basic Usage

Run the ETL pipeline:

```bash
python etl_pipeline.py
```

### Advanced Usage

You can modify the configuration in `config.py` or pass parameters directly in the script.

## :file_folder: Project Structure

```
gdp-etl-pipeline/
│
├── etl_pipeline.py           # Main ETL script
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
├── LICENSE                  # License file
│
├── data/                    # Output directory (created on first run)
│   ├── Countries_by_GDP.csv
│   └── World_Economies.db
│
├── logs/                    # Logs directory (created on first run)
│   └── etl_project_log.txt
│
└── tests/                   # Unit tests (optional)
    └── test_etl.py
```

## :arrows_counterclockwise: Pipeline Workflow

```
1. Extract
   ↓
   Scrape GDP data from Wikipedia Archive
   ↓
2. Transform
   ↓
   Convert millions → billions USD
   Round to 2 decimal places
   ↓
3. Load
   ↓
   Save to CSV
   Save to SQLite Database
   ↓
4. Query & Validate
   ↓
   Execute sample queries
   ↓
5. Log All Steps
```

## :gear: Configuration

Edit `config.py` to customize:

```python
# Data source
URL = 'https://web.archive.org/web/...'

# Output paths
CSV_PATH = './data/Countries_by_GDP.csv'
DB_NAME = './data/World_Economies.db'

# Database settings
TABLE_NAME = 'Countries_by_GDP'

# Logging
LOG_FILE = './logs/etl_project_log.txt'
```

## :bar_chart: Output Files

### CSV Output
Located at: `data/Countries_by_GDP.csv`

| Country | GDP_USD_billions |
|---------|------------------|
| United States | 25462.70 |
| China | 17963.17 |
| ... | ... |

### SQLite Database
Located at: `data/World_Economies.db`

Table: `Countries_by_GDP`
- Country (TEXT)
- GDP_USD_billions (REAL)

## :mag: Query Examples

The pipeline includes a sample query. You can add more:

```python
# Get countries with GDP >= 100 billion
query = "SELECT * FROM Countries_by_GDP WHERE GDP_USD_billions >= 100"

# Get top 10 countries
query = "SELECT * FROM Countries_by_GDP ORDER BY GDP_USD_billions DESC LIMIT 10"

# Get average GDP
query = "SELECT AVG(GDP_USD_billions) as avg_gdp FROM Countries_by_GDP"
```

## :memo: Logging

All operations are logged with timestamps in `logs/etl_project_log.txt`:

```
2025-Nov-22-14:30:15 : Preliminaries complete. Initiating ETL process
2025-Nov-22-14:30:16 : Data extraction complete. Initiating Transformation process
2025-Nov-22-14:30:16 : Data transformation complete. Initiating loading process
...
```

## :handshake: Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## :page_facing_up: License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Your Name
- GitHub: [@salihbulutt](https://github.com/salihbulutt)
- Email: salihbulut1@gmail.com

## 🙏 Acknowledgments

- Data source: Wikipedia
- Built with Python, BeautifulSoup, Pandas, and SQLite

## 📈 Future Enhancements

- [ ] Add unit tests
- [ ] Implement command-line arguments
- [ ] Add data visualization
- [ ] Create REST API endpoint
- [ ] Add Docker support
- [ ] Implement scheduling (cron jobs)

---

**⭐ If you find this project helpful, please consider giving it a star!**

:arrow_up: [Back to the Top](#bank-largest-banks-etl-pipeline)
