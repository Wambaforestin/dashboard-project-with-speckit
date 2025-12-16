# Quickstart Guide: Dashboard Journalistique Olympique

**Feature**: 001-journalistic-dashboard  
**Audience**: Developers implementing the enhancement  
**Prerequisite**: Existing MVP dashboard in `app.py`

---

## Overview

This feature transforms the existing Olympic MVP dashboard by adding:
1. **Carte Mondiale** tab with choropleth map showing medal density by country
2. **Top Athlètes** tab with ranked table (top 10 athletes)
3. **Comparateur** tab with two-country timeline comparison
4. **CSV Export** button in sidebar for filtered data download
5. **Tab Navigation** using `st.tabs()` to organize all views

---

## Development Environment Setup

### 1. Activate Virtual Environment
```powershell
cd C:\Users\wamba\Desktop\python\test-project-speckit
.\test-speckit\Scripts\Activate.ps1
```

### 2. Verify Dependencies
```powershell
pip list | Select-String "streamlit|pandas|plotly"
# Expected: streamlit>=1.52.0, pandas>=2.3.3, plotly>=6.5.0
```

### 3. Run Current MVP (Baseline)
```powershell
streamlit run app.py
```
**Expected**: Dashboard loads with filters, KPIs, 4 existing charts, and data table

---

## Implementation Phases

### Phase 2A: Add Reference Data Constants

**File**: `app.py` (top of file, after imports)

**Action**: Add NOC mapping and world countries lists

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import io

# Theme colors (from .streamlit/config.toml)
THEME_PRIMARY = "#00897B"
THEME_BACKGROUND = "#E0F7FA"
THEME_SECONDARY_BG = "#B2EBF2"
THEME_TEXT = "#006064"
TEAL_SCALE = ["#E0F7FA", "#B2EBF2", "#80DEEA", "#4DD0E1", "#26C6DA", 
              "#00BCD4", "#00ACC1", "#0097A7", "#00838F", "#006064"]

# NOC to Country mapping (sample - expand to ~200 entries)
NOC_TO_COUNTRY = {
    "USA": "United States", "FRA": "France", "GER": "Germany",
    "URS": "Russia", "GBR": "United Kingdom", "CHN": "China",
    "JPN": "Japan", "ITA": "Italy", "CAN": "Canada", "AUS": "Australia",
    # ... add remaining 190+ mappings
}

# World countries for zero-medal display (sample)
WORLD_COUNTRIES = [
    "United States", "France", "Germany", "United Kingdom", "China",
    "Japan", "Italy", "Canada", "Australia", "Russia",
    # ... add remaining 185+ countries
]
```

**Deliverable**: Constants defined and accessible throughout `app.py`

---

### Phase 2B: Refactor Existing Code into Cached Functions

**Goal**: Extract data loading and filtering into reusable, cached functions

**Before** (existing MVP structure):
```python
# Data loading inline
data_path = os.path.join("raw_data", "olympics_1896_2004.csv")
df = pd.read_csv(data_path, skiprows=5, encoding='utf-8')

# Filters applied inline
if selected_years:
    df = df[df["Year"].isin(selected_years)]
# ... more filter logic
```

**After** (refactored with caching):
```python
@st.cache_data
def load_data() -> pd.DataFrame:
    """Load Olympics dataset from CSV.
    
    Returns:
        pd.DataFrame: Full Olympics dataset (1896-2004).
    
    Raises:
        FileNotFoundError: If CSV file not found.
    """
    data_path = os.path.join("raw_data", "olympics_1896_2004.csv")
    df = pd.read_csv(data_path, skiprows=5, encoding='utf-8')
    return df

def apply_filters(
    df: pd.DataFrame,
    year_filter: list[int],
    sport_filter: list[str],
    noc_filter: list[str]
) -> pd.DataFrame:
    """Apply user-selected filters to dataset.
    
    Args:
        df: Base Olympics DataFrame.
        year_filter: Selected years (empty = no filter).
        sport_filter: Selected sports (empty = no filter).
        noc_filter: Selected NOC codes (empty = no filter).
    
    Returns:
        pd.DataFrame: Filtered subset of input DataFrame.
    """
    filtered = df.copy()
    if year_filter:
        filtered = filtered[filtered["Year"].isin(year_filter)]
    if sport_filter:
        filtered = filtered[filtered["Sport"].isin(sport_filter)]
    if noc_filter:
        filtered = filtered[filtered["NOC"].isin(noc_filter)]
    return filtered

