import pandas as pd
import plotly.graph_objects as go
from jinja2 import Template
import os
import sys
sys.path.append('.')
from config.settings import *

def load_historical_data():
    """Load historical backlink data"""
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        print("No historical data found")
        return pd.DataFrame()

def create_backlink_trend_chart(df):
    """Create backlink growth trend chart"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_backlinks'],
        mode='lines+markers',
        name='Total Backlinks',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['referring_domains'],
        mode='lines+markers',
        name='Referring Domains',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Backlink Growth Over Time',
        xaxis_title='Date',
        yaxis_title='Count',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_new_vs_lost_chart(df):
    """Create new vs lost backlinks chart"""
    
    df_recent = df.tail(6)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_recent['date'],
        y=df_recent['new_backlinks'],
        name='New Backlinks',
        marker_color='#10b981'
    ))
    
    fig.add_trace(go.Bar(
        x=df_recent['date'],
        y=df_recent['lost_backlinks'],
        name='Lost Backlinks',
        marker_color='#ef4444'
    ))
    
    fig.update_layout(
        title='New vs Lost Backlinks (Last 6 Months)',
        xaxis_title='Date',
        yaxis_title='Count',
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def calculate_metrics(df):
    """Calculate key metrics from historical data"""
    
    if len(df) < 2:
        return {
            'current_backlinks': int(df['total_backlinks'].iloc[-1]) if len(df) > 0 else 0,
            'current_domains': int(df['referring_domains'].iloc[-1]) if len(df) > 0 else 0,
            'monthly_change': 0,
            'percent_change': 0,
            'new_this_month': int(df['new_backlinks'].iloc[-1]) if len(df) > 0 else 0,
            'lost_this_month': int(df['lost_backlinks'].iloc[-1]) if len(df) > 0 else 0,
            'domain_authority': df['domain_authority'].iloc[-1] if len(df) > 0 else 'N/A'
        }
    
    current = df.iloc[-1]
    previous = df.iloc[-2]
    
    change = current['total_backlinks'] - previous['total_backlinks']
    percent = (change / previous['total_backlinks'] * 100) if previous['total_backlinks'] > 0 else 0
    
    return {
        'current_backlinks': int(current['total_backlinks']),
        'current_domains': int(current['referring_domains']),
        'monthly_change': int(change),
        'percent_change': round(percent, 2),
        'new_this_month': int(current['new_backlinks']),
        'lost_this_month': int(current['lost_backlinks']),
        'domain_authority': current['domain_authority']
    }

def generate_html_report(df, metrics, trend_chart, new_lost_chart):
    """Generate HTML report using template"""
    
    template_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ report_title }}</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 32px;
            }
            .header p {
                margin: 10px 0 0 0;
                opacity: 0.9;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .metric-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .metric-label {
                font-size: 14px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 10px;
            }
            .metric-value {
                font-size: 36px;
                font-weight: bold;
                color: #333;
            }
            .metric-change {
                font-size: 14px;
                margin-top: 5px;
            }
            .positive {
                color: #10b981;
            }
            .negative {
                color: #ef4444;
            }
            .chart-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .footer {
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{ report_title }}</h1>
            <p>Domain: {{ domain }} | Generated: {{ date }}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Backlinks</div>
                <div class="metric-value">{{ metrics.current_backlinks }}</div>
                <div class="metric-change {% if metrics.monthly_change >= 0 %}positive{% else %}negative{% endif %}">
                    {% if metrics.monthly_change >= 0 %}▲{% else %}▼{% endif %} 
                    {{ metrics.monthly_change }} ({{ metrics.percent_change }}%) this month
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Referring Domains</div>
                <div class="metric-value">{{ metrics.current_domains }}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">New Backlinks</div>
                <div class="metric-value positive">{{ metrics.new_this_month }}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Lost Backlinks</div>
                <div class="metric-value negative">{{ metrics.lost_this_month }}</div>
            </div>
        </div>
        
        <div class="chart-container">
            {{ trend_chart|safe }}
        </div>
        
        <div class="chart-container">
            {{ new_lost_chart|safe }}
        </div>
        
        <div class="footer">
            <p>This report was automatically generated by your backlink monitoring system.</p>
            <p>Data sources: RapidAPI SEO Tools, Moz Link Explorer</p>
        </div>
    </body>
    </html>
    """
    
    template = Template(template_html)
    
    html_content = template.render(
        report_title=REPORT_TITLE,
        domain=TARGET_DOMAIN,
        date=CURRENT_DATE,
        metrics=metrics,
        trend_chart=trend_chart,
        new_lost_chart=new_lost_chart
    )
    
    return html_content

def save_report(html_content):
    """Save HTML report to file"""
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    with open(REPORT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Report saved to {REPORT_FILENAME}")
    return REPORT_FILENAME

if __name__ == "__main__":
    print("Generating report...")
    
    df = load_historical_data()
    
    if df.empty:
        print("No data available to generate report")
        exit(1)
    
    metrics = calculate_metrics(df)
    
    trend_chart = create_backlink_trend_chart(df)
    new_lost_chart = create_new_vs_lost_chart(df)
    
    html_content = generate_html_report(df, metrics, trend_chart, new_lost_chart)
    
    report_path = save_report(html_content)
    print(f"Report generated successfully: {report_path}")
