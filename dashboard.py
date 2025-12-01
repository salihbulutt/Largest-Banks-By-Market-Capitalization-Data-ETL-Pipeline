# Simple Dashboard using Plotly
# This creates an interactive HTML dashboard from your ETL data

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Read the data from CSV
df = pd.read_csv('Largest_banks_data.csv')

# Remove index column if exists
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1)

# Create a dashboard with multiple charts
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('Top 10 Banks by Market Cap (USD)', 
                    'Market Cap in Different Currencies',
                    'Market Share Distribution', 
                    'Currency Comparison',
                    'Top 5 Banks Detailed View',
                    'Market Cap Statistics'),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "pie"}, {"type": "bar"}],
           [{"type": "table"}, {"type": "indicator"}]],
    row_heights=[0.35, 0.35, 0.3],
    vertical_spacing=0.15,
    horizontal_spacing=0.12
)

# Chart 1: Top 10 Banks Bar Chart (USD)
fig.add_trace(
    go.Bar(x=df['Name'][:10], 
           y=df['MC_USD_Billion'][:10],
           marker_color='rgb(55, 83, 109)',
           name='USD'),
    row=1, col=1
)

# Chart 2: Currency Comparison for Top 5 Banks
top_5 = df.head(5)
fig.add_trace(
    go.Bar(x=top_5['Name'], y=top_5['MC_USD_Billion'], 
           name='USD', marker_color='#3b82f6'),
    row=1, col=2
)
fig.add_trace(
    go.Bar(x=top_5['Name'], y=top_5['MC_GBP_Billion'], 
           name='GBP', marker_color='#8b5cf6'),
    row=1, col=2
)
fig.add_trace(
    go.Bar(x=top_5['Name'], y=top_5['MC_EUR_Billion'], 
           name='EUR', marker_color='#ec4899'),
    row=1, col=2
)

# Chart 3: Pie Chart - Market Share
fig.add_trace(
    go.Pie(labels=df['Name'][:10], 
           values=df['MC_USD_Billion'][:10],
           hole=0.3),
    row=2, col=1
)

# Chart 4: All Banks in USD (Horizontal Bar)
fig.add_trace(
    go.Bar(y=df['Name'], 
           x=df['MC_USD_Billion'],
           orientation='h',
           marker_color='rgb(26, 118, 255)',
           name='All Banks'),
    row=2, col=2
)

# Chart 5: Data Table - Top 5 Banks
fig.add_trace(
    go.Table(
        header=dict(values=['Rank', 'Bank Name', 'USD (B)', 'GBP (B)', 'EUR (B)', 'INR (B)'],
                    fill_color='rgb(55, 83, 109)',
                    align='left',
                    font=dict(color='white', size=12)),
        cells=dict(values=[
            list(range(1, 6)),
            top_5['Name'],
            top_5['MC_USD_Billion'],
            top_5['MC_GBP_Billion'],
            top_5['MC_EUR_Billion'],
            top_5['MC_INR_Billion']
        ],
        fill_color='lavender',
        align='left')
    ),
    row=3, col=1
)

# Chart 6: Statistics Indicator
total_market_cap = df['MC_USD_Billion'].sum()
average_market_cap = df['MC_USD_Billion'].mean()

fig.add_trace(
    go.Indicator(
        mode = "number+delta",
        value = total_market_cap,
        title = {"text": "Total Market Cap (USD Billion)"},
        delta = {'reference': average_market_cap, 'relative': False},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ),
    row=3, col=2
)

# Update layout
fig.update_layout(
    title_text="Largest Banks Dashboard - ETL Pipeline Analytics",
    title_font_size=24,
    showlegend=True,
    height=1600,
    template='plotly_white'
)

# Update x-axis labels - rotate and add more space
fig.update_xaxes(tickangle=-45, row=1, col=1, tickfont=dict(size=10))
fig.update_xaxes(tickangle=-45, row=1, col=2, tickfont=dict(size=10))
fig.update_yaxes(tickangle=0, row=2, col=2, tickfont=dict(size=9))

# Add margins to prevent label cutoff
fig.update_layout(
    margin=dict(l=100, r=50, t=100, b=150)
)

# Save as HTML file
output_file = 'dashboard.html'
fig.write_html(output_file)

print("SUCCESS: Dashboard created successfully!")
print(f"NEXT STEP: Open '{output_file}' in your web browser to view the dashboard")
print(f"FILE LOCATION: {output_file}")