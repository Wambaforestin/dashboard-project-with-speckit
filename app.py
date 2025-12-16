import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from typing import Tuple

# Theme Constants (T001)
THEME_PRIMARY = "#00897B"  # Teal primary color
THEME_BACKGROUND = "#E0F7FA"  # Light teal background
THEME_SECONDARY_BG = "#B2DFDB"  # Secondary background
THEME_TEXT = "#004D40"  # Dark teal text
TEAL_SCALE = ["#E0F7FA", "#B2DFDB", "#80CBC4", "#4DB6AC", "#26A69A", "#009688", "#00897B", "#00796B", "#00695C", "#004D40"]

# NOC to Country Name Mapping (T002)
NOC_TO_COUNTRY = {
    "AHO": "Netherlands Antilles", "ALG": "Algeria", "ANZ": "Australasia", "ARG": "Argentina",
    "ARM": "Armenia", "AUS": "Australia", "AUT": "Austria", "AZE": "Azerbaijan",
    "BAH": "Bahamas", "BAR": "Barbados", "BDI": "Burundi", "BEL": "Belgium",
    "BER": "Bermuda", "BLR": "Belarus", "BOH": "Bohemia", "BRA": "Brazil",
    "BUL": "Bulgaria", "BWI": "West Indies Federation", "CAN": "Canada", "CHI": "Chile",
    "CHN": "China", "CIV": "Ivory Coast", "CMR": "Cameroon", "COL": "Colombia",
    "CRC": "Costa Rica", "CRO": "Croatia", "CUB": "Cuba", "CZE": "Czech Republic",
    "DEN": "Denmark", "DJI": "Djibouti", "DOM": "Dominican Republic", "ECU": "Ecuador",
    "EGY": "Egypt", "ERI": "Eritrea", "ESP": "Spain", "EST": "Estonia",
    "ETH": "Ethiopia", "EUA": "Germany", "EUN": "Unified Team", "FIN": "Finland",
    "FRA": "France", "FRG": "West Germany", "GBR": "United Kingdom", "GDR": "East Germany",
    "GEO": "Georgia", "GER": "Germany", "GHA": "Ghana", "GRE": "Greece",
    "GUY": "Guyana", "HAI": "Haiti", "HKG": "Hong Kong", "HUN": "Hungary",
    "INA": "Indonesia", "IND": "India", "IOP": "Independent Olympic Participants", "IRI": "Iran",
    "IRL": "Ireland", "IRQ": "Iraq", "ISL": "Iceland", "ISR": "Israel",
    "ISV": "Virgin Islands", "ITA": "Italy", "JAM": "Jamaica", "JPN": "Japan",
    "KAZ": "Kazakhstan", "KEN": "Kenya", "KGZ": "Kyrgyzstan", "KOR": "South Korea",
    "KSA": "Saudi Arabia", "KUW": "Kuwait", "LAT": "Latvia", "LIB": "Lebanon",
    "LTU": "Lithuania", "LUX": "Luxembourg", "MAR": "Morocco", "MAS": "Malaysia",
    "MDA": "Moldova", "MEX": "Mexico", "MGL": "Mongolia", "MKD": "North Macedonia",
    "MOZ": "Mozambique", "NAM": "Namibia", "NED": "Netherlands", "NGR": "Nigeria",
    "NIG": "Niger", "NOR": "Norway", "NZL": "New Zealand", "PAK": "Pakistan",
    "PAN": "Panama", "PAR": "Paraguay", "PER": "Peru", "PHI": "Philippines",
    "POL": "Poland", "POR": "Portugal", "PRK": "North Korea", "PUR": "Puerto Rico",
    "QAT": "Qatar", "ROU": "Romania", "RSA": "South Africa", "RU1": "Russian Empire",
    "RUS": "Russia", "SCG": "Serbia and Montenegro", "SEN": "Senegal", "SIN": "Singapore",
    "SLO": "Slovenia", "SRI": "Sri Lanka", "SUI": "Switzerland", "SUR": "Suriname",
    "SVK": "Slovakia", "SWE": "Sweden", "SYR": "Syria", "TAN": "Tanzania",
    "TCH": "Czechoslovakia", "TGA": "Tonga", "THA": "Thailand", "TPE": "Taiwan",
    "TRI": "Trinidad and Tobago", "TUN": "Tunisia", "TUR": "Turkey", "UAE": "United Arab Emirates",
    "UGA": "Uganda", "UKR": "Ukraine", "URS": "Soviet Union", "URU": "Uruguay",
    "USA": "United States", "UZB": "Uzbekistan", "VEN": "Venezuela", "VIE": "Vietnam",
    "YUG": "Yugoslavia", "ZAM": "Zambia", "ZIM": "Zimbabwe", "ZZX": "Mixed NOC"
}

