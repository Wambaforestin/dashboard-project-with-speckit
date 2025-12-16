# Function Contracts: Dashboard Journalistique Olympique

**Feature**: 001-journalistic-dashboard  
**Purpose**: Define input/output contracts for all data transformation and visualization functions

---

## Core Data Loading

### `load_data() -> pd.DataFrame`

**Purpose**: Load Olympics dataset from CSV with caching

**Input**: None

**Output**: 
```python
pd.DataFrame with columns:
    - Year: int
    - City: str
    - Sport: str
    - Discipline: str
    - Athlete Name: str
    - NOC: str
    - Gender: str
    - Event: str
    - Event Gender: str
    - Medal: str
    - Position: str
```

**Behavior**:
- Reads `raw_data/olympics_1896_2004.csv` with `skiprows=5`, `encoding='utf-8'`
- Caches result with `@st.cache_data` (invalidates on file modification only)
- Raises `FileNotFoundError` if CSV missing
- Logs warning if row count differs from expected ~30k rows

**Example**:
```python
df = load_data()
assert len(df) > 25000, "Dataset unexpectedly small"
assert "Athlete Name" in df.columns
```

---

## Filter Application

### `apply_filters(df: pd.DataFrame, year_filter: list[int], sport_filter: list[str], noc_filter: list[str]) -> pd.DataFrame`

**Purpose**: Apply user-selected filters to dataset

**Input**:
- `df`: Base Olympics DataFrame from `load_data()`
- `year_filter`: List of selected years (e.g., `[2000, 2004]`), empty list = no filter
- `sport_filter`: List of selected sports (e.g., `["Athletics", "Swimming"]`), empty = no filter
- `noc_filter`: List of selected NOC codes (e.g., `["USA", "FRA"]`), empty = no filter

**Output**: Filtered DataFrame (subset of input `df`)

**Behavior**:
- Returns copy of `df` (does not mutate original)
- If all filters empty, returns full dataset
- Filters are cumulative (AND logic)
- Preserves original column schema

**Example**:
```python
filtered = apply_filters(df, year_filter=[2000, 2004], sport_filter=[], noc_filter=["USA"])
# Returns only USA medals from 2000 and 2004, all sports
```

---

## Aggregations for Map

### `aggregate_medals_by_country(df: pd.DataFrame) -> pd.DataFrame`

**Purpose**: Aggregate medal counts by country for choropleth map

**Input**: Filtered Olympics DataFrame

**Output**:
```python
pd.DataFrame with columns:
    - NOC: str (3-letter code)
    - Country: str (full country name)
    - Total_Medals: int
    - Gold: int
    - Silver: int
    - Bronze: int
```

**Behavior**:
- Groups by NOC, counts total medals
- Maps NOC → Country using `NOC_TO_COUNTRY` dict
- Pre-populates all `WORLD_COUNTRIES` with 0 medals (for zero-medal display)
- Unmapped NOCs: logged warning, excluded from output
- **Cached** with `@st.cache_data(ttl=600)` by filter parameters

**Validation**:
- `Total_Medals == Gold + Silver + Bronze` (assertion)
- All countries in `WORLD_COUNTRIES` present (even if 0 medals)

**Example**:
```python
df_map = aggregate_medals_by_country(filtered_df)
assert "United States" in df_map["Country"].values
assert df_map[df_map["Country"] == "Monaco"]["Total_Medals"].iloc[0] >= 0
```

---

## Top Athletes Ranking

### `get_top_athletes(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame`

**Purpose**: Calculate top N athletes with Olympic tiebreaker

**Input**:
- `df`: Filtered Olympics DataFrame
- `limit`: Number of top athletes to return (default 10)

**Output**:
```python
pd.DataFrame with columns:
    - Rank: int (1 to limit)
    - Name: str (Athlete Name)
    - Country: str (NOC)
    - Total: int
    - Gold: int
    - Silver: int
    - Bronze: int
```

**Behavior**:
- Groups by `Athlete Name` + `NOC`, counts medals
- Sorts by `[Total DESC, Gold DESC, Silver DESC, Bronze DESC]`
- Takes top `limit` rows
- Adds `Rank` column (1-indexed)
- **Cached** with `@st.cache_data(ttl=600)` by filter parameters

**Edge Cases**:
- If dataset has <10 athletes, returns all available (partial list)
- If 0 athletes, returns empty DataFrame (caller displays "Aucun athlète trouvé")

**Validation**:
- `Total == Gold + Silver + Bronze` (assertion)
- Rank is sequential 1 to N (no gaps)

**Example**:
```python
top10 = get_top_athletes(filtered_df, limit=10)
assert len(top10) <= 10
assert top10.iloc[0]["Rank"] == 1
assert top10.iloc[0]["Total"] >= top10.iloc[1]["Total"]  # Tiebreaker validated
```

---

## Country Comparison

### `get_country_comparison_data(df: pd.DataFrame, country1: str, country2: str) -> pd.DataFrame`

**Purpose**: Generate time-series comparison of two countries

**Input**:
- `df`: Filtered Olympics DataFrame
- `country1`: NOC code (e.g., "USA")
- `country2`: NOC code (e.g., "RUS")

**Output**:
```python
pd.DataFrame with columns:
    - Year: int
    - Country1_Name: str (country1 full name)
    - Country1_Medals: int
    - Country2_Name: str (country2 full name)
    - Country2_Medals: int
```

**Behavior**:
- Groups by Year + NOC for each country
- Outer join on Year (includes years where one country has 0 medals)
- Fills missing years with 0 medals
- Sorts by Year ascending
- Maps NOC to country name for display
- **Cached** with `@st.cache_data(ttl=600)` by country1, country2, filters