# Main app flow
df = load_data()
filtered_df = apply_filters(df, selected_years, selected_sports, selected_nocs)
```

**Deliverable**: `load_data()` and `apply_filters()` functions implemented

---

### Phase 2C: Implement Aggregation Functions

**File**: `app.py` (after filter functions)

**Action**: Add cached aggregation functions for each visualization

```python
@st.cache_data(ttl=600)
def aggregate_medals_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate medal counts by country for choropleth map.
    
    See contracts/functions.md for full specification.
    """
    # Implementation from data-model.md transformation logic
    df_medals = df.groupby("NOC")["Medal"].count().reset_index(name="Total_Medals")
    df_medals["Country"] = df_medals["NOC"].map(NOC_TO_COUNTRY)
    
    # Add medal breakdown
    medal_breakdown = df.groupby(["NOC", "Medal"]).size().unstack(fill_value=0)
    df_medals = df_medals.merge(medal_breakdown, on="NOC", how="left").fillna(0)
    
    # Pre-populate all countries with 0
    all_countries = pd.DataFrame({"Country": WORLD_COUNTRIES, "Total_Medals": 0})
    df_medals = pd.merge(all_countries, df_medals, on="Country", how="left").fillna(0)
    
    return df_medals

@st.cache_data(ttl=600)
def get_top_athletes(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Calculate top N athletes with Olympic tiebreaker.
    
    See contracts/functions.md for full specification.
    """
    # Implementation from data-model.md transformation logic
    df_athletes = df.groupby(["Athlete Name", "NOC"]).size().reset_index(name="Total")
    
    # Medal breakdown
    medal_breakdown = (
        df[df["Medal"].isin(["Gold", "Silver", "Bronze"])]
        .groupby(["Athlete Name", "NOC", "Medal"]).size().unstack(fill_value=0)
    )
    df_athletes = df_athletes.merge(medal_breakdown, on=["Athlete Name", "NOC"], how="left").fillna(0)
    
    # Olympic tiebreaker sort
    df_athletes = df_athletes.sort_values(
        by=["Total", "Gold", "Silver", "Bronze"],
        ascending=[False, False, False, False]
    ).head(limit).reset_index(drop=True)
    
    df_athletes["Rank"] = range(1, len(df_athletes) + 1)
    return df_athletes

@st.cache_data(ttl=600)
def get_country_comparison_data(
    df: pd.DataFrame, 
    country1: str, 
    country2: str
) -> pd.DataFrame:
    """Generate time-series comparison of two countries.
    
    See contracts/functions.md for full specification.
    """
    # Implementation from data-model.md transformation logic
    df_c1 = df[df["NOC"] == country1].groupby("Year")["Medal"].count().reset_index(name="Country1_Medals")
    df_c2 = df[df["NOC"] == country2].groupby("Year")["Medal"].count().reset_index(name="Country2_Medals")
    
    comparison = pd.merge(df_c1, df_c2, on="Year", how="outer").fillna(0).sort_values("Year")
    comparison["Country1_Name"] = NOC_TO_COUNTRY.get(country1, country1)
    comparison["Country2_Name"] = NOC_TO_COUNTRY.get(country2, country2)
    
    return comparison

def generate_csv_export(df: pd.DataFrame) -> tuple[str, str]:
    """Generate CSV export with timestamp filename.
    
    See contracts/functions.md for full specification.
    """
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_data = csv_buffer.getvalue()
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"olympics_filtered_{timestamp}.csv"
    
    return csv_data, filename
