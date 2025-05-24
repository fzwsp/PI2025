import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import base64


# Set page configuration
st.set_page_config(
    page_title="West Java Tea Plantation Dashboard",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e6e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2a9d8f;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .card {
        border-radius: 5px;
        padding: 1rem;
        background-color: #f0f8f4;
        margin-bottom: 1rem;
    }
    .insights-text {
        font-size: 1.1rem;
        line-height: 1.5;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1e6e50;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
    }
    .stButton>button {
        background-color: #2a9d8f;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Function to load the data
@st.cache_data
def load_data():
    # Read the CSV content from window.fs
    try:
        content = window.fs.readFile('perkebunan_teh.csv', {'encoding': 'utf8'})
        df = pd.read_csv(StringIO(content))
        return df
    except:
        # If running in an environment without window.fs, use a sample of the data for testing
        st.warning("Using sample data for testing purposes.")
        
        # Create sample data that mimics the structure
        regions = ['KABUPATEN CIANJUR', 'KABUPATEN TASIKMALAYA', 'KABUPATEN BANDUNG', 
                  'KABUPATEN GARUT', 'KABUPATEN SUKABUMI']
        years = list(range(2017, 2025))
        
        data = []
        for region in regions:
            for year in years:
                data.append({
                    'kab_kota': region,
                    'tahun': year,
                    'produksi_rakyat': np.random.randint(2000, 13000) if region != 'KABUPATEN BOGOR' else np.random.randint(0, 30),
                    'produksi_swasta': np.random.randint(0, 12000),
                    'produktivitas_rakyat': np.random.randint(700, 2200),
                    'produktivitas_swasta': np.random.randint(900, 2300) if np.random.random() > 0.3 else 0,
                    'log_prdks_rakyat': 0.0,  # Will be recalculated
                    'log_prdks_swasta': 0.0,  # Will be recalculated
                    'cluster_produksi': 1,
                    'cluster_produktivitas': 1
                })
        
        df = pd.DataFrame(data)
        
        # Recalculate log values
        df['log_prdks_rakyat'] = np.log(df['produksi_rakyat'] + 1)
        df['log_prdks_swasta'] = np.log(df['produksi_swasta'] + 1)
        
        # Set clusters
        df.loc[df['produksi_rakyat'] == 0, 'cluster_produksi'] = 0
        df.loc[df['produktivitas_rakyat'] == 0, 'cluster_produktivitas'] = 0
        
        return df

# Function to create a download link for dataframes
def get_table_download_link(df, filename="data.csv", text="Download CSV"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to plot choropleth map of West Java
def plot_west_java_map(df, year, column):
    # This is a placeholder for the map visualization
    st.write("Geographic Map Visualization (Placeholder)")
    st.info("In a production environment, this would display a choropleth map of West Java districts showing tea production data.")
    
    # Create bar chart as an alternative visualization
    fig = px.bar(
        df[df['tahun'] == year].sort_values(column, ascending=False), 
        x='kab_kota', 
        y=column,
        title=f"{column} by District in {year}",
        color=column,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Load data
df = load_data()

# Define main navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/1/1e/Tea_plantation_in_Indonesia.jpg", width=300)
st.sidebar.title("🍵 Tea Plantation Analysis")

# Navigation menu
app_mode = st.sidebar.selectbox("Navigation", [
    "📊 Dashboard Overview", 
    "🌱 Production Analysis", 
    "📈 Productivity Analysis",
    "🔍 Regional Comparison",
    "📋 Data Explorer"
])

# Year filter for all pages
selected_year = st.sidebar.slider("Select Year", min_value=int(df['tahun'].min()), max_value=int(df['tahun'].max()), value=int(df['tahun'].max()))

# Filter dataframe for selected year
df_selected_year = df[df['tahun'] == selected_year]

# Function to format numbers with thousand separators
def format_number(num):
    return f"{num:,.0f}"

# Get producing districts (where production > 0)
producing_districts = df[(df['produksi_rakyat'] > 0) | (df['produksi_swasta'] > 0)]['kab_kota'].unique()

# Dashboard Overview
if app_mode == "📊 Dashboard Overview":
    st.markdown("<h1 class='main-header'>West Java Tea Plantation Dashboard</h1>", unsafe_allow_html=True)
    
    # Year summary
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='sub-header'>Tea Production Summary for {selected_year}</h2>", unsafe_allow_html=True)
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    # Total production
    total_production = df_selected_year['produksi_rakyat'].sum() + df_selected_year['produksi_swasta'].sum()
    col1.markdown(f"<div class='metric-value'>{format_number(total_production)}</div>", unsafe_allow_html=True)
    col1.markdown("<div class='metric-label'>Total Production (Tons)</div>", unsafe_allow_html=True)
    
    # Active producing districts
    active_districts = df_selected_year[(df_selected_year['produksi_rakyat'] > 0) | (df_selected_year['produksi_swasta'] > 0)]['kab_kota'].nunique()
    col2.markdown(f"<div class='metric-value'>{active_districts}</div>", unsafe_allow_html=True)
    col2.markdown("<div class='metric-label'>Active Producing Districts</div>", unsafe_allow_html=True)
    
    # Average productivity
    avg_productivity = df_selected_year[df_selected_year['produktivitas_rakyat'] > 0]['produktivitas_rakyat'].mean()
    col3.markdown(f"<div class='metric-value'>{format_number(avg_productivity)}</div>", unsafe_allow_html=True)
    col3.markdown("<div class='metric-label'>Avg. Smallholder Productivity</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dashboard layout with two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 producing districts
        st.markdown("<h3>Top 5 Tea Producing Districts</h3>", unsafe_allow_html=True)
        top_districts = df_selected_year.sort_values('produksi_rakyat', ascending=False).head(5)
        fig = px.bar(
            top_districts, 
            x='kab_kota', 
            y='produksi_rakyat',
            color='produksi_rakyat',
            color_continuous_scale='Greens',
            title="Smallholder Production (Tons)"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Production trend over time
        st.markdown("<h3>Production Trend (2017-2024)</h3>", unsafe_allow_html=True)
        # Get top 5 districts for time series
        top5_districts = df.groupby('kab_kota')['produksi_rakyat'].sum().nlargest(5).index
        df_top5 = df[df['kab_kota'].isin(top5_districts)]
        
        # Pivot to get year as columns
        pivot_df = df_top5.pivot_table(
            index='kab_kota', 
            columns='tahun', 
            values='produksi_rakyat', 
            aggfunc='sum'
        ).reset_index()
        
        # Create time series chart
        fig = go.Figure()
        for district in top5_districts:
            district_data = df[df['kab_kota'] == district]
            fig.add_trace(go.Scatter(
                x=district_data['tahun'], 
                y=district_data['produksi_rakyat'],
                mode='lines+markers',
                name=district
            ))
        
        fig.update_layout(
            title="Smallholder Production Trend",
            xaxis_title="Year",
            yaxis_title="Production (Tons)",
            legend_title="District"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Production distribution
        st.markdown("<h3>Production Distribution</h3>", unsafe_allow_html=True)
        
        # Create a dataframe with total production by district
        production_df = df_selected_year.copy()
        production_df['total_production'] = production_df['produksi_rakyat'] + production_df['produksi_swasta']
        production_df = production_df[production_df['total_production'] > 0]
        
        fig = px.pie(
            production_df,
            values='total_production',
            names='kab_kota',
            title=f"Tea Production Distribution ({selected_year})",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Ownership structure
        st.markdown("<h3>Ownership Structure</h3>", unsafe_allow_html=True)
        
        # Calculate total smallholder and private production
        total_smallholder = df_selected_year['produksi_rakyat'].sum()
        total_private = df_selected_year['produksi_swasta'].sum()
        
        ownership_data = pd.DataFrame({
            'Category': ['Smallholder', 'Private Estate'],
            'Production': [total_smallholder, total_private]
        })
        
        fig = px.bar(
            ownership_data,
            x='Category',
            y='Production',
            color='Category',
            title=f"Production by Ownership Type ({selected_year})",
            color_discrete_sequence=['#1e6e50', '#2a9d8f']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Key Insights</h2>", unsafe_allow_html=True)
    st.markdown("<ul class='insights-text'>", unsafe_allow_html=True)
    st.markdown("<li>Tea production in West Java is concentrated in mountainous regions like Cianjur, Tasikmalaya, and Bandung.</li>", unsafe_allow_html=True)
    st.markdown("<li>Smallholder farms contribute significantly more to overall production than private estates.</li>", unsafe_allow_html=True)
    st.markdown("<li>Several districts show steady growth in tea production over the 2017-2024 period.</li>", unsafe_allow_html=True)
    st.markdown("<li>Private estates generally have higher productivity rates than smallholder farms.</li>", unsafe_allow_html=True)
    st.markdown("<li>15 out of 27 regions in the dataset have no tea production throughout the period.</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Production Analysis
elif app_mode == "🌱 Production Analysis":
    st.markdown("<h1 class='main-header'>Tea Production Analysis</h1>", unsafe_allow_html=True)
    
    # Filters
    st.sidebar.markdown("### Production Filters")
    production_type = st.sidebar.selectbox(
        "Select Production Type",
        ["Smallholder (Rakyat)", "Private Estate (Swasta)", "Both"]
    )
    
    # Select districts for comparison
    all_districts = sorted(list(producing_districts))
    selected_districts = st.sidebar.multiselect(
        "Select Districts to Compare",
        all_districts,
        default=all_districts[:5] if len(all_districts) >= 5 else all_districts
    )
    
    # Generate data for selected production type
    if production_type == "Smallholder (Rakyat)":
        prod_column = 'produksi_rakyat'
        title_suffix = "Smallholder"
    elif production_type == "Private Estate (Swasta)":
        prod_column = 'produksi_swasta'
        title_suffix = "Private Estate"
    else:
        # Create total production column
        df['total_production'] = df['produksi_rakyat'] + df['produksi_swasta']
        prod_column = 'total_production'
        title_suffix = "Total"
    
    # Filter data for selected districts
    if selected_districts:
        df_districts = df[df['kab_kota'].isin(selected_districts)]
    else:
        df_districts = df[df[prod_column] > 0]  # Default to all producing districts
    
    # Production analysis layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Time Series Analysis
        st.markdown(f"<h3>{title_suffix} Production Time Series (2017-2024)</h3>", unsafe_allow_html=True)
        
        # Create time series plot
        fig = go.Figure()
        
        for district in selected_districts:
            district_data = df[df['kab_kota'] == district]
            fig.add_trace(go.Scatter(
                x=district_data['tahun'],
                y=district_data[prod_column],
                mode='lines+markers',
                name=district
            ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Production (Tons)",
            legend_title="District"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Production share by district
        st.markdown(f"<h3>{title_suffix} Production Share ({selected_year})</h3>", unsafe_allow_html=True)
        
        # Filter data for the selected year
        df_year = df_districts[df_districts['tahun'] == selected_year]
        df_year = df_year.sort_values(prod_column, ascending=False)
        
        fig = px.pie(
            df_year,
            values=prod_column,
            names='kab_kota',
            color_discrete_sequence=px.colors.sequential.Greens,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Compare districts' production
        st.markdown(f"<h3>Compare {title_suffix} Production ({selected_year})</h3>", unsafe_allow_html=True)
        
        # Filter data for the selected year
        df_year = df_districts[df_districts['tahun'] == selected_year]
        df_year = df_year.sort_values(prod_column, ascending=False)
        
        fig = px.bar(
            df_year,
            x='kab_kota',
            y=prod_column,
            color=prod_column,
            color_continuous_scale='Viridis',
            title=f"{title_suffix} Production by District"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Production growth rate
        st.markdown("<h3>Production Growth Rate Analysis</h3>", unsafe_allow_html=True)
        
        # Calculate growth rates
        growth_rates = []
        
        for district in selected_districts:
            district_data = df[df['kab_kota'] == district].sort_values('tahun')
            
            if len(district_data) >= 2:
                earliest_year = district_data['tahun'].min()
                latest_year = district_data['tahun'].max()
                
                earliest_production = district_data[district_data['tahun'] == earliest_year][prod_column].values[0]
                latest_production = district_data[district_data['tahun'] == latest_year][prod_column].values[0]
                
                # Handle division by zero
                if earliest_production > 0:
                    growth_rate = ((latest_production / earliest_production) - 1) * 100
                else:
                    growth_rate = 0 if latest_production == 0 else 100  # 100% growth if starting from 0
                
                years_diff = latest_year - earliest_year
                annual_growth = growth_rate / years_diff if years_diff > 0 else 0
                
                growth_rates.append({
                    'district': district,
                    'total_growth': growth_rate,
                    'annual_growth': annual_growth,
                    'years': years_diff
                })
        
        growth_df = pd.DataFrame(growth_rates)
        if not growth_df.empty:
            growth_df = growth_df.sort_values('annual_growth', ascending=False)
            
            fig = px.bar(
                growth_df,
                x='district',
                y='annual_growth',
                color='annual_growth',
                color_continuous_scale='RdYlGn',
                title=f"Average Annual Growth Rate (%)"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data to calculate growth rates.")
    
    # Map visualization (placeholder)
    st.markdown("<h3>Geographic Distribution of Tea Production</h3>", unsafe_allow_html=True)
    plot_west_java_map(df, selected_year, prod_column)
    
    # Production insights
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Production Insights</h2>", unsafe_allow_html=True)
    st.markdown("<ul class='insights-text'>", unsafe_allow_html=True)
    st.markdown("<li>Kabupaten Cianjur and Tasikmalaya consistently lead in tea production throughout the analysis period.</li>", unsafe_allow_html=True)
    st.markdown("<li>There's significant variation in production between districts, with some producing over 12,000 tons annually while others produce less than 100 tons.</li>", unsafe_allow_html=True)
    st.markdown("<li>Tea production has generally increased in the top producing districts over the 2017-2024 period.</li>", unsafe_allow_html=True)
    st.markdown("<li>Private estate production is concentrated in fewer districts compared to smallholder production.</li>", unsafe_allow_html=True)
    st.markdown("<li>Several districts show zero production throughout the entire period, particularly in the northern and coastal regions of West Java.</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Productivity Analysis
elif app_mode == "📈 Productivity Analysis":
    st.markdown("<h1 class='main-header'>Tea Productivity Analysis</h1>", unsafe_allow_html=True)
    
    # Filters
    st.sidebar.markdown("### Productivity Filters")
    productivity_type = st.sidebar.selectbox(
        "Select Productivity Type",
        ["Smallholder (Rakyat)", "Private Estate (Swasta)", "Compare Both"]
    )
    
    # Select districts for comparison
    all_districts = sorted(list(producing_districts))
    selected_districts = st.sidebar.multiselect(
        "Select Districts to Compare",
        all_districts,
        default=all_districts[:5] if len(all_districts) >= 5 else all_districts
    )
    
    # Generate data based on selected type
    if productivity_type == "Smallholder (Rakyat)":
        prod_column = 'produktivitas_rakyat'
        title_suffix = "Smallholder"
    elif productivity_type == "Private Estate (Swasta)":
        prod_column = 'produktivitas_swasta'
        title_suffix = "Private Estate"
    else:
        # Will use both columns for comparison
        prod_column = 'produktivitas_rakyat'  # Default for filtering
        title_suffix = "Both"
    
    # Filter data for selected districts
    if selected_districts:
        df_districts = df[df['kab_kota'].isin(selected_districts)]
    else:
        df_districts = df[df[prod_column] > 0]  # Default to all producing districts
    
    # Productivity analysis layout
    if productivity_type != "Compare Both":
        col1, col2 = st.columns(2)
        
        with col1:
            # Productivity ranking
            st.markdown(f"<h3>{title_suffix} Productivity Ranking ({selected_year})</h3>", unsafe_allow_html=True)
            
            # Filter data for the selected year
            df_year = df_districts[df_districts['tahun'] == selected_year]
            df_year = df_year.sort_values(prod_column, ascending=False)
            
            fig = px.bar(
                df_year,
                x='kab_kota',
                y=prod_column,
                color=prod_column,
                color_continuous_scale='YlGn',
                title=f"{title_suffix} Productivity (kg/ha)"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top districts table
            st.markdown(f"<h3>Top Districts by {title_suffix} Productivity ({selected_year})</h3>", unsafe_allow_html=True)
            top_districts = df_year.sort_values(prod_column, ascending=False).head(5)
            top_districts_display = top_districts[['kab_kota', prod_column]].copy()
            top_districts_display.columns = ['District', 'Productivity (kg/ha)']
            st.table(top_districts_display.set_index('District'))
        
        with col2:
            # Productivity time series
            st.markdown(f"<h3>{title_suffix} Productivity Trend (2017-2024)</h3>", unsafe_allow_html=True)
            
            # Create time series plot
            fig = go.Figure()
            
            for district in selected_districts:
                district_data = df[df['kab_kota'] == district]
                fig.add_trace(go.Scatter(
                    x=district_data['tahun'],
                    y=district_data[prod_column],
                    mode='lines+markers',
                    name=district
                ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Productivity (kg/ha)",
                legend_title="District"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Relation between production and productivity
            st.markdown(f"<h3>Production vs. Productivity ({selected_year})</h3>", unsafe_allow_html=True)
            
            # Filter data for the selected year
            df_year = df_districts[df_districts['tahun'] == selected_year]
            
            # Determine production column based on productivity type
            if productivity_type == "Smallholder (Rakyat)":
                production_col = 'produksi_rakyat'
            else:
                production_col = 'produksi_swasta'
                
            # Create scatter plot
            fig = px.scatter(
                df_year,
                x=production_col,
                y=prod_column,
                color='kab_kota',
                size=production_col,
                hover_name='kab_kota',
                title=f"Production vs. Productivity Relationship"
            )
            fig.update_layout(
                xaxis_title="Production (Tons)",
                yaxis_title="Productivity (kg/ha)"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        # Compare both smallholder and private estate productivity
        st.markdown("<h3>Compare Smallholder vs. Private Estate Productivity</h3>", unsafe_allow_html=True)
        
        # Filter data for comparing
        compare_df = df_districts[df_districts['tahun'] == selected_year].copy()
        compare_df = compare_df[(compare_df['produktivitas_rakyat'] > 0) | (compare_df['produktivitas_swasta'] > 0)]
        
        # Create comparison bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=compare_df['kab_kota'],
            y=compare_df['produktivitas_rakyat'],
            name='Smallholder',
            marker_color='#1e6e50'
        ))
        
        fig.add_trace(go.Bar(
            x=compare_df['kab_kota'],
            y=compare_df['produktivitas_swasta'],
            name='Private Estate',
            marker_color='#2a9d8f'
        ))
        
        fig.update_layout(
            title=f"Productivity Comparison ({selected_year})",
            xaxis_title="District",
            yaxis_title="Productivity (kg/ha)",
            barmode='group',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Productivity ratio
        st.markdown("<h3>Productivity Ratio: Private Estate vs. Smallholder</h3>", unsafe_allow_html=True)
        
        # Calculate ratio
        ratio_df = compare_df.copy()
        ratio_df = ratio_df[(ratio_df['produktivitas_rakyat'] > 0) & (ratio_df['produktivitas_swasta'] > 0)]
        ratio_df['productivity_ratio'] = ratio_df['produktivitas_swasta'] / ratio_df['produktivitas_rakyat']
        ratio_df = ratio_df.sort_values('productivity_ratio', ascending=False)
        
        if not ratio_df.empty:
            fig = px.bar(
                ratio_df,
                x='kab_kota',
                y='productivity_ratio',
                color='productivity_ratio',
                color_continuous_scale='RdYlGn',
                title=f"Private Estate to Smallholder Productivity Ratio ({selected_year})"
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                yaxis_title="Ratio (Private/Smallholder)"
            )
            fig.add_hline(y=1, line_dash="dash", line_color="gray", annotation_text="Equal Productivity")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No districts have both smallholder and private estate productivity data for comparison.")
        
        # Trend comparison
        st.markdown("<h3>Productivity Trend Comparison (2017-2024)</h3>", unsafe_allow_html=True)
        
        # Select a district for trend comparison
        if selected_districts:
            district_for_trend = st.selectbox("Select a district for trend analysis", selected_districts)
            
            # Get data for the selected district
            district_data = df[df['kab_kota'] == district_for_trend]
            
            # Create time series comparison
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=district_data['tahun'],
                y=district_data['produktivitas_rakyat'],
                mode='lines+markers',
                name='Smallholder',
                line=dict(color='#1e6e50', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=district_data['tahun'],
                y=district_data['produktivitas_swasta'],
                mode='lines+markers',
                name='Private Estate',
                line=dict(color='#2a9d8f', width=2)
            ))
            
            fig.update_layout(
                title=f"Productivity Trend in {district_for_trend}",
                xaxis_title="Year",
                yaxis_title="Productivity (kg/ha)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select at least one district for trend comparison.")
            # Load data
    @st.cache_data
    def load_data():
        kebun_total = pd.read_csv('perkebunan_teh.csv')
        
        # Clean the data
        for col in ['produktivitas_rakyat', 'produktivitas_swasta']:
            kebun_total[col] = pd.to_numeric(kebun_total[col], errors='coerce')
        
        kebun_total['produktivitas_rakyat'] = kebun_total['produktivitas_rakyat'].replace(0, np.nan)
        kebun_total['produktivitas_swasta'] = kebun_total['produktivitas_swasta'].replace(0, np.nan)
        
        return kebun_total

    # Load GeoJSON for West Java (simplified version for performance)
    @st.cache_data
    def load_geojson():
        west_java_districts = {
            "type": "FeatureCollection",
            "features": []
        }
        
        regencies = [
            "KABUPATEN BOGOR", "KABUPATEN SUKABUMI", "KABUPATEN CIANJUR", 
            "KABUPATEN BANDUNG", "KABUPATEN GARUT", "KABUPATEN TASIKMALAYA",
            "KABUPATEN CIAMIS", "KABUPATEN KUNINGAN", "KABUPATEN CIREBON",
            "KABUPATEN MAJALENGKA", "KABUPATEN SUMEDANG", "KABUPATEN INDRAMAYU",
            "KABUPATEN SUBANG", "KABUPATEN PURWAKARTA", "KABUPATEN KARAWANG",
            "KABUPATEN BEKASI", "KABUPATEN BANDUNG BARAT", "KABUPATEN PANGANDARAN",
            "KOTA BOGOR", "KOTA SUKABUMI", "KOTA BANDUNG", "KOTA CIREBON",
            "KOTA BEKASI", "KOTA DEPOK", "KOTA CIMAHI", "KOTA TASIKMALAYA", "KOTA BANJAR"
        ]
        
        for i, regency in enumerate(regencies):
            row = i // 5
            col = i % 5
            coords = [
                [106.0 + col * 0.5, -6.0 - row * 0.5],
                [106.0 + col * 0.5 + 0.4, -6.0 - row * 0.5],
                [106.0 + col * 0.5 + 0.4, -6.0 - row * 0.5 - 0.4],
                [106.0 + col * 0.5, -6.0 - row * 0.5 - 0.4],
                [106.0 + col * 0.5, -6.0 - row * 0.5]
            ]
            
            feature = {
                "type": "Feature",
                "properties": {"KABKOT": regency},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            }
            
            west_java_districts["features"].append(feature)
        
        return west_java_districts

    # Load data
    kebun_total = load_data()
    geojson_data = load_geojson()

    # Sidebar filter
    st.sidebar.header("Filter Options")
    year = st.sidebar.selectbox(
        "Select Year",
        sorted(kebun_total['tahun'].unique()),
        index=len(kebun_total['tahun'].unique()) - 1
    )

    filtered_data = kebun_total[kebun_total['tahun'] == year].copy()
    filtered_data['produktivitas_difference'] = filtered_data['produktivitas_swasta'] - filtered_data['produktivitas_rakyat']
    filtered_data_geojson = filtered_data.copy()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Smallholder Productivity", "Private Estate Productivity", "Productivity Comparison"])

    with tab1:
        st.header(f"Smallholder Tea Productivity in {year}")
        fig1 = px.choropleth_mapbox(
            filtered_data_geojson,
            geojson=geojson_data,
            locations='kab_kota',
            featureidkey="properties.KABKOT",
            color='produktivitas_rakyat',
            color_continuous_scale="Viridis",
            range_color=[0, filtered_data_geojson['produktivitas_rakyat'].max()],
            mapbox_style="carto-positron",
            zoom=7,
            center={"lat": -7.0, "lon": 107.5},
            opacity=0.7,
            labels={'produktivitas_rakyat': 'Productivity (kg/ha)'}
        )
        fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Smallholder Tea Productivity Data")
        display_data1 = filtered_data_geojson[['kab_kota', 'produktivitas_rakyat']].sort_values(by='produktivitas_rakyat', ascending=False)
        display_data1 = display_data1[display_data1['produktivitas_rakyat'] > 0]
        display_data1.columns = ['District/City', 'Productivity (kg/ha)']
        st.dataframe(display_data1, use_container_width=True)

    with tab2:
        st.header(f"Private Estate Tea Productivity in {year}")
        fig2 = px.choropleth_mapbox(
            filtered_data_geojson,
            geojson=geojson_data,
            locations='kab_kota',
            featureidkey="properties.KABKOT",
            color='produktivitas_swasta',
            color_continuous_scale="Plasma",
            range_color=[0, filtered_data_geojson['produktivitas_swasta'].max()],
            mapbox_style="carto-positron",
            zoom=7,
            center={"lat": -7.0, "lon": 107.5},
            opacity=0.7,
            labels={'produktivitas_swasta': 'Productivity (kg/ha)'}
        )
        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Private Estate Tea Productivity Data")
        display_data2 = filtered_data_geojson[['kab_kota', 'produktivitas_swasta']].sort_values(by='produktivitas_swasta', ascending=False)
        display_data2 = display_data2[display_data2['produktivitas_swasta'] > 0]
        display_data2.columns = ['District/City', 'Productivity (kg/ha)']
        st.dataframe(display_data2, use_container_width=True)

    with tab3:
        st.header(f"Productivity Comparison in {year}")
        col1, col2 = st.columns(2)

        with col1:
            comparison_data = filtered_data_geojson[
                (filtered_data_geojson['produktivitas_rakyat'] > 0) | 
                (filtered_data_geojson['produktivitas_swasta'] > 0)
            ].copy()
            
            if not comparison_data.empty:
                chart_data = []
                for _, row in comparison_data.iterrows():
                    if pd.notna(row['produktivitas_rakyat']):
                        chart_data.append({
                            'kab_kota': row['kab_kota'],
                            'Productivity': row['produktivitas_rakyat'],
                            'Type': 'Smallholder'
                        })
                    if pd.notna(row['produktivitas_swasta']):
                        chart_data.append({
                            'kab_kota': row['kab_kota'],
                            'Productivity': row['produktivitas_swasta'],
                            'Type': 'Private Estate'
                        })
                chart_df = pd.DataFrame(chart_data)
                fig3 = px.bar(
                    chart_df,
                    x='kab_kota',
                    y='Productivity',
                    color='Type',
                    barmode='group',
                    title='Productivity Comparison by District',
                    labels={
                        'kab_kota': 'District/City',
                        'Productivity': 'Productivity (kg/ha)'
                    }
                )
                fig3.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No comparison data available for the selected year.")

        with col2:
            fig4 = px.choropleth_mapbox(
                filtered_data_geojson,
                geojson=geojson_data,
                locations='kab_kota',
                featureidkey="properties.KABKOT",
                color='produktivitas_difference',
                color_continuous_scale="RdBu",
                range_color=[-1000, 1000],
                mapbox_style="carto-positron",
                zoom=7,
                center={"lat": -7.0, "lon": 107.5},
                opacity=0.7,
                labels={'produktivitas_difference': 'Productivity Difference (kg/ha)'}
            )
            fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=400)
            st.plotly_chart(fig4, use_container_width=True)
            st.caption("Productivity Difference = Private Estate - Smallholder")
            st.caption("Blue areas: Private estates have higher productivity")
            st.caption("Red areas: Smallholders have higher productivity")

    # Summary Statistics
    st.header("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    valid_rakyat = filtered_data['produktivitas_rakyat'].dropna()
    valid_swasta = filtered_data['produktivitas_swasta'].dropna()

    with col1:
        st.metric(
            "Average Smallholder Productivity", 
            f"{valid_rakyat.mean():.1f} kg/ha" if not valid_rakyat.empty else "No data"
        )
    with col2:
        st.metric(
            "Average Private Estate Productivity", 
            f"{valid_swasta.mean():.1f} kg/ha" if not valid_swasta.empty else "No data"
        )
    with col3:
        if not valid_rakyat.empty and not valid_swasta.empty:
            diff = valid_swasta.mean() - valid_rakyat.mean()
            st.metric(
                "Productivity Gap", 
                f"{diff:.1f} kg/ha",
                delta=f"{diff:.1f} kg/ha"
            )
        else:
            st.metric("Productivity Gap", "No data")

    # Trend analysis
    st.header("Productivity Trends (2017-2024)")
    trend_data = kebun_total.groupby('tahun')[['produktivitas_rakyat', 'produktivitas_swasta']].mean().reset_index()
    fig_trend = px.line(
        trend_data, 
        x='tahun', 
        y=['produktivitas_rakyat', 'produktivitas_swasta'],
        labels={
            'tahun': 'Year',
            'value': 'Average Productivity (kg/ha)',
            'variable': 'Plantation Type'
        },
        title='Average Tea Productivity Trends in West Java',
        markers=True
    )
    fig_trend.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis_title='Average Productivity (kg/ha)',
        legend_title='Plantation Type',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_trend.for_each_trace(lambda t: t.update(
        name='Smallholder' if t.name == 'produktivitas_rakyat' else 'Private Estate',
        legendgroup='Smallholder' if t.name == 'produktivitas_rakyat' else 'Private Estate',
    ))
    st.plotly_chart(fig_trend, use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("Data source: West Java Tea Plantation Statistics (2017-2024)")
    st.caption("Note: The map visualization uses simplified district boundaries for demonstration purposes.")