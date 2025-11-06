import requests
import pandas as pd
import os
from datetime import datetime
import sys
sys.path.append('.')
from config.settings import *

def fetch_backlink_data_rapidapi():
    """Fetch backlink data from RapidAPI's SEO tools"""
    
    url = "https://seo-api7.p.rapidapi.com/backlinks"
    
    querystring = {"domain": TARGET_DOMAIN}
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "seo-api7.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching from RapidAPI: {e}")
        return None

def fetch_moz_data():
    """Fetch basic data from Moz free checker"""
    
    url = f"https://moz.com/link-explorer?q={TARGET_DOMAIN}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        return {
            'domain_authority': 'N/A',
            'page_authority': 'N/A',
            'note': 'Free tier - limited data'
        }
    except Exception as e:
        print(f"Error fetching Moz data: {e}")
        return None

def collect_all_data():
    """Main function to collect data from all sources"""
    
    print(f"Collecting backlink data for {TARGET_DOMAIN}...")
    
    # Fetch from different sources
    rapidapi_data = fetch_backlink_data_rapidapi()
    moz_data = fetch_moz_data()
    
    # Compile into structured format
    current_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'domain': TARGET_DOMAIN,
        'total_backlinks': rapidapi_data.get('total_backlinks', 0) if rapidapi_data else 0,
        'referring_domains': rapidapi_data.get('referring_domains', 0) if rapidapi_data else 0,
        'new_backlinks': rapidapi_data.get('new_backlinks', 0) if rapidapi_data else 0,
        'lost_backlinks': rapidapi_data.get('lost_backlinks', 0) if rapidapi_data else 0,
        'domain_authority': moz_data.get('domain_authority', 'N/A') if moz_data else 'N/A',
        'data_source': 'RapidAPI + Moz'
    }
    
    return current_data

def save_to_history(data):
    """Append current data to historical CSV"""
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    df_new = pd.DataFrame([data])
    
    if os.path.exists(HISTORY_FILE):
        df_existing = pd.read_csv(HISTORY_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    df_combined.to_csv(HISTORY_FILE, index=False)
    print(f"Data saved to {HISTORY_FILE}")
    
    return df_combined

if __name__ == "__main__":
    data = collect_all_data()
    print(f"Collected data: {data}")
    
    history_df = save_to_history(data)
    print(f"Total records in history: {len(history_df)}")
