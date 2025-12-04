import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration de la page
st.set_page_config(
    page_title="Explorateur Jeux Olympiques",
    page_icon="🏅",
    layout="wide"
)

# Titre principal
st.title("Dashboard Historique des Jeux Olympiques (1896-2004)")

# Fonction de chargement des données avec cache pour la performance
@st.cache_data
def load_data():
    file_path = os.path.join('raw_data', 'olympics_1896_2004.csv')
    
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8', skiprows=5)
        # Nettoyage basique et gestion des types
        # On s'assure que les colonnes critiques existent, sinon on adapte
        # Hypothèse sur les noms de colonnes standards : Year, NOC, Sport, Sex, Medal, Name
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
        return None

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

# Application des filtres
# Si une liste est vide, on considère que l'utilisateur veut "Tout voir" (ou rien, ici on gère le cas vide)
if not selected_years:
    df_filtered = df[df['Year'].isin(years_list)]
else:
    df_filtered = df[df['Year'].isin(selected_years)]

if selected_noc:
    df_filtered = df_filtered[df_filtered['NOC'].isin(selected_noc)]

if selected_sports:
    df_filtered = df_filtered[df_filtered['Sport'].isin(selected_sports)]


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
        st.plotly_chart(fig_line, use_container_width=True)
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
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning(f"Colonne '{gender_col}' introuvable dans les données.")

# --- TABLEAU DE DONNÉES ---
st.markdown("---")
st.subheader("Données brutes filtrées")

with st.expander("Voir les détails des données"):
    st.dataframe(df_filtered, use_container_width=True)

# Footer
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: small; margin-top: 50px;'>
        Données olympiques 1896-2004 | Généré par Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)