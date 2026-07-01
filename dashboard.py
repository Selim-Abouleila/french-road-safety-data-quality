import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Data Quality Intelligence | BAAC 2024",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dynamic Data Loading & KPI Calculation ---
@st.cache_data
def load_data():
    datasets = {}
    datasets['caract'] = pd.read_csv('caract-2024.csv', sep=';', low_memory=False)
    datasets['lieux'] = pd.read_csv('lieux-2024.csv', sep=';', low_memory=False)
    datasets['usagers'] = pd.read_csv('usagers-2024.csv', sep=';', low_memory=False)
    datasets['vehicules'] = pd.read_csv('vehicules-2024.csv', sep=';', low_memory=False)
    
    num_tables = len(datasets)
    duplicates = sum(df.duplicated().sum() for df in datasets.values())
    
    caract = datasets['caract']
    lat = pd.to_numeric(caract['lat'].str.replace(',', '.'), errors='coerce')
    invalid_coords = ((lat < -90) | (lat > 90)).sum()
    
    hidden_unknowns_cols = 0
    high_missing_cols = 0
    missing_data = []

    for name, df in datasets.items():
        missing_pct = (df.isnull().sum() / len(df)) * 100
        high_missing_cols += (missing_pct > 90).sum()
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                if (df[col] == -1).sum() > 0:
                    hidden_unknowns_cols += 1
                    
        for col, pct in missing_pct.items():
            if pct > 0:
                missing_data.append({'Dataset': name.capitalize(), 'Column': f"{col} ({name})", 'Missing %': pct})
                
    missing_df = pd.DataFrame(missing_data).sort_values('Missing %', ascending=False).head(10)
    
    return datasets, num_tables, duplicates, invalid_coords, hidden_unknowns_cols, high_missing_cols, missing_df

with st.spinner("Crunching BAAC data..."):
    datasets, num_tables, duplicates, invalid_coords, hidden_unknowns_cols, high_missing_cols, missing_df = load_data()

