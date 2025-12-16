# Data Model: Dashboard Journalistique Olympique

**Feature**: 001-journalistic-dashboard  
**Phase**: 1 (Design)  
**Date**: 2025-12-16  
**Source Dataset**: `raw_data/olympics_1896_2004.csv`

---

## Source Data Schema

### Olympics Dataset (CSV)
**Location**: `raw_data/olympics_1896_2004.csv`  
**Format**: CSV with 5 header rows (skip with `skiprows=5`)  
**Size**: ~30,000 rows (1896-2004)  
**Encoding**: UTF-8

| Column Name | Type | Description | Sample Values |
|-------------|------|-------------|---------------|
| `Year` | int | Olympic year | 1896, 1900, 1904, ..., 2004 |
| `City` | str | Host city | "Athens", "Paris", "Beijing" |
| `Sport` | str | Sport category | "Athletics", "Swimming", "Gymnastics" |
| `Discipline` | str | Specific discipline | "100m", "Freestyle", "Vault" |
| `Athlete Name` | str | Full athlete name | "Michael Phelps", "Usain Bolt" |
| `NOC` | str | 3-letter country code | "USA", "FRA", "URS", "GER" |
| `Gender` | str | Athlete gender | "Men", "Women" |
| `Event` | str | Specific event | "100m Men", "200m Freestyle Women" |
| `Event Gender` | str | Event category | "M", "W", "X" (mixed) |
| `Medal` | str | Medal type | "Gold", "Silver", "Bronze" |
| `Position` | str/int | Finishing position | "1", "2", "3", "4", etc. |

**Data Quality Notes**:
- Historical NOC codes (e.g., "URS", "GDR", "TCH") preserved as-is (no modern fusion)
- Some athletes have multiple medal entries (one per event)
- Medal column contains only medalists (no non-medalists in dataset)

---

## Derived Data Models

### 1. Medal Country Aggregation

**Purpose**: Support choropleth map visualization (FR-001, FR-002)  
**Source**: Olympics Dataset grouped by NOC  
**Computed By**: `aggregate_medals_by_country()` function

**Schema**:
```python
{
    "NOC": str,              # 3-letter country code (e.g., "USA")
    "Country": str,          # Full country name (e.g., "United States")
    "Total_Medals": int,     # Total medal count
    "Gold": int,             # Gold medal count
    "Silver": int,           # Silver medal count
    "Bronze": int            # Bronze medal count
}
```

**Transformation Logic**:
```python
# Step 1: Group by NOC and count medals
df_medals = filtered_df.groupby("NOC")["Medal"].count().reset_index()
df_medals.columns = ["NOC", "Total_Medals"]

# Step 2: Map NOC to country name for Plotly
df_medals["Country"] = df_medals["NOC"].map(NOC_TO_COUNTRY)

# Step 3: Calculate medal breakdown
medal_breakdown = filtered_df.groupby(["NOC", "Medal"]).size().unstack(fill_value=0)
df_medals = df_medals.merge(medal_breakdown, on="NOC", how="left")

# Step 4: Add zero-medal countries
all_countries = pd.DataFrame({"Country": WORLD_COUNTRIES, "Total_Medals": 0})
df_medals = pd.merge(all_countries, df_medals, on="Country", how="left").fillna(0)
```

**Validation Rules**:
- `Total_Medals` must equal `Gold + Silver + Bronze`
- `Country` must not be null (unmapped NOCs trigger warning)
- All WORLD_COUNTRIES must be present (for zero-medal display)

**Cached**: ✅ Yes (by year, sport, noc filters)

---

### 2. Top Athlete Ranking

**Purpose**: Support Top 10 athletes table (FR-003, FR-004)  
**Source**: Olympics Dataset grouped by Athlete Name + NOC  
**Computed By**: `get_top_athletes()` function

**Schema**:
```python
{
    "Rank": int,             # Position (1-10)
    "Name": str,             # Athlete full name
    "Country": str,          # NOC code
    "Total": int,            # Total medal count
    "Gold": int,             # Gold medal count
    "Silver": int,           # Silver medal count
    "Bronze": int            # Bronze medal count
}
```

**Transformation Logic**:
```python
# Step 1: Count total medals per athlete
df_athletes = filtered_df.groupby(["Athlete Name", "NOC"]).size().reset_index(name="Total")

# Step 2: Calculate medal breakdown
medal_breakdown = (
    filtered_df[filtered_df["Medal"].isin(["Gold", "Silver", "Bronze"])]
    .groupby(["Athlete Name", "NOC", "Medal"])
    .size()
    .unstack(fill_value=0)
)
df_athletes = df_athletes.merge(medal_breakdown, on=["Athlete Name", "NOC"], how="left").fillna(0)

# Step 3: Apply Olympic tiebreaker (Total DESC, Gold DESC, Silver DESC, Bronze DESC)
df_athletes = df_athletes.sort_values(
    by=["Total", "Gold", "Silver", "Bronze"],
    ascending=[False, False, False, False]
).head(10).reset_index(drop=True)

# Step 4: Add rank column
df_athletes["Rank"] = range(1, len(df_athletes) + 1)
```

**Validation Rules**:
- Rank must be sequential 1-10 (or fewer if <10 athletes match filters)
- `Total` must equal `Gold + Silver + Bronze`
- Tiebreaker order: Total → Gold → Silver → Bronze (all descending)

**Edge Case Handling**:
- If fewer than 10 athletes match filters, display all available
- If 0 athletes match, display "Aucun athlète trouvé pour ces critères" (FR-013)

**Cached**: ✅ Yes (by year, sport, noc filters)

