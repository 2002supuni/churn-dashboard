import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title = "Dialog Churn Dashboard",
    page_icon  = "📊",
    layout     = "wide"
)

# ── All data hardcoded — no CSV files needed ──────────────────
@st.cache_data
def load_data():

    kpi = {
        'total_customers'     : 50000,
        'total_churned'       : 10298,
        'churn_rate_pct'      : 20.6,
        'monthly_revenue_lost': 28370629,
        'annual_revenue_lost' : 340447553,
        'avg_arpu'            : 2738,
        'high_risk_customers' : 5638,
    }

    plan = pd.DataFrame([
        {'plan_tier':'Basic',    'total_customers':20935, 'churned_customers':4657, 'churn_rate_pct':22.2, 'avg_arpu':1200, 'monthly_revenue_at_risk':5587284,  'plan_order':1},
        {'plan_tier':'Silver',   'total_customers':15177, 'churned_customers':2761, 'churn_rate_pct':18.2, 'avg_arpu':2398, 'monthly_revenue_at_risk':6619581,  'plan_order':2},
        {'plan_tier':'Gold',     'total_customers':9904,  'churned_customers':1920, 'churn_rate_pct':19.4, 'avg_arpu':4204, 'monthly_revenue_at_risk':8072553,  'plan_order':3},
        {'plan_tier':'Platinum', 'total_customers':3984,  'churned_customers':960,  'churn_rate_pct':24.1, 'avg_arpu':8476, 'monthly_revenue_at_risk':8137089,  'plan_order':4},
    ])

    district = pd.DataFrame([
        {'district':'Ampara',       'total_customers':1601,  'churned_customers':312,  'churn_rate_pct':19.5, 'monthly_revenue_at_risk':862124},
        {'district':'Anuradhapura', 'total_customers':2248,  'churned_customers':483,  'churn_rate_pct':21.5, 'monthly_revenue_at_risk':1335890},
        {'district':'Badulla',      'total_customers':2019,  'churned_customers':422,  'churn_rate_pct':20.9, 'monthly_revenue_at_risk':1156348},
        {'district':'Batticaloa',   'total_customers':1340,  'churned_customers':247,  'churn_rate_pct':18.4, 'monthly_revenue_at_risk':702986},
        {'district':'Colombo',      'total_customers':5695,  'churned_customers':1174, 'churn_rate_pct':20.6, 'monthly_revenue_at_risk':3271651},
        {'district':'Galle',        'total_customers':2587,  'churned_customers':543,  'churn_rate_pct':21.0, 'monthly_revenue_at_risk':1481197},
        {'district':'Gampaha',      'total_customers':5579,  'churned_customers':1118, 'churn_rate_pct':20.0, 'monthly_revenue_at_risk':3102601},
        {'district':'Hambantota',   'total_customers':1572,  'churned_customers':322,  'churn_rate_pct':20.5, 'monthly_revenue_at_risk':863010},
        {'district':'Jaffna',       'total_customers':1391,  'churned_customers':308,  'churn_rate_pct':22.1, 'monthly_revenue_at_risk':821430},
        {'district':'Kalutara',     'total_customers':2888,  'churned_customers':621,  'churn_rate_pct':21.5, 'monthly_revenue_at_risk':1691124},
        {'district':'Kandy',        'total_customers':3370,  'churned_customers':701,  'churn_rate_pct':20.8, 'monthly_revenue_at_risk':1919660},
        {'district':'Kegalle',      'total_customers':2013,  'churned_customers':424,  'churn_rate_pct':21.1, 'monthly_revenue_at_risk':1133428},
        {'district':'Kilinochchi',  'total_customers':291,   'churned_customers':62,   'churn_rate_pct':21.3, 'monthly_revenue_at_risk':181555},
        {'district':'Kurunegala',   'total_customers':4028,  'churned_customers':828,  'churn_rate_pct':20.6, 'monthly_revenue_at_risk':2284266},
        {'district':'Mannar',       'total_customers':234,   'churned_customers':48,   'churn_rate_pct':20.5, 'monthly_revenue_at_risk':133120},
        {'district':'Matale',       'total_customers':1198,  'churned_customers':232,  'churn_rate_pct':19.4, 'monthly_revenue_at_risk':633448},
        {'district':'Matara',       'total_customers':1981,  'churned_customers':419,  'churn_rate_pct':21.2, 'monthly_revenue_at_risk':1106712},
        {'district':'Monaragala',   'total_customers':1057,  'churned_customers':232,  'churn_rate_pct':21.9, 'monthly_revenue_at_risk':624003},
        {'district':'Mullaitivu',   'total_customers':263,   'churned_customers':46,   'churn_rate_pct':17.5, 'monthly_revenue_at_risk':115787},
        {'district':'Nuwara Eliya', 'total_customers':1686,  'churned_customers':360,  'churn_rate_pct':21.4, 'monthly_revenue_at_risk':1011585},
        {'district':'Polonnaruwa',  'total_customers':1005,  'churned_customers':207,  'churn_rate_pct':20.6, 'monthly_revenue_at_risk':563769},
        {'district':'Puttalam',     'total_customers':1831,  'churned_customers':355,  'churn_rate_pct':19.4, 'monthly_revenue_at_risk':962675},
        {'district':'Ratnapura',    'total_customers':2752,  'churned_customers':571,  'churn_rate_pct':20.7, 'monthly_revenue_at_risk':1566198},
        {'district':'Trincomalee',  'total_customers':936,   'churned_customers':177,  'churn_rate_pct':18.9, 'monthly_revenue_at_risk':453702},
        {'district':'Vavuniya',     'total_customers':435,   'churned_customers':86,   'churn_rate_pct':19.8, 'monthly_revenue_at_risk':219395},
    ])

    high_risk = pd.DataFrame([
        {'Rank':1,  'Plan':'Platinum', 'District':'Trincomalee',  'ARPU':'LKR 6,137',  'Churn Prob':'92.6%'},
        {'Rank':2,  'Plan':'Platinum', 'District':'Gampaha',      'ARPU':'LKR 11,769', 'Churn Prob':'91.1%'},
        {'Rank':3,  'Plan':'Basic',    'District':'Puttalam',     'ARPU':'LKR 1,322',  'Churn Prob':'91.0%'},
        {'Rank':4,  'Plan':'Platinum', 'District':'Colombo',      'ARPU':'LKR 8,197',  'Churn Prob':'90.2%'},
        {'Rank':5,  'Plan':'Platinum', 'District':'Monaragala',   'ARPU':'LKR 8,060',  'Churn Prob':'90.0%'},
        {'Rank':6,  'Plan':'Silver',   'District':'Kegalle',      'ARPU':'LKR 1,914',  'Churn Prob':'89.2%'},
        {'Rank':7,  'Plan':'Platinum', 'District':'Gampaha',      'ARPU':'LKR 9,499',  'Churn Prob':'88.9%'},
        {'Rank':8,  'Plan':'Platinum', 'District':'Mannar',       'ARPU':'LKR 6,022',  'Churn Prob':'88.4%'},
        {'Rank':9,  'Plan':'Platinum', 'District':'Galle',        'ARPU':'LKR 6,562',  'Churn Prob':'88.3%'},
        {'Rank':10, 'Plan':'Platinum', 'District':'Kurunegala',   'ARPU':'LKR 8,852',  'Churn Prob':'88.1%'},
        {'Rank':11, 'Plan':'Gold',     'District':'Colombo',      'ARPU':'LKR 4,751',  'Churn Prob':'88.1%'},
        {'Rank':12, 'Plan':'Basic',    'District':'Jaffna',       'ARPU':'LKR 1,672',  'Churn Prob':'88.0%'},
        {'Rank':13, 'Plan':'Gold',     'District':'Polonnaruwa',  'ARPU':'LKR 5,896',  'Churn Prob':'88.0%'},
        {'Rank':14, 'Plan':'Platinum', 'District':'Mullaitivu',   'ARPU':'LKR 9,956',  'Churn Prob':'87.9%'},
        {'Rank':15, 'Plan':'Platinum', 'District':'Kalutara',     'ARPU':'LKR 9,861',  'Churn Prob':'87.6%'},
        {'Rank':16, 'Plan':'Gold',     'District':'Anuradhapura', 'ARPU':'LKR 5,491',  'Churn Prob':'87.5%'},
        {'Rank':17, 'Plan':'Gold',     'District':'Kurunegala',   'ARPU':'LKR 5,406',  'Churn Prob':'87.4%'},
        {'Rank':18, 'Plan':'Gold',     'District':'Puttalam',     'ARPU':'LKR 3,853',  'Churn Prob':'87.3%'},
        {'Rank':19, 'Plan':'Basic',    'District':'Anuradhapura', 'ARPU':'LKR 1,248',  'Churn Prob':'87.2%'},
        {'Rank':20, 'Plan':'Gold',     'District':'Jaffna',       'ARPU':'LKR 5,171',  'Churn Prob':'87.1%'},
    ])

    return kpi, plan, district, high_risk


