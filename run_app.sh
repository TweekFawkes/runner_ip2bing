#!/bin/bash

# IMPORTANT: Replace <YOUR_API_KEY_HERE> with your actual Bing API Key
API_KEY="<YOUR_API_KEY_HERE>"

if [ "$API_KEY" == "<YOUR_API_KEY_HERE>" ]; then
    echo "Error: Please replace <YOUR_API_KEY_HERE> in run_app.sh with your Bing API key."
    exit 1
fi

python app.py --ip_address 34.209.82.230 --api_key "$API_KEY"
read -p "Press Enter to continue..."

python app.py --ip_address 65.130.44.199 --api_key "$API_KEY"
read -p "Press Enter to continue..."

# Add more test IPs here if needed
