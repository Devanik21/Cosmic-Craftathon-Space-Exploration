# Cosmic Craftathon Space Exploration

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/Cosmic-Craftathon-Space-Exploration?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/Cosmic-Craftathon-Space-Exploration?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> A hackathon-born space exploration platform — data-driven planetary science, asteroid tracking, and cosmic discovery tools.

---

**Topics:** `astronomy` · `astrophysics-ml` · `data-science` · `deep-learning` · `hackathon` · `machine-learning` · `neural-networks` · `simulation` · `physics-based-engine` · `space-exploration-simulation`

## Overview

Cosmic Craftathon is a space exploration web application developed during a hackathon, combining NASA
open data APIs with interactive visualisations to make planetary science and space mission data accessible
to curious non-specialists. It provides a multi-panel dashboard covering Near-Earth Object (NEO) tracking,
Mars rover imagery, the International Space Station live position, and the NASA Astronomy Picture of the Day.

The application was built around a core belief: space data is publicly available and endlessly fascinating,
but raw JSON from a NASA API is not an experience. Cosmic Craftathon transforms that data into something
visually compelling and narratively rich — animating asteroid orbital trajectories, mapping ISS position
in real time, and contextualising rover images with terrain descriptions.

The architecture prioritises responsiveness and offline resilience: API responses are cached locally
to handle rate limits gracefully, the UI degrades cleanly when individual API endpoints are unavailable,
and all map and orbit visualisations are client-side rendered without server dependency.

---

## Motivation

Space exploration is one of humanity's most ambitious endeavours, yet most people interact with it
only through occasional news headlines. This project was built during a hackathon to create an always-on
window into active space exploration — turning live NASA telemetry and imagery into an immersive,
educational experience that communicates the scale and pace of what is happening right now beyond Earth's atmosphere.

---

## Architecture

```
NASA Open APIs (NeoWs, APOD, Mars Rover, ISS Position)
        │
  API Layer (requests + local cache with TTL)
        │
  ┌────────────────────────────────────────────┐
  │  Dashboard Panels:                         │
  │  ├── NEO Tracker (orbital viz, distance)   │
  │  ├── APOD Viewer (image + description)     │
  │  ├── Mars Rover Gallery (Curiosity/Percy)  │
  │  └── ISS Live Map (real-time position)     │
  └────────────────────────────────────────────┘
        │
  Streamlit / Plotly interactive frontend
```

---

## Features

### Near-Earth Object Tracker
Live asteroid and comet tracking using NASA's NeoWs API — approach velocity, miss distance from Earth, estimated diameter, and hazard classification displayed per object.

### Orbital Trajectory Visualisation
3D interactive Plotly chart of NEO approach trajectories relative to Earth, with selectable date range and object filtering by hazard status.

### Astronomy Picture of the Day
Daily NASA APOD image with full scientific description, expandable to full resolution, with a calendar picker for historical archive browsing.

### Mars Rover Imagery Gallery
Photographic gallery from Curiosity and Perseverance rover cameras, filterable by sol (Mars day), camera type (NAVCAM, MASTCAM, CHEMCAM), and mission date.

### ISS Real-Time Position Map
Live ISS ground track on a Plotly Mapbox chart, auto-refreshing every 5 seconds, with orbital altitude, velocity, and crew information.

### Asteroid Hazard Dashboard
Summary statistics of currently tracked potentially hazardous asteroids (PHAs) with size distribution histogram and closest approach timeline.

### Mission Timeline
Interactive timeline of major space missions (Apollo, Voyager, Hubble, JWST, Artemis) with milestones, objectives, and status indicators.

### Offline Cache
All API responses cached locally with configurable TTL so the dashboard remains functional during API rate limiting or network interruption.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **Streamlit** | Dashboard framework | Multi-panel layout with auto-refresh support |
| **NASA Open APIs** | Space data source | NeoWs, APOD, Mars Rover Photos, ISS Position |
| **Plotly** | Interactive charts | 3D orbit plots, ISS map, NEO histogram |
| **requests** | HTTP client | API calls with timeout and retry handling |
| **pandas** | Data processing | NEO data wrangling and timeline construction |
| **python-dotenv** | Config | NASA API key management |

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JavaScript projects)
- A virtual environment manager (`venv`, `conda`, or equivalent)
- API keys as listed in the Configuration section

### Installation

```bash
git clone https://github.com/Devanik21/Cosmic-Craftathon-Space-Exploration.git
cd Cosmic-Craftathon-Space-Exploration
python -m venv venv && source venv/bin/activate
pip install streamlit requests pandas plotly python-dotenv
echo 'NASA_API_KEY=your_key_here' > .env
# Free NASA API key: https://api.nasa.gov/
streamlit run app.py
```

---

## Usage

```bash
# Launch dashboard
streamlit run app.py

# Fetch today's APOD
python fetch_apod.py --date today

# Download NEO data for date range
python fetch_neos.py --start 2026-01-01 --end 2026-03-15
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `NASA_API_KEY` | `DEMO_KEY (rate limited)` | Free key from api.nasa.gov — required for full rate limits |
| `CACHE_TTL_SECONDS` | `300` | API response cache lifetime in seconds |
| `ISS_REFRESH_INTERVAL` | `5` | ISS position refresh interval in seconds |
| `DEFAULT_NEO_DAYS` | `7` | Default NEO tracking window in days |

> Copy `.env.example` to `.env` and populate required values before running.

---

## Project Structure

```
Cosmic-Craftathon-Space-Exploration/
├── README.md
├── Space Game Hackathon/final_game.py
└── ...
```

---

## Roadmap

- [ ] JWST image gallery with spectral overlay and science summary per observation
- [ ] Exoplanet explorer using the NASA Exoplanet Archive API with habitability scoring
- [ ] Launch schedule calendar with countdown timers for upcoming SpaceX, NASA, and ESA launches
- [ ] Solar activity dashboard: sunspot number, solar flare alerts, geomagnetic storm index
- [ ] Citizen science mode: flag interesting features in Mars rover images for expert review

---

## Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit your changes: `git commit -m 'feat: add your idea'`
4. Push to your branch: `git push origin feature/your-idea`
5. Open a Pull Request with a clear description

Please follow conventional commit messages and add documentation for new features.

---

## Notes

NASA API DEMO_KEY has a rate limit of 30 requests/hour. Register for a free personal API key at api.nasa.gov for 1,000 requests/hour. All space data is sourced from public NASA datasets.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with curiosity, depth, and care — because good projects deserve good documentation.*
