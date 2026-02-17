# F1 Stats Explorer

Data analysis project based on Formula 1 race results using the Jolpica API.

## Features

- **Live Standings** : View driver and constructor standings for each season
- **Interactive Graph** : Visualize points evolution race by race
- **Detailed Statistics** : Wins, podiums, and retirements for each driver
- **Modern Interface** : Clean dark design with F1 theme (black and red)
- **Up-to-Date Data** : Integration with Jolpica API for official F1 data

## Architecture

```
F1-Stats-Explorer/
├── src/
│   ├── app.py                # Main FastAPI Application
│   ├── api/
│   │   └── routes.py         # API Endpoints
│   ├── data/
│   │   └── fetcher.py        # Jolpica API Data Fetcher
│   ├── static/
│   │   └── style.css         # Modern Styling
│   └── templates/
│       └── index.html        # User Interface
├── docker-compose.yml        # Docker Orchestration
├── Dockerfile                # Docker Configuration
└── requirements.txt          # Python Dependencies
```

## Tech Stack

- **Backend** : Python 3.11 + FastAPI, Uvicorn
- **Frontend** : HTML5, CSS3, JavaScript
- **Graph** : Plotly 2.24.2
- **External API** : Jolpica API (official F1 data)
- **Containerization** : Docker & Docker Compose

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Or Python 3.8+ + pip

### With Docker

```bash
# Clone the repository
git clone git@github.com:Arkane60/F1-Stats-Explorer.git
cd F1-Stats-Explorer

# Start the application
docker compose up
```

### With Python

```bash
# Clone the repository
git clone git@github.com:Arkane60/F1-Stats-Explorer.git
cd F1-Stats-Explorer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Launch the application
cd src
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Access the application: http://localhost:8000

## Usage

1. **Select a year** from the dropdown menu
2. **Click "Load"** to fetch the data
3. **Explore the data** :
   - Driver standings
   - Constructor standings
   - Points evolution graph
   - Statistics (wins, podiums, retirements)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/standings/drivers?season={year}` | Driver standings |
| GET | `/standings/constructors?season={year}` | Constructor standings |
| GET | `/races/points?season={year}` | Points evolution |
| GET | `/stats/pilots?season={year}` | Pilot statistics |
| GET | `/` | Web interface |

## Design

The interface uses a modern theme inspired by F1 :
- **Palette** : Deep black (#000) + bright red (#ff0000)
- **Typography** : Segoe UI
- **Effects** : Glassmorphism, red glows, fluid animations

## Contributing

Any contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.