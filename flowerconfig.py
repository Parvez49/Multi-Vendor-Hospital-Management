import os

# Broker URL (Celery broker URL)
BROKER_URL = "redis://redis:6379/0"

# Broker user and password (if needed)
# BROKER_USER = 'your_broker_username'
# BROKER_PASSWORD = 'your_broker_password'

# Basic authentication (optional)
# BASIC_AUTH = ["your_username:your_password"]

# Port for Flower web interface
PORT = 5555

# Specify the Celery app to monitor (your Django project Celery app name)
CELERY_APP = "Multi_Vendor_Hospital_System.celery"

# Enable real-time updates (WebSocket)
# Uncomment the following line to enable real-time updates
# WEBUI_OPTIONS = {'enable_realtime_stats': True}


# flower --config=flowerconfig.py