# World Countries List for Zero-Medal Display (T003)
WORLD_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
    "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
    "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay",
    "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal",
    "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland",
    "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo",
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela",
    "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Configuration de la page
st.set_page_config(
    page_title="Explorateur Jeux Olympiques",
    page_icon="🏅",
    layout="wide"
)

# Titre principal
st.title("Dashboard Historique des Jeux Olympiques (1896-2004)")

# Fonction de chargement des données avec cache pour la performance (T004)
@st.cache_data
def load_data() -> pd.DataFrame | None:
    """
    Load Olympic dataset from CSV file with proper encoding and row skipping.
    
    Returns:
        pd.DataFrame | None: DataFrame with Olympic data, or None if file not found or error occurs
        
    Raises:
        None: Errors are caught and displayed via st.error
    """
    file_path = os.path.join('raw_data', 'olympics_1896_2004.csv')
    
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8', skiprows=5)
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
        return None


def apply_filters(
    df: pd.DataFrame,
    year_filter: list[int],
    sport_filter: list[str],
    noc_filter: list[str]
) -> pd.DataFrame:
    """
    Apply user-selected filters to the Olympic dataset.
    
    Args:
        df: Source DataFrame with Olympic data
        year_filter: List of years to include (empty list = all years)
        sport_filter: List of sports to include (empty list = all sports)
        noc_filter: List of NOC codes to include (empty list = all NOCs)
        
    Returns:
        pd.DataFrame: Filtered DataFrame based on selected criteria
    """
    filtered = df.copy()
    
    if year_filter:
        filtered = filtered[filtered['Year'].isin(year_filter)]
    
    if noc_filter:
        filtered = filtered[filtered['NOC'].isin(noc_filter)]
    
    if sport_filter:
        filtered = filtered[filtered['Sport'].isin(sport_filter)]
    
    return filtered


