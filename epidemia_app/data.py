import pandas as pd
import streamlit as st
from sqlalchemy import inspect, text


def trouver_nom_colonne_infra(engine):
    """Détermine le nom exact de la colonne d'infrastructure dans la table infrastructures."""
    try:
        inspector = inspect(engine)
        colonnes = [c["name"] for c in inspector.get_columns("infrastructures")]
        candidats = ["nom_infrastructure", "nomInfra", "nom_infra", "nom_structure", "nom", "nom_est"]
        for colonne in candidats:
            if colonne in colonnes:
                return colonne
        return colonnes[1] if len(colonnes) > 1 else colonnes[0]
    except Exception:
        return "nom_infrastructure"


@st.cache_data(ttl=300)
def charger_provinces(_engine):
    """Charge dynamiquement la liste des provinces uniques depuis zonesante."""
    query = text("SELECT DISTINCT province FROM zonesante WHERE province IS NOT NULL AND TRIM(province) != '' ORDER BY province")
    with _engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df["province"].str.strip().dropna().unique().tolist()


@st.cache_data(ttl=300)
def charger_maladies(_engine):
    """Charge la table maladie complète."""
    query = text("SELECT * FROM maladie")
    with _engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df


@st.cache_data(ttl=300)
def charger_infrastructures_par_province(_engine, province_selectionnee):
    """Charge dynamiquement les infrastructures filtrées par la province choisie."""
    colonne_infra = trouver_nom_colonne_infra(_engine)
    query = text(f"""
        SELECT DISTINCT i.{colonne_infra} AS nom_infra
        FROM infrastructures i
        JOIN zonesante z ON i.idZone = z.idZone
        WHERE LOWER(TRIM(z.province)) = LOWER(TRIM(:prov))
          AND i.{colonne_infra} IS NOT NULL
          AND TRIM(i.{colonne_infra}) != ''
        ORDER BY i.{colonne_infra}
    """)
    with _engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"prov": province_selectionnee})
    return df["nom_infra"].str.strip().dropna().tolist()


@st.cache_data(ttl=300)
def charger_toutes_zones_infrastructures(_engine):
    """Charge les zones et infrastructures géolocalisées de toutes les provinces."""
    colonne_infra = trouver_nom_colonne_infra(_engine)
    query = text(f"""
        SELECT
            z.idZone,
            z.NomZone AS nomZone,
            z.province,
            z.population_2026,
            COALESCE(z.capacite_totale, 50) AS lits_reels,
            i.{colonne_infra} AS nom_infra_ref,
            i.latitude AS latitude_infra,
            i.longitude AS longitude_infra
        FROM zonesante z
        JOIN infrastructures i ON z.idZone = i.idZone
        WHERE i.latitude IS NOT NULL AND i.longitude IS NOT NULL
        GROUP BY z.idZone, z.NomZone, z.province, z.population_2026, z.capacite_totale
    """)
    with _engine.connect() as conn:
        df = pd.read_sql(query, conn)
    df["latitude_infra"] = pd.to_numeric(df["latitude_infra"], errors="coerce")
    df["longitude_infra"] = pd.to_numeric(df["longitude_infra"], errors="coerce")
    return df.dropna(subset=["latitude_infra", "longitude_infra"]).reset_index(drop=True)
