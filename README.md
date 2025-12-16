# Olympic Games Explorer - Dashboard Journalistique

A comprehensive Streamlit dashboard for exploring Olympic Games history (1896-2004) with interactive visualizations, athlete rankings, country comparisons, and data export capabilities.

`Project Aim`: This project serves as a testbed for `Speckit`, a GitHub tool that introduces a new `Specification-Driven Development` approach to coding.

## Features

### 📊 Vue d'ensemble
- Key performance indicators (KPIs) showing total athletes, medals, and medal breakdowns
- Medal evolution timeline chart
- Gender distribution analysis
- Top 10 countries and sports rankings
- Raw filtered data viewer

### 🗺️ Carte Mondiale
- Interactive choropleth world map showing medal distribution by country
- Color-coded visualization using teal color scale
- Hover tooltips with detailed medal breakdowns (Gold, Silver, Bronze)
- Zero-medal countries displayed in light gray
- Handles historical NOC codes (URS, GDR, etc.)

### 🏆 Top Athlètes
- Top 10 athletes ranked by total medals
- Olympic tiebreaker logic: Total → Gold → Silver → Bronze
- Detailed medal breakdown for each athlete
- Country information for each athlete

### ⚖️ Comparateur
- Side-by-side comparison of two countries
- Time-series visualization showing medal evolution (1896-2004)
- Dual-color line chart with contrasting colors
- Handles years where countries didn't win medals

### 📥 Export des Données
- CSV export button in sidebar
- Timestamped filenames (olympics_filtered_YYYY-MM-DD_HHMMSS.csv)
- Exports currently filtered data
- Warning when no data matches filters

## Technical Features

- **Performance Optimization**: Cached data loading and aggregations (@st.cache_data with 600s TTL)
- **Type Safety**: Full type hints using Python 3.10+ syntax
- **Responsive Design**: Tabbed interface for easy navigation
- **Filter Consistency**: Filters apply across all visualizations
- **Theme Consistency**: Teal color scheme throughout (#00897B primary)

## Project Structure

- `app.py`: Main application code.
- `raw_data/`: Contains the dataset (`olympics_1896_2004.csv`).
- `.streamlit/`: Custom theme configuration.

## Setup & Run

1. **Create and activate the environment:**

   ```powershell
   python -m venv test-specki
   .\test-specki\Scripts\Activate

2. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**

   ```powershell
   streamlit run app.py
   ```
