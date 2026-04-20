"""
Pet Cost Estimator - Streamlit App
==================================
Helps prospective pet owners estimate annual pet care costs
with supporting pet store industry insights
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Pet Cost Estimator",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #888;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    }
    .insight-card {
        background: #f8f9ff;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.4rem 0;
    }
    .store-insight-card {
        background: #fff8f0;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #FF9F43;
        margin: 0.4rem 0;
    }
    .perspective-tab {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: bold;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .store-tab {
        background: linear-gradient(90deg, #FF9F43, #ee8a2f);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: bold;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin: 1.2rem 0 0.5rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        width: 100%;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.3rem 0;
    }
    .highlight-box {
        background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #FF6B6B;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    with open('pet_price_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_analysis():
    with open('analysis_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()
analysis = load_analysis()

# ==================== DYNAMIC IMPACT CALCULATOR ====================
PET_MARKET_SHARE = {
    'Short-haired Cat': {'share': 0.20, 'avg_monthly_spend': 170},
    'Long-haired Cat': {'share': 0.12, 'avg_monthly_spend': 190},
    'Small Dog': {'share': 0.15, 'avg_monthly_spend': 160},
    'Medium Dog': {'share': 0.13, 'avg_monthly_spend': 200},
    'Large Dog': {'share': 0.10, 'avg_monthly_spend': 265},
    'fish': {'share': 0.08, 'avg_monthly_spend': 45},
    'bird': {'share': 0.09, 'avg_monthly_spend': 93},
    'hamster': {'share': 0.05, 'avg_monthly_spend': 51},
    'rabbit': {'share': 0.04, 'avg_monthly_spend': 130},
    'Reptile': {'share': 0.04, 'avg_monthly_spend': 43}
}

REGION_MARKET_SIZE = {
    'North America': 1.35, 'Europe': 1.25, 'Oceania': 1.30,
    'Asia': 0.85, 'South America': 0.75, 'Africa': 0.65, 'Antarctica': 2.00
}

CATEGORY_PREFERENCE = {
    'Short-haired Cat': {'Grooming': 0.18, 'Food': 0.32, 'Toys & Supplies': 0.28, 'Medical': 0.22},
    'Long-haired Cat': {'Grooming': 0.28, 'Food': 0.28, 'Toys & Supplies': 0.22, 'Medical': 0.22},
    'Small Dog': {'Grooming': 0.22, 'Food': 0.30, 'Toys & Supplies': 0.18, 'Medical': 0.30},
    'Medium Dog': {'Grooming': 0.15, 'Food': 0.32, 'Toys & Supplies': 0.25, 'Medical': 0.28},
    'Large Dog': {'Grooming': 0.12, 'Food': 0.35, 'Toys & Supplies': 0.22, 'Medical': 0.31},
    'fish': {'Grooming': 0.15, 'Food': 0.25, 'Toys & Supplies': 0.38, 'Medical': 0.22},
    'bird': {'Grooming': 0.12, 'Food': 0.30, 'Toys & Supplies': 0.35, 'Medical': 0.23},
    'hamster': {'Grooming': 0.18, 'Food': 0.28, 'Toys & Supplies': 0.35, 'Medical': 0.19},
    'rabbit': {'Grooming': 0.15, 'Food': 0.35, 'Toys & Supplies': 0.25, 'Medical': 0.25},
    'Reptile': {'Grooming': 0.12, 'Food': 0.25, 'Toys & Supplies': 0.42, 'Medical': 0.21}
}

def get_tier_info(avg_mult):
    if avg_mult < 0.8:
        return {'label': 'Budget Conscious', 'margin': 0.15, 'impact': 0.75}
    elif avg_mult < 1.2:
        return {'label': 'Standard', 'margin': 0.25, 'impact': 1.0}
    else:
        return {'label': 'Premium', 'margin': 0.35, 'impact': 1.45}

def generate_impact(pet, region, mults):
    base = PET_MARKET_SHARE.get(pet, {}).get('avg_monthly_spend', 100)
    r_mult = REGION_MARKET_SIZE.get(region, 1.0)
    actual = base * r_mult * np.mean(list(mults.values()))
    regional_avg = base * r_mult
    global_avg = base
    avg_m = np.mean(list(mults.values()))
    tier = get_tier_info(avg_m)
    lift = ((actual - regional_avg) / regional_avg * 100) if regional_avg > 0 else 0
    cat_pref = CATEGORY_PREFERENCE.get(pet, {})
    return {
        'actual_monthly': actual,
        'regional_avg_monthly': regional_avg,
        'global_avg_monthly': global_avg,
        'revenue_lift_pct': lift,
        'spending_tier': tier['label'],
        'store_margin': tier['margin'],
        'cat_pref': cat_pref,
        'avg_mult': avg_m,
        'region_mult': r_mult
    }

# ==================== CONFIG ====================
PET_CATEGORIES = {
    '🐱 Cat': {'types': {'Short-haired Cat': 'British, Siamese', 'Long-haired Cat': 'Ragdoll, Persian'}},
    '🐶 Dog': {'types': {'Small Dog': 'Poodle, Chihuahua', 'Medium Dog': 'Corgi, Shiba', 'Large Dog': 'Golden, Husky'}},
    '🐠 Fish': {'types': {'fish': 'Tropical, Goldfish'}},
    '🦜 Bird': {'types': {'bird': 'Parrot, Finch'}},
    '🐹 Hamster': {'types': {'hamster': 'Syrian, Dwarf'}},
    '🐰 Rabbit': {'types': {'rabbit': 'Lop, Dwarf'}},
    '🦎 Reptile': {'types': {'Reptile': 'Gecko, Snake'}}
}

REGIONS = {
    'North America': '🌎 North America', 'Europe': '🌍 Europe', 'Oceania': '🌏 Oceania',
    'Asia': '🌏 Asia', 'South America': '🌎 South America', 'Africa': '🌍 Africa', 'Antarctica': '🧊 Antarctica'
}

CATEGORY_ICONS = {'Grooming': '🛁', 'Food': '🍖', 'Toys & Supplies': '🎾', 'Medical': '💊'}

PET_TIPS = {
    'Short-haired Cat': {'grooming': 'Low-maintenance! Weekly brushing.','food': 'High-protein diet, wet food for hydration.','supplies': 'Scratching post, cat tree.','medical': 'Regular vaccines, watch dental issues.'},
    'Long-haired Cat': {'grooming': 'Daily brushing to prevent matting.','food': 'Omega fatty acids for coat health.','supplies': 'Detangling brushes, multiple posts.','medical': 'Watch for skin issues, hairballs.'},
    'Small Dog': {'grooming': 'Professional groom every 4-6 weeks.','food': 'Small breed kibble, dental chews.','supplies': 'Harness, small toys, cozy bed.','medical': 'Dental disease, patellar issues.'},
    'Medium Dog': {'grooming': 'Brush 2-3x/week.','food': 'Balanced diet matching activity.','supplies': 'Durable toys, outdoor gear.','medical': 'Hip dysplasia screening.'},
    'Large Dog': {'grooming': 'Regular brushing, shedding season.','food': 'Large breed formula for joints.','supplies': 'Heavy-duty toys, large bed.','medical': 'Hip/elbow screening, bloat prevention.'},
    'fish': {'grooming': 'Weekly water changes, filter cleaning.','food': 'Species-specific flakes/pellets.','supplies': 'Filter, heater, water testing kit.','medical': 'Quarantine new fish, monitor pH.'},
    'bird': {'grooming': 'Wing/nail trims, mist bathing.','food': 'Pellets + fresh fruits/veg. No avocado!','supplies': 'Large cage, varied perches, foraging toys.','medical': 'Annual avian vet, respiratory watch.'},
    'hamster': {'grooming': 'Minimal grooming, sand bath.','food': 'Hamster pellets, occasional treats.','supplies': 'Spacious cage, exercise wheel, deep bedding.','medical': '2-3 year lifespan, watch for wet tail.'},
    'rabbit': {'grooming': 'Regular brushing, nail trims.','food': 'Unlimited hay essential! Fresh veg daily.','supplies': 'Large enclosure, litter box, chew toys.','medical': 'Spay/neuter recommended, watch GI stasis.'},
    'Reptile': {'grooming': 'Enclosure cleaning, UVB replacement.','food': 'Live insects/rodents + calcium.','supplies': 'Heating gradient, UVB, hides, humidity control.','medical': 'Find exotic vet, prevent metabolic bone disease.'}
}

# ==================== HEADER ====================
st.markdown('<p class="main-header">🐾 Pet Cost Estimator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">💰 Estimate your pet care costs &nbsp;|&nbsp; 📊 With pet store industry insights</p>', unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 Your Selection")
    st.markdown("---")
    pet_name = st.text_input("💝 Pet Name (optional)", placeholder="e.g. Luna, Max...")
    st.markdown("---")
    selected_category = st.selectbox("1️⃣ Pet Category", options=list(PET_CATEGORIES.keys()))
    pet_types = PET_CATEGORIES[selected_category]['types']
    if len(pet_types) > 1:
        selected_pet = st.selectbox("2️⃣ Specific Type", options=list(pet_types.keys()), format_func=lambda x: f"{x} ({pet_types[x]})")
    else:
        selected_pet = list(pet_types.keys())[0]
        st.info(f"**{selected_pet}** - {pet_types[selected_pet]}")
    st.markdown("---")
    selected_region = st.selectbox("3️⃣ Region", options=list(REGIONS.keys()), format_func=lambda x: REGIONS[x])
    st.markdown("---")
    st.markdown("4️⃣ Spending Levels")
    demand_multipliers = {}
    for cat in ['Grooming', 'Food', 'Toys & Supplies', 'Medical']:
        val = st.slider(f"{CATEGORY_ICONS[cat]} {cat}", 0.5, 2.0, 1.0, 0.1, key=f"sl_{cat}")
        demand_multipliers[cat] = val
        badge = "🟢 Basic" if val < 0.8 else "🔵 Standard" if val < 1.2 else "🔴 Premium"
        st.caption(f"{badge} ({val:.1f}x)")
    st.markdown("---")
    calculate = st.button("💰 Calculate Annual Cost")

# ==================== MAIN CONTENT ====================
if calculate:
    display_name = pet_name.strip() if pet_name.strip() else selected_pet

    # --- Cost Calculation ---
    region_data = data['region_data'].get(selected_region, {})
    pet_data = region_data.get(selected_pet, {})
    if not pet_data:
        pet_data = data['global_data'].get(selected_pet, {})
        st.warning(f"⚠️ Limited data for {REGIONS[selected_region]}. Using global average.")

    monthly_costs = {}
    for cat in ['Grooming', 'Food', 'Toys & Supplies', 'Medical']:
        base = pet_data.get(cat, {}).get('avg_price', 30)
        monthly_costs[cat] = round(base * demand_multipliers[cat], 2)
    monthly_total = sum(monthly_costs.values())
    annual_total = monthly_total * 12

    # --- Dynamic Impact Calculation ---
    impact = generate_impact(selected_pet, selected_region, demand_multipliers)

    # ============ YOUR ANNUAL COST (MAIN) ============
    if pet_name.strip():
        st.markdown(f"<h2 style='text-align:center;color:#667eea;'>💝 {pet_name}'s Annual Cost</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='text-align:center;color:#667eea;'>🐾 {selected_pet} Annual Cost</h2>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
        <h1 style="font-size:4.5rem;margin:0;color:#FFD93D;">${annual_total:,.0f}</h1>
        <p style="font-size:1.1rem;opacity:0.9;">📍 {REGIONS[selected_region]} &nbsp;|&nbsp; 📅 ${monthly_total:,.0f}/month</p>
    </div>
    """, unsafe_allow_html=True)

    # ============ PART 1: YOUR COST BREAKDOWN (PRIMARY) ============
    st.markdown("<div class='perspective-tab'>💰 YOUR COST BREAKDOWN — Personalized Estimate</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("<div class='section-title'>📊 Monthly Costs</div>", unsafe_allow_html=True)
        df_cost = pd.DataFrame({
            'Category': [f"{CATEGORY_ICONS[c]} {c}" for c in monthly_costs.keys()],
            'Level': [f"{demand_multipliers[c]:.1f}x" for c in monthly_costs.keys()],
            'Monthly': [f"${v:,.0f}" for v in monthly_costs.values()],
            'Annual': [f"${v*12:,.0f}" for v in monthly_costs.values()]
        })
        st.dataframe(df_cost, hide_index=True, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>📈 Your Cost Distribution</div>", unsafe_allow_html=True)
        fig = go.Figure(data=[go.Pie(
            labels=list(monthly_costs.keys()), values=list(monthly_costs.values()),
            hole=0.45, marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            textinfo='label+percent'
        )])
        fig.update_layout(showlegend=False, margin=dict(t=5, b=5, l=5, r=5), height=260)
        st.plotly_chart(fig, use_container_width=True)

    # --- YOUR SPENDING PROFILE ---
    st.markdown("<div class='section-title'>📍 Your Spending Profile</div>", unsafe_allow_html=True)

    prof_c1, prof_c2, prof_c3 = st.columns(3)
    with prof_c1:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.85rem;color:#888;">🌍 Global Avg ({selected_pet})</div>
            <div style="font-size:1.8rem;color:#888;font-weight:bold;">${impact['global_avg_monthly']:.0f}</div>
            <div style="font-size:0.8rem;color:#aaa;">per month</div>
        </div>
        """, unsafe_allow_html=True)
    with prof_c2:
        st.markdown(f"""
        <div class="metric-box" style="border:2px solid #667eea;">
            <div style="font-size:0.85rem;color:#667eea;">📍 {selected_region} Avg</div>
            <div style="font-size:1.8rem;color:#667eea;font-weight:bold;">${impact['regional_avg_monthly']:.0f}</div>
            <div style="font-size:0.8rem;color:#888;">per month (x{impact['region_mult']:.2f})</div>
        </div>
        """, unsafe_allow_html=True)
    with prof_c3:
        st.markdown(f"""
        <div class="metric-box" style="border:2px solid #FF6B6B;background:#fff5f5;">
            <div style="font-size:0.85rem;color:#FF6B6B;">💎 YOUR SPEND</div>
            <div style="font-size:2rem;color:#FF6B6B;font-weight:bold;">${impact['actual_monthly']:.0f}</div>
            <div style="font-size:0.8rem;color:#888;">per month (x{impact['avg_mult']:.1f})</div>
        </div>
        """, unsafe_allow_html=True)

    # Spending tier insight
    lift_sign = "+" if impact['revenue_lift_pct'] >= 0 else ""
    tier_color = "#28a745" if impact['revenue_lift_pct'] >= 0 else "#dc3545"
    st.markdown(f"""
    <div class="highlight-box">
        <div style="font-size:1.1rem;">
            🏷️ <b>Your Tier:</b> {impact['spending_tier']} &nbsp;|&nbsp;
            📊 <b>vs Regional Avg:</b> <span style="color:{tier_color};font-weight:bold;">{lift_sign}{impact['revenue_lift_pct']:.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============ PART 2: PERSONALIZED TIPS ============
    st.markdown("<div class='perspective-tab'>💡 Personalized Care Tips for {name}</div>".replace('{name}', display_name), unsafe_allow_html=True)

    tips = PET_TIPS.get(selected_pet, PET_TIPS['Short-haired Cat'])
    t1, t2 = st.columns(2)
    with t1:
        for icon, key in [('🛁', 'grooming'), ('🍖', 'food')]:
            st.markdown(f"""
            <div class="insight-card">
                <h4>{icon} {key.title()}</h4>
                <p style="font-size:0.92rem;">{tips[key]}</p>
            </div>
            """, unsafe_allow_html=True)
    with t2:
        for icon, key in [('🎾', 'supplies'), ('💊', 'medical')]:
            st.markdown(f"""
            <div class="insight-card">
                <h4>{icon} {key.title()}</h4>
                <p style="font-size:0.92rem;">{tips[key]}</p>
            </div>
            """, unsafe_allow_html=True)

    # ============ PART 3: PET STORE INSIGHTS (SUPPORTING) ============
    st.markdown("<div class='store-tab'>📊 PET STORE INSIGHTS — For Industry Reference (Kaggle 2020 Data)</div>", unsafe_allow_html=True)
    st.caption("*The following analysis is based on real Pet Store Records 2020 data from Kaggle, provided as supplementary industry insights for pet store operators.*")

    # --- Your Choices' Impact on Store Revenue ---
    st.markdown("<div class='section-title'>🔗 How Your Consumer Profile Impacts Pet Store Revenue</div>", unsafe_allow_html=True)

    cat_pref = impact['cat_pref']
    impact_cols = st.columns(4)
    for idx, cat in enumerate(['Grooming', 'Food', 'Toys & Supplies', 'Medical']):
        with impact_cols[idx]:
            pref_pct = cat_pref.get(cat, 0.25) * 100
            actual_spend = monthly_costs.get(cat, 0)
            st.markdown(f"""
            <div class="store-insight-card">
                <div style="font-size:1.5rem;text-align:center;">{CATEGORY_ICONS[cat]}</div>
                <div style="font-weight:bold;text-align:center;">{cat}</div>
                <div style="font-size:1.2rem;color:#FF9F43;font-weight:bold;text-align:center;">${actual_spend:.0f}/mo</div>
                <div style="font-size:0.85rem;color:#888;text-align:center;">{pref_pct:.0f}% of {selected_pet} owners' budget</div>
            </div>
            """, unsafe_allow_html=True)

    # Contextual store insight
    if impact['revenue_lift_pct'] > 15:
        store_msg = f"Pet stores in {selected_region} benefit significantly from {selected_pet} owners with Premium spending patterns. Your profile represents a high-value customer segment that drives disproportionate revenue."
    elif impact['revenue_lift_pct'] > 5:
        store_msg = f"As an above-average spender on {selected_pet} care in {selected_region}, your profile contributes positively to store revenue. Stores should note that {selected_pet} owners in this region often prioritize quality."
    elif impact['revenue_lift_pct'] > -5:
        store_msg = f"Your spending aligns with the typical {selected_pet} owner in {selected_region}, representing the core market base. Most stores design their inventory around customers like you."
    else:
        store_msg = f"Budget-conscious {selected_pet} owners like you represent a price-sensitive segment. Stores in {selected_region} may need competitive pricing and value bundles to retain this customer group."

    st.markdown(f"""
    <div class="store-insight-card">
        <h4>🏪 Store Operator Note</h4>
        <p style="font-size:0.95rem;">{store_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    # Top revenue driver for this pet type
    top_cat = max(impact['cat_pref'], key=impact['cat_pref'].get)
    st.markdown(f"""
    <div class="store-insight-card">
        <h4>🏆 Top Revenue Category for {selected_pet} Owners</h4>
        <p style="font-size:0.95rem;">For <b>{selected_pet}</b> owners, <b>{top_cat}</b> represents the largest share of spending ({impact['cat_pref'][top_cat]*100:.0f}% of budget). Pet stores stocking premium {top_cat.lower()} products for {selected_pet} owners can maximize revenue from this segment.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- General Industry Insights ---
    st.markdown("<div class='section-title'>📋 Industry Overview (2020 Data)</div>", unsafe_allow_html=True)

    ind_c1, ind_c2 = st.columns(2)
    with ind_c1:
        vap = analysis['vap_impact']
        st.markdown(f"""
        <div class="store-insight-card">
            <h4>💊 VAP Products Generate +15% Revenue</h4>
            <p>Vet-approved products averaged <b>${vap['with_vap']['avg_revenue_usd']:,.0f}</b> vs <b>${vap['no_vap']['avg_revenue_usd']:,.0f}</b> for non-VAP.</p>
            <p style="font-size:0.85rem;color:#888;">VAP certification builds customer trust and justifies premium pricing.</p>
        </div>
        """, unsafe_allow_html=True)
    with ind_c2:
        rep = analysis['repurchase']
        st.markdown(f"""
        <div class="store-insight-card">
            <h4>🔄 Repurchase = +12.6% Revenue</h4>
            <p>Repurchased products: <b>${rep['repurchased']['avg_revenue_usd']:,.0f}</b> avg | Non-repurchased: <b>${rep['no_repurchase']['avg_revenue_usd']:,.0f}</b></p>
            <p style="font-size:0.85rem;color:#888;">Lower ratings on repurchased items suggest necessity-driven buying.</p>
        </div>
        """, unsafe_allow_html=True)

    # Revenue by pet type
    st.markdown("<div class='section-title'>🐾 Revenue by Pet Type (2020)</div>", unsafe_allow_html=True)
    pet_cols = st.columns(3)
    for idx, (pet, info) in enumerate(analysis['revenue_by_pet'].items()):
        with pet_cols[idx % 3]:
            emoji = {'cat': '🐱', 'dog': '🐶', 'bird': '🦜', 'fish': '🐠', 'rabbit': '🐰', 'hamster': '🐹'}.get(pet, '🐾')
            st.markdown(f"""
            <div class="store-insight-card">
                <div style="font-weight:bold;">{emoji} {pet.title()}</div>
                <div style="font-size:1.1rem;color:#FF9F43;font-weight:bold;">${info['revenue_usd']:,.0f} ({info['pct']}%)</div>
            </div>
            """, unsafe_allow_html=True)

    # Regional chart
    st.markdown("<div class='section-title'>🌍 Regional Revenue Distribution (2020)</div>", unsafe_allow_html=True)
    fig_reg = go.Figure(data=[go.Bar(
        x=list(analysis['revenue_by_country'].keys()),
        y=[v['revenue_usd'] for v in analysis['revenue_by_country'].values()],
        marker_color=['#667eea', '#4ECDC4', '#45B7D1', '#96CEB4', '#FF6B6B', '#FF9F43', '#DDA0DD', '#8FBC8F', '#F0E68C'],
        text=[f"${v['revenue_usd']:,.0f}" for v in analysis['revenue_by_country'].values()],
        textposition='outside'
    )])
    fig_reg.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=280)
    st.plotly_chart(fig_reg, use_container_width=True)

    st.markdown("---")
    st.caption("💰 Pet Owner Costs: Personalized estimate adjusted by region | 📊 Store Insights: Kaggle Pet Store Records 2020 | 💵 USD | 🌍 7 Continents")

else:
    # ============ WELCOME VIEW ============
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:2rem;">
        <div style="font-size:3.5rem;margin-bottom:1rem;">🐾</div>
        <h2>Welcome to Pet Cost Estimator!</h2>
        <p style="font-size:1.05rem;color:#666;">
            Select your pet, region, and spending preferences on the left.<br>
            Get your <b>personalized annual cost estimate</b> plus <b>supporting pet store industry insights</b>.<br>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='perspective-tab'>📊 Pet Store Industry Snapshot (Kaggle 2020 Data)</div>", unsafe_allow_html=True)

    prev_c1, prev_c2, prev_c3 = st.columns(3)
    with prev_c1:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:2rem;color:#667eea;font-weight:bold;">$12.1M</div>
            <div style="font-size:0.9rem;color:#888;">Total 2020 Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    with prev_c2:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:2rem;color:#FF6B6B;font-weight:bold;">879</div>
            <div style="font-size:0.9rem;color:#888;">Products Analysed</div>
        </div>
        """, unsafe_allow_html=True)
    with prev_c3:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:2rem;color:#4ECDC4;font-weight:bold;">58%</div>
            <div style="font-size:0.9rem;color:#888;">Revenue from India</div>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 **Tip:** Use the sliders to adjust your spending level for each category. Your choices not only affect your costs but also reveal insights about pet store revenue patterns!")

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#bbb;padding:0.5rem;font-size:0.82rem;">
    🐾 Pet Cost Estimator | 💵 USD | 🌍 7 Continents | Data: Kaggle Pet Store Records 2020
</div>
""", unsafe_allow_html=True)
