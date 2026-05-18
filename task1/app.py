import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Sales KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 42px; font-weight: bold; color: #4B91F7; }
    .metric-card { background-color: #1E2937; padding: 20px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Sales KPI Dashboard")
st.markdown("**2025 Performance Overview** | Last Updated: May 2026")

# ====================== Sidebar ======================
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Region", ["South India", "North India", "East", "West"], default=["South India"])
product = st.sidebar.multiselect("Product Category", 
    ["Electronics", "Fashion", "Home & Kitchen", "Beauty"], 
    default=["Electronics", "Fashion"])

# ====================== Fake Data ======================
# Monthly Data
dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='M')
monthly_data = pd.DataFrame({
    'Month': dates,
    'Revenue': [245000, 380000, 520000, 680000, 820000, 910000, 1050000, 1120000, 980000, 1250000, 1380000, 1420000],
    'Units_Sold': [980, 1150, 1320, 1680, 1950, 2100, 2450, 2380, 1980, 2650, 2890, 3100],
    'Conversion_Rate': [19.5, 21.2, 24.8, 26.5, 23.1, 28.7, 25.4, 22.8, 27.9, 24.1, 26.3, 29.2],
    'CAC': [68, 65, 72, 59, 55, 48, 52, 61, 58, 45, 49, 47]
})

# Overall KPIs
total_revenue = monthly_data['Revenue'].sum()
total_units = monthly_data['Units_Sold'].sum()
avg_conversion = monthly_data['Conversion_Rate'].mean()
avg_aov = total_revenue / total_units
growth = ((monthly_data['Revenue'].iloc[-1] - monthly_data['Revenue'].iloc[0]) / monthly_data['Revenue'].iloc[0]) * 100

# ====================== Top Metrics ======================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Revenue", f"₹{total_revenue/1000000:.2f} Cr", "↑ 29.4%")
with col2:
    st.metric("Total Units Sold", f"{total_units:,}", "↑ 18%")
with col3:
    st.metric("Avg Conversion Rate", f"{avg_conversion:.1f}%", "↑ 2.3%")
with col4:
    st.metric("Avg Order Value", f"₹{avg_aov:.0f}", "↑ ₹12")
with col5:
    st.metric("Revenue Growth", f"{growth:.1f}%", "YoY")

st.markdown("---")

# ====================== Charts ======================
tab1, tab2, tab3 = st.tabs(["📈 Performance Trends", "📊 Channel Analysis", "🥇 Top Performers"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig_revenue = px.line(monthly_data, x='Month', y='Revenue',
                            title="Monthly Revenue Trend",
                            markers=True, line_shape="spline")
        fig_revenue.update_traces(line_color='#60A5FA')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        fig_units = px.bar(monthly_data, x='Month', y='Units_Sold',
                          title="Units Sold per Month",
                          color_discrete_sequence=['#34D399'])
        st.plotly_chart(fig_units, use_container_width=True)

    # Conversion Rate
    fig_conv = px.line(monthly_data, x='Month', y='Conversion_Rate',
                      title="Conversion Rate Trend (%)",
                      markers=True, line_shape="spline")
    fig_conv.update_traces(line_color='#F472B6')
    st.plotly_chart(fig_conv, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        # CAC vs AOV
        fig_cac = go.Figure()
        fig_cac.add_bar(x=monthly_data['Month'], y=monthly_data['CAC'], name="CAC", marker_color='#F87171')
        fig_cac.add_scatter(x=monthly_data['Month'], y=monthly_data['Revenue']/monthly_data['Units_Sold'],
                           name="AOV", mode='lines+markers', line_color='#A78BFA')
        fig_cac.update_layout(title="CAC vs Average Order Value")
        st.plotly_chart(fig_cac, use_container_width=True)
    
    with col2:
        st.info("**Key Insights**\n\n"
                "• Revenue peaked in December\n"
                "• Best Conversion in May & December\n"
                "• CAC reduced significantly in Q4")

with tab3:
    st.subheader("Top Performing Products")
    top_products = pd.DataFrame({
        'Product': ['Wireless Earbuds', 'Smart Watch', 'Cotton T-Shirts', 'Kitchen Blender', 'Face Serum'],
        'Revenue': [1240000, 980000, 750000, 620000, 580000],
        'Units': [4200, 1850, 6800, 950, 2100]
    })
    st.dataframe(top_products, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using **Python + Streamlit** | Feel free to fork & customize!")