kpi, plan, district, high_risk = load_data()


# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div style='background:#0066CC; padding:16px 24px; border-radius:10px; margin-bottom:20px;'>
    <h2 style='color:white; margin:0; font-size:22px;'>
        📊 Dialog Axiata — Customer Churn Dashboard
    </h2>
    <p style='color:#CCE0FF; margin:4px 0 0 0; font-size:13px;'>
        Weekly monitoring view | Head of Business Analytics |
        LightGBM model (AUC 0.6XXX) | 50,000 postpaid customers
    </p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar filters ───────────────────────────────────────────
st.sidebar.title("🔎 Filters")

selected_plan = st.sidebar.selectbox(
    "Plan Tier",
    ['All Plans'] + list(plan['plan_tier'])
)
selected_district = st.sidebar.selectbox(
    "District",
    ['All Districts'] + sorted(district['district'].tolist())
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Dialog Axiata PLC**  \n"
    "Data Analyst Assessment — Part K  \n"
    "Model: LightGBM | AUC: 0.6XXX"
)

# Apply filters
plan_f = plan if selected_plan == 'All Plans' \
         else plan[plan['plan_tier'] == selected_plan]
dist_f = district if selected_district == 'All Districts' \
         else district[district['district'] == selected_district]

# Recalculate KPIs from filtered rows
filt_cust    = plan_f['total_customers'].sum()
filt_churned = plan_f['churned_customers'].sum()
filt_rate    = round(filt_churned / filt_cust * 100, 1) if filt_cust > 0 else 0
filt_rev     = plan_f['monthly_revenue_at_risk'].sum()
filt_high    = int(filt_cust * (kpi['high_risk_customers'] / kpi['total_customers']))