def generate_csv_export(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Generate CSV export data and filename with timestamp.
    
    Args:
        df: DataFrame to export
        
    Returns:
        Tuple[str, str]: (csv_data as string, filename with timestamp)
    """
    # Generate CSV data
    csv_data = df.to_csv(index=False, encoding='utf-8')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"olympics_filtered_{timestamp}.csv"
    
    return csv_data, filename


@st.cache_data(ttl=600)
def aggregate_medals_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate medal counts by country with NOC to country name mapping.
    Pre-populates all world countries with 0 medals for complete map visualization.
    
    Args:
        df: Source DataFrame with Olympic data
        
    Returns:
        pd.DataFrame: Aggregated data with columns [NOC, Country, Total_Medals, Gold, Silver, Bronze]
    """
    # Filter only medal rows
    medals_df = df[df['Medal'].notna()].copy()
    
    # Count medals by type for each NOC
    medal_counts = medals_df.groupby(['NOC', 'Medal']).size().unstack(fill_value=0)
    
    # Calculate total medals
    medal_counts['Total_Medals'] = medal_counts.sum(axis=1)
    
    # Ensure all medal columns exist
    for medal_type in ['Gold', 'Silver', 'Bronze']:
        if medal_type not in medal_counts.columns:
            medal_counts[medal_type] = 0
    
    # Reset index and map NOC to country names
    medal_counts = medal_counts.reset_index()
    medal_counts['Country'] = medal_counts['NOC'].map(NOC_TO_COUNTRY)
    
    # Log warnings for unmapped NOC codes (T021)
    unmapped = medal_counts[medal_counts['Country'].isna()]['NOC'].tolist()
    if unmapped:
        st.warning(f"⚠️ Codes NOC non mappés (exclus de la carte): {', '.join(unmapped)}")
    
    # Remove unmapped NOCs
    medal_counts = medal_counts[medal_counts['Country'].notna()]
    
    # Pre-populate all world countries with 0 medals (T019)
    all_countries = pd.DataFrame({'Country': WORLD_COUNTRIES})
    result = all_countries.merge(medal_counts, on='Country', how='left').fillna(0)
    
    # Convert medal counts to integers
    for col in ['Total_Medals', 'Gold', 'Silver', 'Bronze']:
        result[col] = result[col].astype(int)
    
    return result[['Country', 'Total_Medals', 'Gold', 'Silver', 'Bronze']]


def render_choropleth_map(df_map: pd.DataFrame) -> None:
    """
    Render interactive choropleth world map showing medal distribution by country.
    
    Args:
        df_map: Aggregated medal data by country
    """
    # Create choropleth map (T017, T020)
    fig = px.choropleth(
        df_map,
        locations="Country",
        locationmode="country names",
        color="Total_Medals",
        hover_name="Country",
        hover_data={
            "Country": False,
            "Total_Medals": True,
            "Gold": True,
            "Silver": True,
            "Bronze": True
        },
        color_continuous_scale=TEAL_SCALE,
        labels={
            "Total_Medals": "Total Médailles",
            "Gold": "🥇 Or",
            "Silver": "🥈 Argent",
            "Bronze": "🥉 Bronze"
        },
        title="Distribution Géographique des Médailles Olympiques"
    )
    
    # Customize hover template (T020)
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Total: %{customdata[0]} médailles<br>" +
                      "🥇 Or: %{customdata[1]}<br>" +
                      "🥈 Argent: %{customdata[2]}<br>" +
                      "🥉 Bronze: %{customdata[3]}<extra></extra>",
        customdata=df_map[['Total_Medals', 'Gold', 'Silver', 'Bronze']].values
    )
    
    # Update layout for better visualization
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data(ttl=600)
def get_top_athletes(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """
    Get top athletes ranked by total medals with Olympic tiebreaker logic.
    Tiebreaker: Total (desc) → Gold (desc) → Silver (desc) → Bronze (desc)
    
    Args:
        df: Source DataFrame with Olympic data
        limit: Number of top athletes to return (default: 10)
        
    Returns:
        pd.DataFrame: Top athletes with columns [Rank, Name, Country, Total, Gold, Silver, Bronze]
    """
    # Filter only medal rows
    medals_df = df[df['Medal'].notna()].copy()
    
    if medals_df.empty:
        return pd.DataFrame(columns=['Rank', 'Name', 'Country', 'Total', 'Gold', 'Silver', 'Bronze'])
    
    # Count medals by type for each athlete (T026)
    medal_counts = medals_df.groupby(['Athlete Name', 'NOC', 'Medal']).size().unstack(fill_value=0)
    
    # Calculate total medals
    medal_counts['Total'] = medal_counts.sum(axis=1)
    
    # Ensure all medal columns exist
    for medal_type in ['Gold', 'Silver', 'Bronze']:
        if medal_type not in medal_counts.columns:
            medal_counts[medal_type] = 0
    
    # Reset index
    medal_counts = medal_counts.reset_index()
    
    # Apply Olympic tiebreaker (T022)
    medal_counts = medal_counts.sort_values(
        by=['Total', 'Gold', 'Silver', 'Bronze'],
        ascending=[False, False, False, False]
    ).head(limit)
    
    # Add rank column
    medal_counts['Rank'] = range(1, len(medal_counts) + 1)
    
    # Map NOC to country names
    medal_counts['Country'] = medal_counts['NOC'].map(NOC_TO_COUNTRY).fillna(medal_counts['NOC'])
    
    # Rename and reorder columns
    result = medal_counts[['Rank', 'Athlete Name', 'Country', 'Total', 'Gold', 'Silver', 'Bronze']].copy()
    result.columns = ['Rank', 'Name', 'Country', 'Total', 'Gold', 'Silver', 'Bronze']
    
    return result


def render_top_athletes_table(df_athletes: pd.DataFrame) -> None:
    """
    Render styled table of top athletes with medal counts.
    
    Args:
        df_athletes: DataFrame with top athletes data
    """
    if df_athletes.empty:
        st.info("Aucun athlète trouvé pour ces critères")
        return
    
    # Configure columns with French headers (T023)
    st.dataframe(
        df_athletes,
        column_config={
            "Rank": st.column_config.NumberColumn("Rang", format="%d"),
            "Name": st.column_config.TextColumn("Nom"),
            "Country": st.column_config.TextColumn("Pays"),
            "Total": st.column_config.NumberColumn("Total", format="%d"),
            "Gold": st.column_config.NumberColumn("🥇 Or", format="%d"),
            "Silver": st.column_config.NumberColumn("🥈 Argent", format="%d"),
            "Bronze": st.column_config.NumberColumn("🥉 Bronze", format="%d")
        },
        hide_index=True,
        width="stretch"
    )


@st.cache_data(ttl=600)
def get_country_comparison_data(df: pd.DataFrame, country1_noc: str, country2_noc: str) -> pd.DataFrame:
    """
    Get time-series medal data for two countries for comparison.
    Uses outer join to include years where only one country won medals.
    
    Args:
        df: Source DataFrame with Olympic data
        country1_noc: NOC code for first country
        country2_noc: NOC code for second country
        
    Returns:
        pd.DataFrame: Time-series data with columns [Year, Country1_Name, Country1_Medals, Country2_Name, Country2_Medals]
    """
    # Filter medals for both countries
    medals_df = df[df['Medal'].notna()].copy()
    
    # Get country names
    country1_name = NOC_TO_COUNTRY.get(country1_noc, country1_noc)
    country2_name = NOC_TO_COUNTRY.get(country2_noc, country2_noc)
    
    # Count medals by year for each country
    country1_data = medals_df[medals_df['NOC'] == country1_noc].groupby('Year').size().reset_index(name='Medals')
    country2_data = medals_df[medals_df['NOC'] == country2_noc].groupby('Year').size().reset_index(name='Medals')
    
    # Outer join on Year to include all years (T033)
    comparison = country1_data.merge(country2_data, on='Year', how='outer', suffixes=('_1', '_2'))
    
    # Fill NaN with 0 for years where a country didn't win medals
    comparison = comparison.fillna(0)
    
    # Rename columns
    comparison.columns = ['Year', f'{country1_name}_Medals', f'{country2_name}_Medals']
    
    # Sort by year
    comparison = comparison.sort_values('Year')
    
    return comparison


def render_comparison_chart(df_comparison: pd.DataFrame, country1_noc: str, country2_noc: str) -> None:
    """
    Render line chart comparing medal evolution for two countries.
    
    Args:
        df_comparison: Time-series comparison data
        country1_noc: NOC code for first country
        country2_noc: NOC code for second country
    """
    if df_comparison.empty:
        st.info("Aucune donnée disponible pour la comparaison")
        return
    
    # Get country names
    country1_name = NOC_TO_COUNTRY.get(country1_noc, country1_noc)
    country2_name = NOC_TO_COUNTRY.get(country2_noc, country2_noc)
    
    # Reshape data for Plotly (T028)
    df_melted = df_comparison.melt(
        id_vars=['Year'],
        value_vars=[f'{country1_name}_Medals', f'{country2_name}_Medals'],
        var_name='Country',
        value_name='Medals'
    )
    
    # Clean country names (remove _Medals suffix)
    df_melted['Country'] = df_melted['Country'].str.replace('_Medals', '')
    
    # Create line chart with contrasting colors
    fig = px.line(
        df_melted,
        x='Year',
        y='Medals',
        color='Country',
        markers=True,
        title=f"Évolution des Médailles: {country1_name} vs {country2_name}",
        labels={'Medals': 'Nombre de médailles', 'Year': 'Année', 'Country': 'Pays'},
        color_discrete_sequence=[THEME_PRIMARY, "#FF6F00"]
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Chargement des données
df = load_data()

if df is None:
    st.warning("Le fichier 'olympics_1896_2004.csv' est introuvable dans le dossier 'raw_data'.")
    st.stop()

# --- SIDEBAR : FILTRES ---
st.sidebar.header("Filtres de recherche")

# 1. Filtre Année
years_list = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Sélectionner l'Année", years_list, default=years_list)

# 2. Filtre Pays (NOC)
noc_list = sorted(df['NOC'].unique())
selected_noc = st.sidebar.multiselect("Sélectionner le Pays (NOC)", noc_list, default=noc_list[:5]) # Par défaut les 5 premiers pour ne pas surcharger

# 3. Filtre Sport
sport_list = sorted(df['Sport'].unique())
selected_sports = st.sidebar.multiselect("Sélectionner le Sport", sport_list, default=sport_list)

# Application des filtres (T006)
df_filtered = apply_filters(df, selected_years, selected_sports, selected_noc)

# CSV Export Button (T014-T015)
st.sidebar.markdown("---")
st.sidebar.subheader("Export des données")

if df_filtered.empty:
    st.sidebar.warning("Aucune donnée ne correspond aux filtres appliqués")
else:
    csv_data, filename = generate_csv_export(df_filtered)
    st.sidebar.download_button(
        label="📥 Télécharger les données (CSV)",
        data=csv_data,
        file_name=filename,
        mime="text/csv"
    )


# --- KPIs (Indicateurs Clés) ---
st.markdown("Indicateurs Clés")

# Calculs
total_athletes = df_filtered['Athlete Name'].nunique()
medals_df = df_filtered[df_filtered['Medal'].notna()] # On ne garde que les lignes avec médailles
total_medals = len(medals_df)
gold_medals = len(medals_df[medals_df['Medal'] == 'Gold'])
silver_medals = len(medals_df[medals_df['Medal'] == 'Silver'])
bronze_medals = len(medals_df[medals_df['Medal'] == 'Bronze'])

# Affichage en colonnes
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Athlètes Uniques", total_athletes)
col2.metric("Total Médailles", total_medals)
col3.metric("🥇 Or", gold_medals)
col4.metric("🥈 Argent", silver_medals)
col5.metric("🥉 Bronze", bronze_medals)

st.markdown("---")

# --- TABBED INTERFACE (T007-T012) ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'ensemble", "🗺️ Carte Mondiale", "🏆 Top Athlètes", "⚖️ Comparateur"])

# Tab 1: Vue d'ensemble (T008 - existing MVP content)
with tab1:
    # --- GRAPHIQUES ---

    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("Évolution des médailles par an")
        
        # Préparation des données pour le line chart
        medals_by_year = medals_df.groupby('Year').size().reset_index(name='Count')
        
        if not medals_by_year.empty:
            fig_line = px.line(
                medals_by_year, 
                x='Year', 
                y='Count', 
                markers=True,
                title="Nombre de médailles distribuées au fil du temps",
                labels={'Count': 'Nombre de médailles', 'Year': 'Année'},
                color_discrete_sequence=["#D4AF37"] # Ligne couleur Or
            )
            # Mise à jour du fond du graphique pour qu'il soit transparent
            fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_line, width="stretch")
        else:
            st.info("Pas assez de données pour afficher l'évolution temporelle.")

    with col_chart2:
        st.subheader("Répartition Hommes/Femmes")
        
        # Utilisation de 'Gender' au lieu de 'Sex'
        gender_col = 'Gender' if 'Gender' in df_filtered.columns else 'Sex'
        
        if gender_col in df_filtered.columns:
            gender_counts = df_filtered[gender_col].value_counts().reset_index()
            # Renommer les colonnes pour Plotly
            gender_counts.columns = [gender_col, 'Count']
            
            fig_pie = px.pie(
                gender_counts, 
                values='Count', 
                names=gender_col, 
                title="Répartition par Genre",
                color_discrete_sequence=px.colors.qualitative.Bold # Couleurs vives
            )
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, width="stretch")
        else:
            st.warning(f"Colonne '{gender_col}' introuvable dans les données.")

    # --- NOUVEAUX GRAPHIQUES ---
    st.markdown("---")
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.subheader("Top 10 Pays par Médailles")
        # Group by NOC and count medals
        medals_by_country = medals_df['NOC'].value_counts().reset_index()
        medals_by_country.columns = ['NOC', 'Count']
        top_10_countries = medals_by_country.head(10)
        
        if not top_10_countries.empty:
            fig_bar_country = px.bar(
                top_10_countries,
                x='NOC',
                y='Count',
                title="Top 10 Pays (Médailles)",
                labels={'Count': 'Nombre de médailles', 'NOC': 'Pays'},
                color='Count',
                color_continuous_scale='Viridis'
            )
            fig_bar_country.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar_country, width="stretch")
        else:
            st.info("Pas assez de données pour afficher le classement par pays.")

    with col_chart4:
        st.subheader("Top 10 Sports par Médailles")
        # Group by Sport and count medals
        medals_by_sport = medals_df['Sport'].value_counts().reset_index()
        medals_by_sport.columns = ['Sport', 'Count']
        top_10_sports = medals_by_sport.head(10)
        
        if not top_10_sports.empty:
            fig_bar_sport = px.bar(
                top_10_sports,
                x='Count',
                y='Sport',
                orientation='h',
                title="Top 10 Sports (Médailles)",
                labels={'Count': 'Nombre de médailles', 'Sport': 'Sport'},
                color='Count',
                color_continuous_scale='Plasma'
            )
            fig_bar_sport.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar_sport, width="stretch")
        else:
            st.info("Pas assez de données pour afficher le classement par sport.")

    # --- TABLEAU DE DONNÉES ---
    st.markdown("---")
    st.subheader("Données brutes filtrées")

    with st.expander("Voir les détails des données"):
        st.dataframe(df_filtered, width="stretch")