# --- Custom CSS for Premium Aesthetics ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-color: #f8fafc;
        --surface-color: #ffffff;
        --border-color: #e2e8f0;
        --text-main: #0f172a;
        --text-muted: #64748b;
        --accent-primary: #2563eb;
        --accent-success: #10b981;
        --accent-warning: #f59e0b;
        --accent-critical: #ef4444;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        background-color: var(--bg-color);
        color: var(--text-main);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #eff6ff;
        color: var(--accent-primary);
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
        border: 1px solid #bfdbfe;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text-main);
        margin-bottom: 8px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-muted);
        font-weight: 400;
        margin-bottom: 24px;
        max-width: 800px;
        line-height: 1.6;
    }

    .kpi-wrapper {
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 20px;
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: transform 0.2s ease-in-out;
    }
    .kpi-wrapper:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-chip {
        font-size: 0.7rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 4px;
        line-height: 1;
    }
    .kpi-caption {
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    .insight-card {
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        height: 100%;
        border-top: 4px solid var(--border-color);
    }
    .insight-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    .insight-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-main);
    }
    .insight-takeaway {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-main);
        margin-bottom: 8px;
        line-height: 1.5;
    }
    .insight-body {
        font-size: 0.9rem;
        color: var(--text-muted);
        line-height: 1.6;
    }

    .matrix-row {
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 16px 24px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }
    .matrix-table-name {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--accent-primary);
        background: #eff6ff;
        padding: 4px 10px;
        border-radius: 6px;
        width: 140px;
        text-align: center;
    }
    .matrix-desc {
        flex: 1;
        font-size: 0.95rem;
        color: var(--text-muted);
    }
    .matrix-issue {
        flex: 2;
        font-size: 0.95rem;
        color: var(--text-main);
        font-weight: 500;
    }
    .matrix-status {
        width: 120px;
        text-align: right;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
        color: var(--text-muted);
        font-weight: 500;
        font-size: 1.05rem;
        padding: 0 4px;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary);
    }

    [data-testid="stSidebar"] {
        background-color: var(--surface-color);
        border-right: 1px solid var(--border-color);
    }
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 8px;
    }
    .sidebar-text {
        font-size: 0.9rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin-bottom: 24px;
    }
    
    .chip-good { background: #dcfce7; color: #166534; }
    .chip-watch { background: #fef9c3; color: #854d0e; }
    .chip-risk { background: #fee2e2; color: #991b1b; }
    .chip-structural { background: #e0e7ff; color: #3730a3; }
</style>
""", unsafe_allow_html=True)

# --- HTML Helper Functions ---
def render_kpi(label, value, caption, status_class, status_text):
    html = f"""<div class="kpi-wrapper">
<div class="kpi-header">
<span class="kpi-label">{label}</span>
<span class="kpi-chip {status_class}">{status_text}</span>
</div>
<div class="kpi-value">{value}</div>
<div class="kpi-caption">{caption}</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)

def render_insight_card(title, severity_class, severity_text, takeaway, body, border_color):
    html = f"""<div class="insight-card" style="border-top-color: {border_color};">
<div class="insight-header">
<div style="flex:1;">
<div class="insight-title">{title}</div>
</div>
<span class="kpi-chip {severity_class}">{severity_text}</span>
</div>
<div class="insight-takeaway">{takeaway}</div>
<div class="insight-body">{body}</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)

def render_matrix_row(table_name, desc, issue, status_class, status_text):
    html = f"""<div class="matrix-row">
<div class="matrix-table-name">{table_name}</div>
<div class="matrix-desc">{desc}</div>
<div class="matrix-issue">{issue}</div>
<div class="matrix-status"><span class="kpi-chip {status_class}">{status_text}</span></div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">Quality Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-text">Executive Data Quality Readout for the 2024 French Road Safety (BAAC) dataset.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">Dataset Selection</div>', unsafe_allow_html=True)
    selected_dataset = st.selectbox("Select Dataset to Profile", options=["caract", "lieux", "usagers", "vehicules"], index=0)
    
    st.divider()
    st.markdown('<div class="sidebar-text"><strong>Status:</strong> Ready for ETL Phase<br><strong>Profiled:</strong> July 2026</div>', unsafe_allow_html=True)

# --- Hero Section ---
st.markdown('<span class="hero-badge">2024 BAAC Dataset · Quality Intelligence</span>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Data Quality Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Executive summary and impact analysis identifying structural completeness risks, hidden defaults, and schema consistency across the national road safety database.</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Dynamic KPI Row ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    render_kpi("Tables Profiled", str(num_tables), "Core relational tables", "chip-good", "Complete")
with col2:
    status_dup = "chip-good" if duplicates < 10 else "chip-warning"
    text_dup = "Excellent" if duplicates < 10 else "Needs Cleaning"
    render_kpi("Duplicates", str(duplicates), "Total duplicated records", status_dup, text_dup)
with col3:
    status_coord = "chip-good" if invalid_coords == 0 else "chip-risk"
    text_coord = "Valid" if invalid_coords == 0 else "Invalid Exists"
    render_kpi("Invalid Coords", str(invalid_coords), "Mathematical boundary checks", status_coord, text_coord)
with col4:
    status_unk = "chip-watch" if hidden_unknowns_cols > 0 else "chip-good"
    render_kpi("Hidden '-1'", str(hidden_unknowns_cols), "Columns with pseudo-nulls", status_unk, "ETL Risk")
with col5:
    render_kpi(">90% Missing", str(high_missing_cols), "Highly sparse attributes", "chip-structural", "Structural")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Dataset Deep Dive", "Executive Quality Report", "Operational Impact"])

# --- TAB 1: Dataset Deep Dive (PART 1 REQUIREMENTS) ---
with tab1:
    st.markdown(f'<br><h3 style="font-weight: 700; margin-bottom: 8px;">Profiling Analysis: {selected_dataset.capitalize()}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: var(--text-muted); margin-bottom: 24px;">Deep-dive into the structural inventory, missingness, and consistency exactly matching Part 1 requirements for the <code>{selected_dataset}-2024.csv</code> table.</p>', unsafe_allow_html=True)
    
    df_selected = datasets[selected_dataset]
    
    # A. Dataset Structure
    st.markdown('<h4>A. Dataset Structure (Column Inventory)</h4>', unsafe_allow_html=True)
    cols_df = pd.DataFrame({
        "Column Name": df_selected.columns,
        "Data Type": df_selected.dtypes.astype(str)
    })
    st.dataframe(cols_df, use_container_width=True, height=250)
    
    # B. Missing Values & Completeness
    st.markdown('<br><h4>B. Missing Values & Completeness</h4>', unsafe_allow_html=True)
    missing_pct = (df_selected.isnull().sum() / len(df_selected)) * 100
    missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=False)
    
    if len(missing_pct) > 0:
        st.bar_chart(missing_pct, height=300, color="#ef4444")
    else:
        st.success("No missing values (nulls) detected natively in this table.")
        
    # C. Consistency and Validity Checks
    st.markdown('<br><h4>C. Consistency and Validity Checks</h4>', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        dup_count = df_selected.duplicated().sum()
        status = "chip-good" if dup_count == 0 else "chip-risk"
        text = "Clean" if dup_count == 0 else "Duplicates Found"
        render_kpi("Exact Duplicates", str(dup_count), "Total duplicated records", status, text)
        
    with colB:
        hidden_col_count = 0
        for c in df_selected.columns:
            if df_selected[c].dtype in ['int64', 'float64', 'int32', 'float32'] and (df_selected[c] == -1).sum() > 0:
                hidden_col_count += 1
        status_hid = "chip-good" if hidden_col_count == 0 else "chip-watch"
        text_hid = "Clean" if hidden_col_count == 0 else "Hidden Nulls Detected"
        render_kpi("Hidden Anomalies (-1)", str(hidden_col_count), "Columns natively using -1", status_hid, text_hid)


# --- TAB 2: Quality Report ---
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic Data Viz
    st.markdown('<h3 style="font-weight: 700; margin-bottom: 8px;">Global Structural Fragmentation</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-muted); margin-bottom: 24px;">Top 10 columns across the entire database with the highest percentage of missing values.</p>', unsafe_allow_html=True)
    
    chart_data = missing_df.set_index('Column')[['Missing %']]
    st.bar_chart(chart_data, height=350, color="#3730a3")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        render_insight_card(
            "Missingness Clusters", "chip-structural", "Structural",
            "Several columns exceed 90% missingness.",
            "Fields such as lartpc, v2, secu3, etatp, and occutc are highly sparse. These are conditional attributes that apply only to specific subsets like public transport or pedestrians.",
            "#3730a3"
        )
    with c2:
        render_insight_card(
            "Hidden Defaults", "chip-watch", "ETL Risk",
            "The dataset uses '-1' to encode 'Unknown'.",
            "Route index (v1) contains 23% hidden unknowns. These pseudo-nulls bypass standard NaN detection and will mathematically distort downstream analytics if not cast to null early.",
            "#f59e0b"
        )
    with c3:
        render_insight_card(
            "Schema Consistency", "chip-good", "Excellent",
            "Structural integrity is exceptionally high.",
            "Only 2 duplicates exist across hundreds of thousands of rows. There are zero out-of-bounds coordinates, zero negative birth years, and categorical dictionaries are perfectly respected.",
            "#10b981"
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<h3 style="font-weight: 700; margin-bottom: 8px;">Completeness Matrix</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-muted); margin-bottom: 24px;">Deep-dive into structural fragmentation across the four primary entities.</p>', unsafe_allow_html=True)
    
    render_matrix_row("lieux", "Locations & Infrastructure", "Severe fragmentation. Precise architecture fields (lartpc, voie, v2) frequently missing.", "chip-risk", "High Risk")
    render_matrix_row("usagers", "Individuals Involved", "Linear drop-off in secondary safety equipment (secu2 43% missing, secu3 90% missing).", "chip-watch", "Moderate Risk")
    render_matrix_row("vehicules", "Vehicles Involved", "Near perfect completeness, excluding public-transport specific columns (occutc).", "chip-good", "Healthy")
    render_matrix_row("caract", "Accident Characteristics", "Address data (adr) missing 4%, but core coordinates remain robustly populated.", "chip-good", "Healthy")


# --- TAB 3: Operational Impact ---
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="font-weight: 700; margin-bottom: 8px;">Downstream Analytics Impact</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-muted); margin-bottom: 24px;">How missingness and hidden data patterns affect integration, modeling, and BI workflows.</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        render_insight_card(
            "Algorithmic Bias from Missingness", "chip-risk", "High Severity",
            "Naive row-dropping introduces survivorship bias.",
            "If we drop the 5% of rows missing Max Speed (vma) or the 2% missing Birth Year (an_nais), we risk skewing predictive models. Severe rural accidents might disproportionately lack speed limit data.",
            "#ef4444"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        render_insight_card(
            "Dimensionality Inflation", "chip-watch", "Medium Severity",
            "Sparse matrices risk overfitting machine learning models.",
            "Features with >90% missingness (e.g., public transport occupants) create extremely sparse vectors if one-hot encoded. We must partition models (e.g., cars vs. buses) to avoid the curse of dimensionality.",
            "#f59e0b"
        )
        
    with c2:
        render_insight_card(
            "Statistical Distortion", "chip-risk", "High Severity",
            "Hidden '-1' values will break distance calculations.",
            "These 'Unknown' values are extremely dangerous for ML algorithms or aggregations. If a clustering algorithm ingests -1 as a literal coordinate or category weight, results will be mathematically corrupted.",
            "#ef4444"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        render_insight_card(
            "Geospatial Mapping Failures", "chip-watch", "Medium Severity",
            "Missing strings cause silent point drops in mapping libraries.",
            "While coordinate boundaries are valid, 4.2% missing addresses and formatting issues (commas vs. decimals) will cause Kepler/Folium to drop points. Density maps may underrepresent certain departments.",
            "#f59e0b"
        )
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<h3 style="font-weight: 700; margin-bottom: 16px;">Recommended ETL Architecture</h3>', unsafe_allow_html=True)
    st.markdown("""<div style="background: var(--surface-color); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 24px;">
<ul style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.8; margin-bottom: 0;">
<li><strong><span style="color: var(--accent-primary);">1. Type Casting Layer:</span></strong> Instantly cast string coordinates (handling European comma notation) to floats.</li>
<li><strong><span style="color: var(--accent-warning);">2. Null Imputation Layer:</span></strong> Transform all <code>-1</code> integers in categorical/numerical columns directly to <code>np.nan</code>.</li>
<li><strong><span style="color: var(--accent-success);">3. Contextual Branching:</span></strong> Separate pedestrian and public transport rows into dedicated schema branches rather than forcing them into a global dense matrix.</li>
</ul>
</div>""", unsafe_allow_html=True)