**Edge Cases**:
- If `country1 == country2`: caller must validate before calling (return None or raise ValueError)
- If one country has no medals in any year, that country's line is all zeros

**Validation**:
- Years are sorted ascending
- Medal counts are non-negative integers

**Example**:
```python
comparison = get_country_comparison_data(filtered_df, "USA", "RUS")
assert "Year" in comparison.columns
assert comparison["Country1_Medals"].min() >= 0
assert len(comparison) > 0  # At least one Olympic year in range
```

---

## CSV Export

### `generate_csv_export(df: pd.DataFrame) -> tuple[str, str]`

**Purpose**: Generate CSV file content and filename for download

**Input**: Filtered Olympics DataFrame

**Output**: 
```python
(csv_data: str, filename: str)
    - csv_data: Full CSV content as string
    - filename: Timestamped filename (e.g., "olympics_filtered_2025-12-16_143052.csv")
```

**Behavior**:
- Converts DataFrame to CSV string using `to_csv(index=False, encoding='utf-8')`
- Generates filename with current timestamp (`datetime.now().strftime("%Y-%m-%d_%H%M%S")`)
- Does NOT cache (user-triggered, fresh timestamp each call)

**Edge Cases**:
- If `df` is empty (0 rows), returns CSV with headers only
- Caller should display warning when exporting empty dataset

**Example**:
```python
csv_content, filename = generate_csv_export(filtered_df)
assert filename.startswith("olympics_filtered_")
assert filename.endswith(".csv")
assert "Year,City,Sport" in csv_content  # Headers present
```

---

## Visualization Functions

### `render_choropleth_map(df_map: pd.DataFrame) -> None`

**Purpose**: Display choropleth map in Streamlit

**Input**: Aggregated medal data from `aggregate_medals_by_country()`

**Output**: None (renders chart via `st.plotly_chart()`)

**Behavior**:
- Creates `px.choropleth()` with `locationmode="country names"`
- Uses `color_continuous_scale=TEAL_SCALE`
- Custom hover template: shows Country, NOC, Total Medals
- Zero-medal countries display in light gray (lightest end of scale)
- Renders with `st.plotly_chart(fig, use_container_width=True)`

**Example**:
```python
df_map = aggregate_medals_by_country(filtered_df)
render_choropleth_map(df_map)
# User sees interactive world map in Streamlit
```

---

### `render_top_athletes_table(df_athletes: pd.DataFrame) -> None`

**Purpose**: Display styled top athletes table

**Input**: Top athletes DataFrame from `get_top_athletes()`

**Output**: None (renders table via `st.dataframe()` or `st.table()`)

**Behavior**:
- Displays DataFrame with columns: Rank, Name, Country, Total, Gold, Silver, Bronze
- If `df_athletes` is empty, displays `st.info("Aucun athlète trouvé pour ces critères")`
- Uses `st.dataframe()` for sortable table or `st.table()` for static styling
- Applies column width optimization for readability

**Example**:
```python
top10 = get_top_athletes(filtered_df)
render_top_athletes_table(top10)
# User sees ranked table of top 10 athletes
```

---

### `render_comparison_chart(df_comparison: pd.DataFrame, country1: str, country2: str) -> None`

**Purpose**: Display line chart comparing two countries over time

**Input**:
- `df_comparison`: Time-series data from `get_country_comparison_data()`
- `country1`: First country NOC (for labeling)
- `country2`: Second country NOC (for labeling)

**Output**: None (renders chart via `st.plotly_chart()`)

**Behavior**:
- Creates `px.line()` with two traces (one per country)
- Uses `color_discrete_sequence=[THEME_PRIMARY, "#FF6F00"]` for contrast
- X-axis: Year (1896-2004), Y-axis: Total Medals
- Custom hover: shows Year, Country Name, Medal Count
- Renders with `st.plotly_chart(fig, use_container_width=True)`

**Edge Cases**:
- If one country has all zeros, line is flat at bottom (valid visualization)

**Example**:
```python
comparison = get_country_comparison_data(filtered_df, "USA", "RUS")
render_comparison_chart(comparison, "USA", "RUS")
# User sees two-line chart with USA vs RUS medal trends
```

---

## Helper Functions

### `validate_noc_mapping() -> None`

**Purpose**: Log warnings for unmapped NOC codes at startup

**Input**: None (reads from `df` and `NOC_TO_COUNTRY`)

**Output**: None (logs warnings via `st.warning()`)

**Behavior**:
- Gets unique NOC codes from dataset
- Checks each against `NOC_TO_COUNTRY` dict
- Logs warning for unmapped NOCs: "NOC code 'XYZ' not mapped to country name"
- Runs once at application startup (not in critical path)

**Example**:
```python
validate_noc_mapping()
# Logs: "Warning: NOC code 'ZZZ' not mapped to country name"
```

---

## Contract Validation Rules

### Type Checking
- All function signatures include type hints (Python 3.10+ syntax)
- DataFrame columns validated at function entry (assert expected columns present)

### Caching Strategy
- Functions with `@st.cache_data`: `load_data`, `aggregate_medals_by_country`, `get_top_athletes`, `get_country_comparison_data`
- Functions without caching: `generate_csv_export` (user-triggered), rendering functions (display only)

### Error Handling
- File not found: Raise `FileNotFoundError` with clear message
- Invalid input: Raise `ValueError` with descriptive error
- Empty results: Return empty DataFrame or display user-friendly message (not error)

---

**Phase 1 Status**: ✅ **Contracts Complete**  
**Next**: Create quickstart guide for developers