---

### 3. Country Comparison Time Series

**Purpose**: Support two-country comparison chart (FR-005, FR-006)  
**Source**: Olympics Dataset grouped by Year + NOC  
**Computed By**: `get_country_comparison_data()` function

**Schema**:
```python
{
    "Year": int,             # Olympic year (1896-2004)
    "Country1_Medals": int,  # Total medals for first country
    "Country2_Medals": int   # Total medals for second country
}
```

**Transformation Logic**:
```python
# Step 1: Filter for selected countries
df_c1 = filtered_df[filtered_df["NOC"] == country1].groupby("Year")["Medal"].count().reset_index()
df_c1.columns = ["Year", "Country1_Medals"]

df_c2 = filtered_df[filtered_df["NOC"] == country2].groupby("Year")["Medal"].count().reset_index()
df_c2.columns = ["Year", "Country2_Medals"]

# Step 2: Merge on Year (outer join to include years where one country has 0 medals)
df_comparison = pd.merge(df_c1, df_c2, on="Year", how="outer").fillna(0)

# Step 3: Sort by Year
df_comparison = df_comparison.sort_values("Year")
```

**Validation Rules**:
- Years must span full dataset range (1896-2004) where countries participated
- Medal counts must be non-negative integers
- Missing years (no medals for either country) should show 0, not null

**Edge Case Handling**:
- If `country1 == country2`, display error message (spec requirement)
- If one country has no medals in any year, show flat zero line

**Cached**: ✅ Yes (by country1, country2, year, sport, noc filters)

---

### 4. Filtered Dataset Export

**Purpose**: Support CSV download (FR-007, FR-008)  
**Source**: Direct filter application on Olympics Dataset  
**Computed By**: `generate_csv_export()` function

**Schema**: Same as source Olympics Dataset (all 11 columns preserved)

**Transformation Logic**:
```python
# Apply filters
export_df = df.copy()
if year_filter:
    export_df = export_df[export_df["Year"].isin(year_filter)]
if sport_filter:
    export_df = export_df[export_df["Sport"].isin(sport_filter)]
if noc_filter:
    export_df = export_df[export_df["NOC"].isin(noc_filter)]

# Convert to CSV string
csv_buffer = io.StringIO()
export_df.to_csv(csv_buffer, index=False, encoding="utf-8")
csv_data = csv_buffer.getvalue()
```

**Validation Rules**:
- Must contain all 11 source columns in original order
- Encoding must be UTF-8
- No index column in CSV output
- Filename format: `olympics_filtered_YYYY-MM-DD_HHMMSS.csv`

**Edge Case Handling**:
- If filters result in 0 rows, export CSV with headers only
- Display warning: "Aucune donnée ne correspond aux filtres appliqués"

**Cached**: ❌ No (export is user-triggered, not pre-computed)

---

## Entity Relationships

```text
Olympics Dataset (Source)
    │
    ├──> Medal Country Aggregation (grouped by NOC)
    │       └──> Choropleth Map Visualization
    │
    ├──> Top Athlete Ranking (grouped by Athlete Name + NOC)
    │       └──> Top 10 Athletes Table
    │
    ├──> Country Comparison Time Series (grouped by Year + NOC for 2 countries)
    │       └──> Comparison Line Chart
    │
    └──> Filtered Dataset Export (direct filter, no aggregation)
            └──> CSV Download
```

**Data Flow**:
1. `load_data()` loads raw CSV → cached base DataFrame
2. User applies filters via sidebar → creates `filtered_df`
3. Each tab calls aggregation function with `filtered_df` → cached results
4. Visualizations render using aggregated data

---

## Reference Data

### NOC to Country Name Mapping (Sample)

**Full mapping in `app.py` as `NOC_TO_COUNTRY` dictionary (~200 entries)**

| NOC | Country Name |
|-----|--------------|
| USA | United States |
| FRA | France |
| GER | Germany |
| URS | Russia |
| GBR | United Kingdom |
| CHN | China |
| JPN | Japan |
| ITA | Italy |
| CAN | Canada |
| AUS | Australia |
| ... | ... |

**Source**: Manual curation based on dataset NOC codes  
**Maintenance**: Add mappings as needed when new NOCs discovered  
**Edge Case**: Unmapped NOCs logged as warning, excluded from map

---

### World Countries List

**Purpose**: Pre-populate choropleth with all countries for zero-medal display  
**Location**: `WORLD_COUNTRIES` constant in `app.py` (~195 entries)

**Sample**:
```python
WORLD_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "United States", 
    "France", "Germany", "United Kingdom", "China", ...
]
```

**Source**: Standard world country list (ISO 3166)  
**Maintenance**: Static list (countries rarely change)

---

## Data Validation Strategy

### Load-Time Validation
- ✅ Verify CSV has expected 11 columns
- ✅ Check no critical columns are fully null (Year, Athlete Name, NOC, Medal)
- ✅ Log warning if dataset size differs significantly from expected ~30k rows

### Runtime Validation
- ✅ Ensure aggregations produce non-negative medal counts
- ✅ Verify tiebreaker logic maintains sort order (Total DESC, Gold DESC, ...)
- ✅ Confirm filtered datasets never exceed source dataset size

### User-Facing Validation
- ✅ Display "Aucun athlète trouvé" when athlete query returns 0 results
- ✅ Show "Veuillez sélectionner deux pays différents" when country1 == country2
- ✅ Warn when CSV export contains 0 rows

---

**Phase 1 Status**: ✅ **Data Model Complete**  
**Next**: Create API contracts and quickstart guide