if selected_district != 'All Districts':
    filt_cust    = dist_f['total_customers'].sum()
    filt_churned = dist_f['churned_customers'].sum()
    filt_rate    = round(filt_churned / filt_cust * 100, 1) if filt_cust > 0 else 0
    filt_rev     = dist_f['monthly_revenue_at_risk'].sum()
    filt_high    = int(filt_cust * (kpi['high_risk_customers'] / kpi['total_customers']))


# ── PANEL 1 — KPI Cards ───────────────────────────────────────
st.subheader("📌 Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Customers", f"{filt_cust:,}")
with c2:
    delta = round(filt_rate - kpi['churn_rate_pct'], 1)
    show_delta = selected_plan != 'All Plans' or selected_district != 'All Districts'
    st.metric("Churn Rate", f"{filt_rate}%",
              delta=f"{delta}% vs overall" if show_delta else None,
              delta_color="inverse")
with c3:
    st.metric("Customers Churned", f"{filt_churned:,}")
with c4:
    st.metric("Monthly Revenue Lost", f"LKR {filt_rev/1e6:.1f}M")
with c5:
    st.metric("High Risk Customers", f"{filt_high:,}",
              help="Churn probability ≥ 65%")

st.markdown("---")


# ── PANEL 2 — Plan Tier ───────────────────────────────────────
st.subheader("📋 Churn by Plan Tier")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        plan_f, x='plan_tier', y='churn_rate_pct',
        color='churn_rate_pct', color_continuous_scale='RdYlGn_r',
        range_color=[15, 27],
        text=[f"{v}%" for v in plan_f['churn_rate_pct']],
        title='Churn Rate % by Plan Tier',
        labels={'plan_tier':'Plan Tier', 'churn_rate_pct':'Churn Rate (%)'}
    )
    fig1.update_traces(textposition='outside')
    fig1.add_hline(y=kpi['churn_rate_pct'], line_dash="dash", line_color="black",
                   annotation_text=f"Overall avg: {kpi['churn_rate_pct']}%")
    fig1.update_layout(coloraxis_showscale=False, yaxis_range=[0, 30],
                       plot_bgcolor='white', height=350,
                       margin=dict(t=50, b=30, l=30, r=30))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        plan_f, x='plan_tier', y='monthly_revenue_at_risk',
        color='monthly_revenue_at_risk', color_continuous_scale='Reds',
        text=[f"LKR {v/1e6:.2f}M" for v in plan_f['monthly_revenue_at_risk']],
        title='Monthly Revenue at Risk by Plan Tier',
        labels={'plan_tier':'Plan Tier', 'monthly_revenue_at_risk':'Revenue at Risk (LKR)'}
    )
    fig2.update_traces(textposition='outside')
    fig2.update_layout(coloraxis_showscale=False, plot_bgcolor='white',
                       height=350, margin=dict(t=50, b=30, l=30, r=30))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")


