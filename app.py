import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.engine import DataEngine
from src.intelligence import MarketIntelligence
import os

# 1. Configuração e Carga
st.set_page_config(page_title="Market Intelligence", layout="wide")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'MOCK_DATA.json')
engine = DataEngine(DATA_PATH)
df_raw = engine.load_data()

# --- SIDEBAR ---
st.sidebar.image("https://static.vecteezy.com/system/resources/thumbnails/026/847/626/small/flying-black-crow-isolated-png.png", width=80)
st.sidebar.title("Strategic Filters")

todas_marcas = sorted(df_raw['marca'].unique())
select_all = st.sidebar.checkbox("Select All Brands", value=True)
selected_marcas = st.sidebar.multiselect("Brands:", todas_marcas, default=todas_marcas if select_all else [])
selected_uf = st.sidebar.multiselect("Region (UF):", sorted(df_raw['uf'].unique()), default=df_raw['uf'].unique())
selected_days = st.sidebar.slider("Analysis Period:", 1, 31, (1, 31))

# Execução dos Filtros
df_filt = engine.apply_filters(df_raw, selected_marcas, selected_uf, selected_days)

if not df_filt.empty:
    st.title("🚗 Automotive Market Intelligence Portal")
    st.markdown(f"### Competitive Performance Analysis | December 2025")
    
    # --- KPIs ---
    k1, k2, k3, k4 = st.columns(4)
    v_gm = len(df_filt[df_filt['marca'] == 'Chevrolet'])
    k1.metric("Total Registrations", f"{len(df_filt):,}")
    k2.metric("Chevrolet Share", f"{(v_gm / len(df_filt) * 100):.2f}%")
    k3.metric("Market Leader", df_filt['marca'].mode()[0])
    k4.metric("Active States", len(df_filt['uf'].unique()))
    st.divider()

    # --- LINHA 1: RANKING E SPC ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🏆 Market Share Ranking")
        rank_df = MarketIntelligence.get_pareto_data(df_filt)
        fig_rank = px.bar(rank_df, x='vendas', y='marca', orientation='h', color='vendas', color_continuous_scale='Viridis')
        fig_rank.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_rank, use_container_width=True)

    with col_b:
        st.subheader("📈 Statistical Process Control (SPC)")
        v_dia, mean, std = MarketIntelligence.calculate_spc(df_filt)
        fig_spc = px.line(v_dia, x='dia_do_mes', y='vol', markers=True)
        for val, color, label in zip([mean, mean+3*std, mean-3*std], ["blue", "red", "red"], ["Mean", "UCL", "LCL"]):
            fig_spc.add_hline(y=val, line_dash="dot", line_color=color, annotation_text=label)
        st.plotly_chart(fig_spc, use_container_width=True)

    # --- LINHA 2: BOXPLOT E PARETO ---
    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("📦 Sales Consistency (Daily Volatility)")
        # Lógica de preenchimento de zeros para o BoxPlot (Consistência)
        dias_range = range(selected_days[0], selected_days[1] + 1)
        temp_idx = pd.MultiIndex.from_product([selected_marcas, dias_range], names=['marca', 'dia_do_mes']).to_frame(index=False)
        v_m_d = df_filt.groupby(['marca', 'dia_do_mes']).size().reset_index(name='vendas')
        df_box = temp_idx.merge(v_m_d, on=['marca', 'dia_do_mes'], how='left').fillna(0)
        st.plotly_chart(px.box(df_box, x='marca', y='vendas', color='marca', points="all"), use_container_width=True)

    with col_d:
        st.subheader("🎯 Market Concentration (Pareto)")
        fig_p = go.Figure([
            go.Bar(x=rank_df['marca'], y=rank_df['vendas'], name="Volume"),
            go.Scatter(x=rank_df['marca'], y=rank_df['acc_perc'], name="% Acc", yaxis="y2", line=dict(color="orange", width=3))
        ])
        fig_p.update_layout(yaxis2=dict(overlaying='y', side='right', range=[0, 105]), showlegend=False)
        st.plotly_chart(fig_p, use_container_width=True)

    # --- LINHA 3: DECISION LOGIC ---
    st.divider()
    st.subheader("🧠 Customer Decision Insights")
    rules = MarketIntelligence.get_decision_logic(df_filt)
    col_e, col_f = st.columns([1, 1.5])
    with col_e:
        if rules: st.code(rules)
    with col_f:
        st.info("A árvore de decisão identifica se o fator 'Dia' ou 'Região' tem maior peso na escolha da marca.")

    # --- FOOTER ---
    with st.expander("🗺️ Regional Density Heatmap"):
        uf_h = df_filt['uf'].value_counts(normalize=True).reset_index(name='Share %').rename(columns={'index': 'UF'})
        uf_h['Share %'] = (uf_h['Share %'] * 100).round(2)
        st.dataframe(uf_h.style.background_gradient(cmap='Blues'), use_container_width=True)

else:
    st.warning("Filtros sem correspondência.")