```

**Deliverable**: 4 aggregation functions + CSV export function implemented

---

### Phase 2D: Implement Visualization Functions

**File**: `app.py` (after aggregation functions)

**Action**: Add rendering functions for new visualizations

```python
def render_choropleth_map(df_map: pd.DataFrame) -> None:
    """Display choropleth map of medal distribution."""
    fig = px.choropleth(
        df_map,
        locations="Country",
        locationmode="country names",
        color="Total_Medals",
        hover_name="Country",
        hover_data={"Total_Medals": True, "Gold": True, "Silver": True, "Bronze": True},
        color_continuous_scale=TEAL_SCALE,
        labels={"Total_Medals": "Médailles"}
    )
    fig.update_layout(
        title="Distribution Mondiale des Médailles",
        geo=dict(showframe=False, showcoastlines=True)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_top_athletes_table(df_athletes: pd.DataFrame) -> None:
    """Display styled top athletes table."""
    if df_athletes.empty:
        st.info("Aucun athlète trouvé pour ces critères")
    else:
        st.dataframe(
            df_athletes[["Rank", "Athlete Name", "NOC", "Total", "Gold", "Silver", "Bronze"]],
            column_config={
                "Rank": "Rang",
                "Athlete Name": "Nom",
                "NOC": "Pays",
                "Total": "Total",
                "Gold": "🥇 Or",
                "Silver": "🥈 Argent",
                "Bronze": "🥉 Bronze"
            },
            hide_index=True
        )

def render_comparison_chart(
    df_comparison: pd.DataFrame, 
    country1: str, 
    country2: str
) -> None:
    """Display two-country comparison line chart."""
    fig = px.line(
        df_comparison,
        x="Year",
        y=["Country1_Medals", "Country2_Medals"],
        labels={"value": "Nombre de Médailles", "Year": "Année"},
        color_discrete_sequence=[THEME_PRIMARY, "#FF6F00"]
    )
    fig.update_layout(
        title=f"Comparaison: {NOC_TO_COUNTRY.get(country1, country1)} vs {NOC_TO_COUNTRY.get(country2, country2)}",
        legend_title="Pays"
    )
    st.plotly_chart(fig, use_container_width=True)
```

**Deliverable**: 3 rendering functions implemented

---

### Phase 2E: Restructure Main App with Tabs

**File**: `app.py` (main execution block)

**Before** (MVP linear layout):
```python
st.title("Dashboard Olympique")

# Filters
with st.sidebar:
    # ... filter widgets

# KPIs
col1, col2 = st.columns(2)
# ... KPIs

# Charts
st.plotly_chart(...)  # Evolution chart
st.plotly_chart(...)  # Gender pie chart
# ... more charts
```

**After** (tabbed layout):
```python
st.title("Dashboard Journalistique Olympique")

# Filters (unchanged, remain in sidebar)
with st.sidebar:
    st.header("Filtres")
    selected_years = st.multiselect("Année", options=sorted(df["Year"].unique()))
    selected_sports = st.multiselect("Sport", options=sorted(df["Sport"].unique()))
    selected_nocs = st.multiselect("Pays (NOC)", options=sorted(df["NOC"].unique()))
    
    # CSV Export button
    csv_data, csv_filename = generate_csv_export(filtered_df)
    st.download_button(
        label="📥 Télécharger les données (CSV)",
        data=csv_data,
        file_name=csv_filename,
        mime="text/csv"
    )

# Apply filters
filtered_df = apply_filters(df, selected_years, selected_sports, selected_nocs)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Vue d'ensemble",
    "🗺️ Carte Mondiale",
    "🏆 Top Athlètes",
    "⚖️ Comparateur"
])

with tab1:
    # Existing MVP content (KPIs, evolution chart, gender pie, etc.)
    st.header("Statistiques Générales")
    col1, col2 = st.columns(2)
    # ... existing MVP code

with tab2:
    st.header("Distribution Géographique des Médailles")
    df_map = aggregate_medals_by_country(filtered_df)
    render_choropleth_map(df_map)

with tab3:
    st.header("Top 10 des Athlètes")
    df_athletes = get_top_athletes(filtered_df, limit=10)
    render_top_athletes_table(df_athletes)

with tab4:
    st.header("Comparateur de Nations")
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Premier pays", options=sorted(df["NOC"].unique()), key="c1")
    with col2:
        country2 = st.selectbox("Deuxième pays", options=sorted(df["NOC"].unique()), key="c2")
    
    if country1 == country2:
        st.error("Veuillez sélectionner deux pays différents")
    elif country1 and country2:
        df_comparison = get_country_comparison_data(filtered_df, country1, country2)
        render_comparison_chart(df_comparison, country1, country2)