# ── PANEL 3 — District ────────────────────────────────────────
st.subheader("🗺️ Churn by District — Top 10")

top10_rev  = dist_f.sort_values('monthly_revenue_at_risk', ascending=False).head(10)
top10_rate = dist_f.sort_values('churn_rate_pct', ascending=False).head(10)

col3, col4 = st.columns(2)

with col3:
    d = top10_rev.sort_values('monthly_revenue_at_risk', ascending=True)
    fig3 = px.bar(
        d, x='monthly_revenue_at_risk', y='district', orientation='h',
        color='monthly_revenue_at_risk', color_continuous_scale='Reds',
        text=[f"LKR {v/1e6:.2f}M" for v in d['monthly_revenue_at_risk']],
        title='Top 10 — Monthly Revenue at Risk',
        labels={'monthly_revenue_at_risk':'Revenue at Risk (LKR)', 'district':'District'}
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(coloraxis_showscale=False, plot_bgcolor='white',
                       height=420, margin=dict(t=50, b=30, l=100, r=70))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    d2 = top10_rate.sort_values('churn_rate_pct', ascending=True)
    fig4 = px.bar(
        d2, x='churn_rate_pct', y='district', orientation='h',
        color='churn_rate_pct', color_continuous_scale='RdYlGn_r',
        range_color=[17, 23],
        text=[f"{v}%" for v in d2['churn_rate_pct']],
        title='Top 10 — Churn Rate %',
        labels={'churn_rate_pct':'Churn Rate (%)', 'district':'District'}
    )
    fig4.update_traces(textposition='outside')
    fig4.update_layout(coloraxis_showscale=False, plot_bgcolor='white',
                       height=420, margin=dict(t=50, b=30, l=100, r=60))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")


# ── PANEL 4 — Treemap ─────────────────────────────────────────
st.subheader("💰 Revenue at Risk — All Districts")

col5, col6 = st.columns([3, 2])

with col5:
    fig5 = px.treemap(
        dist_f[dist_f['monthly_revenue_at_risk'] > 0],
        path=['district'], values='monthly_revenue_at_risk',
        color='churn_rate_pct', color_continuous_scale='RdYlGn_r',
        range_color=[17, 23],
        title='Bigger box = more revenue at risk  |  Red = high churn rate',
        hover_data={'churn_rate_pct':':.1f', 'total_customers':':,',
                    'monthly_revenue_at_risk':':,'}
    )
    fig5.update_layout(height=420, coloraxis_colorbar_title='Churn %',
                       margin=dict(t=50, b=10, l=10, r=10))
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown("**District Summary Table**")
    tbl = dist_f.sort_values('monthly_revenue_at_risk', ascending=False)[
        ['district', 'total_customers', 'churn_rate_pct', 'monthly_revenue_at_risk']
    ].copy().reset_index(drop=True)
    tbl.columns = ['District', 'Customers', 'Churn %', 'Rev at Risk']
    tbl['Churn %']     = tbl['Churn %'].apply(lambda x: f"{x}%")
    tbl['Rev at Risk'] = tbl['Rev at Risk'].apply(lambda x: f"LKR {x:,.0f}")
    st.dataframe(tbl, use_container_width=True, height=400)

st.markdown("---")


# ── PANEL 5 — High Risk List ──────────────────────────────────
st.subheader("⚠️ Top 20 Highest Risk Customers (De-identified)")

col7, col8 = st.columns([1, 2])
with col7:
    st.markdown(f"**High-risk customers:** {kpi['high_risk_customers']:,}")
    st.markdown("**Threshold:** Churn probability ≥ 65%")
    st.markdown("**Ranked by:** LightGBM churn probability score")
    st.markdown("Customer IDs hidden for privacy.")
with col8:
    st.dataframe(high_risk, use_container_width=True, height=420)

# Footer
st.markdown("""
<div style='text-align:center; color:#888; font-size:11px; padding:10px;'>
    Dialog Axiata PLC | Data Analyst Assessment Part K |
    LightGBM AUC 0.6XXX | 50,000 postpaid customers | 2025
</div>
""", unsafe_allow_html=True)
