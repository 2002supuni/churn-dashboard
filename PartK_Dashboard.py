# ============================================================
# Part K — Dialog Churn Dashboard
# Built with Streamlit + Plotly
# ============================================================
# HOW TO RUN:
#   1. Make sure these 4 CSV files are in the same folder:
#      powerbi_customer.csv
#      powerbi_district.csv
#      powerbi_plan_tier.csv
#      powerbi_kpi.csv
#
#   2. Open terminal in that folder and run:
#      pip install streamlit plotly pandas
#      streamlit run PartK_Dashboard.py
#
#   3. Your browser will open automatically
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title  = "Dialog Churn Dashboard",
    page_icon   = "📊",
    layout      = "wide"
)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    customer = pd.read_csv("powerbi_customer.csv")
    district = pd.read_csv("powerbi_district.csv")
    plan     = pd.read_csv("powerbi_plan_tier.csv")
    kpi      = pd.read_csv("powerbi_kpi.csv")
    return customer, district, plan, kpi

customer, district, plan, kpi = load_data()

# Sort plan tier correctly Basic → Platinum
plan_order = {'Basic': 1, 'Silver': 2, 'Gold': 3, 'Platinum': 4}
plan['plan_order'] = plan['plan_tier'].map(plan_order)
plan = plan.sort_values('plan_order')


