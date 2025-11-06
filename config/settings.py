import os
from datetime import datetime

# Domain to monitor
TARGET_DOMAIN = os.getenv('TARGET_DOMAIN', 'example.com')

# Email settings
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_TO = os.getenv('EMAIL_TO')

# API Keys
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

# Paths
DATA_DIR = 'data'
REPORTS_DIR = 'reports'
HISTORY_FILE = f'{DATA_DIR}/backlinks_history.csv'

# Report settings
REPORT_TITLE = f'Monthly Backlink Report - {TARGET_DOMAIN}'
CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
REPORT_FILENAME = f'{REPORTS_DIR}/backlink_report_{CURRENT_DATE}.html'