# Tab 2: Carte Mondiale (T009, T018)
with tab2:
    st.header("Distribution Géographique des Médailles")
    
    # Aggregate medals by country and render map
    df_map = aggregate_medals_by_country(df_filtered)
    render_choropleth_map(df_map)

# Tab 3: Top Athlètes (T010, T024-T025)
with tab3:
    st.header("Top 10 des Athlètes")
    
    # Get top athletes and render table
    df_athletes = get_top_athletes(df_filtered, limit=10)
    render_top_athletes_table(df_athletes)

# Tab 4: Comparateur (T011, T029-T032)
with tab4:
    st.header("Comparateur de Nations")
    
    # Country selection widgets (T029)
    col1, col2 = st.columns(2)
    
    # Get sorted list of NOCs with country names
    noc_options = sorted(df['NOC'].unique().tolist())
    
    with col1:
        country1 = st.selectbox(
            "Sélectionner le premier pays",
            options=noc_options,
            format_func=lambda x: f"{x} - {NOC_TO_COUNTRY.get(x, x)}",
            key="country1"
        )
    
    with col2:
        country2 = st.selectbox(
            "Sélectionner le deuxième pays",
            options=noc_options,
            format_func=lambda x: f"{x} - {NOC_TO_COUNTRY.get(x, x)}",
            index=1 if len(noc_options) > 1 else 0,
            key="country2"
        )
    
    # Validation and rendering (T030-T032)
    if not country1 or not country2:
        st.info("🔍 Veuillez sélectionner deux pays pour commencer la comparaison")
    elif country1 == country2:
        st.error("❌ Veuillez sélectionner deux pays différents")
    else:
        # Get comparison data and render chart (T031)
        df_comparison = get_country_comparison_data(df_filtered, country1, country2)
        render_comparison_chart(df_comparison, country1, country2)

# Footer
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: small; margin-top: 50px;'>
        Données olympiques 1896-2004 | Généré par Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)