# ── Header ────────────────────────────────────────────────────
st.markdown(
    """
    <div style='background-color:#0066CC; padding:18px 24px;
                border-radius:10px; margin-bottom:20px;'>
        <h2 style='color:white; margin:0; font-size:22px;'>
            📊 Dialog Axiata — Customer Churn Dashboard
        </h2>
        <p style='color:#CCE0FF; margin:4px 0 0 0; font-size:13px;'>
            Weekly monitoring view for Head of Business Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ── Sidebar filter ────────────────────────────────────────────
st.sidebar.title("🔎 Filters")
st.sidebar.markdown("Use these to drill into specific segments.")

# Plan tier filter
plan_options = ['All'] + list(customer['plan_tier'].dropna().unique())
selected_plan = st.sidebar.selectbox("Plan Tier", plan_options)

# District filter
district_options = ['All'] + sorted(customer['district'].dropna().unique().tolist())
selected_district = st.sidebar.selectbox("District", district_options)

# Apply filters to customer table
filtered = customer.copy()
if selected_plan != 'All':
    filtered = filtered[filtered['plan_tier'] == selected_plan]
if selected_district != 'All':
    filtered = filtered[filtered['district'] == selected_district]

# Recalculate KPIs from filtered data
total_customers      = len(filtered)
total_churned        = filtered['churn_flag'].sum()
churn_rate_pct       = round(filtered['churn_flag'].mean() * 100, 1) if total_customers > 0 else 0
monthly_rev_lost     = filtered[filtered['churn_flag'] == 1]['monthly_arpu_lkr'].sum()
high_risk            = (filtered['churn_probability'] >= 0.65).sum()


# ── PANEL 1 — KPI Cards ───────────────────────────────────────
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label = "Total Customers",
        value = f"{total_customers:,}"
    )
with col2:
    overall_rate = kpi['overall_churn_rate_pct'].iloc[0]
    delta = round(churn_rate_pct - overall_rate, 1) if selected_plan != 'All' or selected_district != 'All' else None
    st.metric(
        label = "Churn Rate",
        value = f"{churn_rate_pct}%",
        delta = f"{delta}% vs overall" if delta is not None else None,
        delta_color = "inverse"
    )
with col3:
    st.metric(
        label = "Customers Churned",
        value = f"{total_churned:,}"
    )
with col4:
    st.metric(
        label = "Monthly Revenue Lost",
        value = f"LKR {monthly_rev_lost/1e6:.1f}M"
    )
with col5:
    st.metric(
        label = "High Risk Customers",
        value = f"{high_risk:,}",
        help  = "Customers with churn probability ≥ 65%"
    )

st.markdown("---")


# ── PANEL 2 — Churn by Plan Tier ─────────────────────────────
st.subheader("📋 Churn Rate by Plan Tier")

# Recalculate plan tier from filtered data
plan_filtered = (
    filtered.groupby('plan_tier')
    .agg(
        total_customers   = ('customer_id', 'count'),
        churned_customers = ('churn_flag', 'sum'),
        churn_rate        = ('churn_flag', 'mean'),
        avg_arpu          = ('monthly_arpu_lkr', 'mean'),
        total_arpu        = ('monthly_arpu_lkr', 'sum'),
    )
    .reset_index()
)
plan_filtered['churn_rate_pct']          = (plan_filtered['churn_rate'] * 100).round(1)
plan_filtered['monthly_revenue_at_risk'] = (plan_filtered['total_arpu'] * plan_filtered['churn_rate']).round(0)
plan_filtered['plan_order']              = plan_filtered['plan_tier'].map(plan_order)
plan_filtered = plan_filtered.sort_values('plan_order')

col_left, col_right = st.columns(2)

with col_left:
    # Bar chart — churn rate
    fig_plan = px.bar(
        plan_filtered,
        x     = 'plan_tier',
        y     = 'churn_rate_pct',
        color = 'churn_rate_pct',
        color_continuous_scale = 'RdYlGn_r',
        range_color = [15, 27],
        text  = 'churn_rate_pct',
        labels = {
            'plan_tier'     : 'Plan Tier',
            'churn_rate_pct': 'Churn Rate (%)'
        },
        title = 'Churn Rate % by Plan Tier'
    )
    fig_plan.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_plan.add_hline(
        y           = churn_rate_pct,
        line_dash   = "dash",
        line_color  = "black",
        annotation_text = f"Overall: {churn_rate_pct}%"
    )
    fig_plan.update_layout(
        coloraxis_showscale = False,
        yaxis_range         = [0, 30],
        plot_bgcolor        = 'white',
        height              = 350
    )
    st.plotly_chart(fig_plan, use_container_width=True)

with col_right:
    # Bar chart — revenue at risk by plan tier
    fig_rev_plan = px.bar(
        plan_filtered,
        x     = 'plan_tier',
        y     = 'monthly_revenue_at_risk',
        color = 'monthly_revenue_at_risk',
        color_continuous_scale = 'Reds',
        text  = plan_filtered['monthly_revenue_at_risk'].apply(lambda x: f'LKR {x/1e6:.2f}M'),
        labels = {
            'plan_tier'               : 'Plan Tier',
            'monthly_revenue_at_risk' : 'Revenue at Risk (LKR)'
        },
        title = 'Monthly Revenue at Risk by Plan Tier'
    )
    fig_rev_plan.update_traces(textposition='outside')
    fig_rev_plan.update_layout(
        coloraxis_showscale = False,
        plot_bgcolor        = 'white',
        height              = 350,
        yaxis_tickformat    = ','
    )
    st.plotly_chart(fig_rev_plan, use_container_width=True)

st.markdown("---")


# ── PANEL 3 — Churn by District ───────────────────────────────
st.subheader("🗺️ Churn by District — Top 10 by Revenue at Risk")

# Recalculate district from filtered data
district_filtered = (
    filtered.groupby('district')
    .agg(
        total_customers   = ('customer_id', 'count'),
        churned_customers = ('churn_flag', 'sum'),
        churn_rate        = ('churn_flag', 'mean'),
        avg_arpu          = ('monthly_arpu_lkr', 'mean'),
        total_arpu        = ('monthly_arpu_lkr', 'sum'),
    )
    .reset_index()
)
district_filtered['churn_rate_pct']          = (district_filtered['churn_rate'] * 100).round(1)
district_filtered['monthly_revenue_at_risk'] = (district_filtered['total_arpu'] * district_filtered['churn_rate']).round(0)
district_top10 = district_filtered.sort_values('monthly_revenue_at_risk', ascending=False).head(10)
district_top10 = district_top10.sort_values('monthly_revenue_at_risk', ascending=True)

col_l, col_r = st.columns(2)

with col_l:
    # Horizontal bar — revenue at risk
    fig_dist = px.bar(
        district_top10,
        x          = 'monthly_revenue_at_risk',
        y          = 'district',
        orientation = 'h',
        color      = 'monthly_revenue_at_risk',
        color_continuous_scale = 'Reds',
        text       = district_top10['monthly_revenue_at_risk'].apply(lambda x: f'LKR {x/1e6:.2f}M'),
        labels     = {
            'monthly_revenue_at_risk' : 'Revenue at Risk (LKR)',
            'district'                : 'District'
        },
        title      = 'Top 10 Districts — Monthly Revenue at Risk'
    )
    fig_dist.update_traces(textposition='outside')
    fig_dist.update_layout(
        coloraxis_showscale = False,
        plot_bgcolor        = 'white',
        height              = 420,
        xaxis_tickformat    = ','
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with col_r:
    # Churn rate by district
    district_rate = district_filtered.sort_values('churn_rate_pct', ascending=False).head(10)
    district_rate = district_rate.sort_values('churn_rate_pct', ascending=True)

    fig_dist_rate = px.bar(
        district_rate,
        x           = 'churn_rate_pct',
        y           = 'district',
        orientation = 'h',
        color       = 'churn_rate_pct',
        color_continuous_scale = 'RdYlGn_r',
        range_color = [17, 23],
        text        = 'churn_rate_pct',
        labels      = {
            'churn_rate_pct' : 'Churn Rate (%)',
            'district'       : 'District'
        },
        title       = 'Top 10 Districts — Churn Rate %'
    )
    fig_dist_rate.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_dist_rate.update_layout(
        coloraxis_showscale = False,
        plot_bgcolor        = 'white',
        height              = 420
    )
    st.plotly_chart(fig_dist_rate, use_container_width=True)

st.markdown("---")


# ── PANEL 4 — Revenue at Risk Treemap ────────────────────────
st.subheader("💰 Revenue at Risk — Full Overview")

col_tree, col_table = st.columns([3, 2])

with col_tree:
    # Treemap — bigger box = more revenue at risk
    treemap_data = district_filtered[district_filtered['monthly_revenue_at_risk'] > 0]
    fig_tree = px.treemap(
        treemap_data,
        path   = ['district'],
        values = 'monthly_revenue_at_risk',
        color  = 'churn_rate_pct',
        color_continuous_scale = 'RdYlGn_r',
        range_color = [17, 23],
        title  = 'Revenue at Risk by District\n(Box size = LKR at risk | Colour = Churn rate)',
        hover_data = {
            'churn_rate_pct'          : ':.1f',
            'total_customers'         : ':,',
            'monthly_revenue_at_risk' : ':,'
        }
    )
    fig_tree.update_layout(height=400, coloraxis_colorbar_title='Churn %')
    st.plotly_chart(fig_tree, use_container_width=True)

with col_table:
    # Summary table
    st.markdown("**District Summary Table**")
    display_df = district_filtered.sort_values(
        'monthly_revenue_at_risk', ascending=False
    )[['district', 'total_customers', 'churn_rate_pct', 'monthly_revenue_at_risk']].copy()

    display_df.columns = ['District', 'Customers', 'Churn %', 'Revenue at Risk (LKR)']
    display_df['Revenue at Risk (LKR)'] = display_df['Revenue at Risk (LKR)'].apply(
        lambda x: f"LKR {x:,.0f}"
    )
    display_df['Churn %'] = display_df['Churn %'].apply(lambda x: f"{x}%")
    display_df = display_df.reset_index(drop=True)

    st.dataframe(display_df, use_container_width=True, height=380)

st.markdown("---")


# ── PANEL 5 — Churn Risk Distribution ────────────────────────
st.subheader("⚠️ Customer Churn Risk Distribution")

col_hist, col_high = st.columns(2)

with col_hist:
    # Histogram of churn probabilities
    fig_hist = px.histogram(
        filtered,
        x      = 'churn_probability',
        color  = 'churn_label',
        nbins  = 40,
        color_discrete_map = {'Churned': '#d9534f', 'Retained': '#5cb85c'},
        labels = {'churn_probability': 'Churn Probability', 'churn_label': 'Status'},
        title  = 'Distribution of Churn Probabilities'
    )
    fig_hist.add_vline(
        x=0.65, line_dash="dash", line_color="black",
        annotation_text="High risk threshold (65%)"
    )
    fig_hist.update_layout(plot_bgcolor='white', height=320)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_high:
    # High risk customers table — top 20
    st.markdown("**Top 20 Highest Risk Customers**")
    high_risk_df = (
        filtered[filtered['churn_probability'] >= 0.65]
        .sort_values('churn_probability', ascending=False)
        .head(20)
        [['plan_tier', 'district', 'monthly_arpu_lkr', 'churn_probability', 'revenue_at_risk']]
        .copy()
    )
    # De-identify — hide actual customer IDs
    high_risk_df.insert(0, 'Rank', range(1, len(high_risk_df) + 1))
    high_risk_df.columns = ['Rank', 'Plan', 'District', 'ARPU (LKR)', 'Churn Prob', 'Rev at Risk']
    high_risk_df['Churn Prob']    = high_risk_df['Churn Prob'].apply(lambda x: f"{x:.1%}")
    high_risk_df['ARPU (LKR)']    = high_risk_df['ARPU (LKR)'].apply(lambda x: f"LKR {x:,.0f}")
    high_risk_df['Rev at Risk']   = high_risk_df['Rev at Risk'].apply(lambda x: f"LKR {x:,.0f}")
    high_risk_df = high_risk_df.reset_index(drop=True)
    st.dataframe(high_risk_df, use_container_width=True, height=320)

st.markdown("---")


# ── Footer ────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; color:#888; font-size:12px; padding:10px;'>
        Dialog Axiata PLC — Internal Analytics Dashboard |
        Data Analyst Selection Assessment — Part K |
        Audience: Head of Business Analytics (Weekly View)
    </div>
    """,
    unsafe_allow_html=True
)