```

**Deliverable**: Main app restructured with 4 tabs + CSV export button

---

## Testing Checklist

### Acceptance Testing (Manual)

Use acceptance scenarios from `spec.md` to validate each user story:

**User Story 1 (Carte Mondiale)**:
- [ ] Map displays without filters → shows all medals 1896-2004
- [ ] Filter by year 2000-2004 → map updates to show only those years
- [ ] Hover over country → tooltip shows country name + medal count
- [ ] Countries with 0 medals → displayed in light gray with "0 médailles"

**User Story 2 (Top Athlètes)**:
- [ ] No filters → shows top 10 all-time athletes
- [ ] Filter by NOC "USA" → shows only USA athletes
- [ ] Filter by sport "Swimming" → shows only swimmers
- [ ] Athletes with tied totals → sorted by Gold, then Silver, then Bronze
- [ ] Table shows columns: Rank, Name, Country, Total, Gold, Silver, Bronze

**User Story 3 (Comparateur)**:
- [ ] Select USA + RUS → line chart with 2 lines (1896-2004)
- [ ] Apply sport filter → both lines update
- [ ] Hover over year → shows exact medal counts for both countries
- [ ] Select same country twice → error message displayed

**User Story 4 (Export CSV)**:
- [ ] Apply filters → click CSV button → file downloads with filtered data only
- [ ] No filters → click CSV button → full dataset downloads
- [ ] Open CSV in Excel → all 11 columns present
- [ ] Filename format: `olympics_filtered_YYYY-MM-DD_HHMMSS.csv`

**User Story 5 (Tabs)**:
- [ ] On load → 4 tabs visible horizontally
- [ ] Default tab → "Vue d'ensemble" active, shows MVP content
- [ ] Switch tabs → content changes instantly
- [ ] Apply filter on any tab → all tabs update consistently

### Performance Testing

Run with full dataset and measure:
- [ ] Initial load time: < 3 seconds (constitution requirement)
- [ ] Filter change response: < 500ms (constitution requirement)
- [ ] Map rendering: < 5 seconds (spec SC-001)
- [ ] Top athletes update: < 2 seconds (spec SC-002)
- [ ] Comparison chart: < 3 seconds (spec SC-003)
- [ ] CSV export: < 2 seconds for 10k rows (spec SC-004)

**Measurement**: Add timing decorators during dev, remove before merge

### Visual Consistency Testing

- [ ] All Plotly charts use teal color scale (TEAL_SCALE)
- [ ] Comparison chart uses primary teal + contrasting orange
- [ ] No hardcoded colors outside THEME_* constants
- [ ] Theme colors match `.streamlit/config.toml`

---

## Common Gotchas

### 1. NOC Code Mapping Incomplete
**Symptom**: Some countries missing from map  
**Fix**: Add missing NOC → Country mappings to `NOC_TO_COUNTRY` dict  
**Validation**: Run app, check console for "NOC code 'XYZ' not mapped" warnings

### 2. Cache Not Invalidating
**Symptom**: Filters applied but charts don't update  
**Fix**: Clear cache with `st.cache_data.clear()` or restart Streamlit server  
**Prevention**: Use correct cache keys (convert lists to tuples)

### 3. Plotly Map Shows Blank
**Symptom**: Choropleth renders but no countries colored  
**Fix**: Verify `locationmode="country names"` and Country column has full names (not NOC codes)  
**Debug**: Check `df_map["Country"].unique()` matches expected country names

### 4. Tiebreaker Not Working
**Symptom**: Athletes with same total sorted incorrectly  
**Fix**: Ensure sort includes all 4 columns: `["Total", "Gold", "Silver", "Bronze"]`  
**Test**: Manually verify top 2-3 athletes match Olympic tiebreaker rules

---

## Next Steps After Implementation

1. **Run acceptance tests** using checklist above
2. **Measure performance** against success criteria (SC-001 through SC-008)
3. **Update README.md** with new feature descriptions
4. **Re-run constitution check** (Phase 1 gate) to verify no regressions
5. **Generate task breakdown** with `/speckit.tasks` command for systematic implementation

---

**Quickstart Status**: ✅ **Complete**  
**Ready for**: Implementation (Phase 2) or Task Generation (`/speckit.tasks`)
