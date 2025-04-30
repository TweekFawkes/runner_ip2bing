import argparse
import socket
import sys
# import webbrowser # Add webbrowser import
from curl_cffi import requests # Use curl_cffi
import datetime # Add datetime import
import os       # Add os import

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###


def main():
    parser = argparse.ArgumentParser(description="Fetch Bing search results for 'ip:<IP_ADDRESS>' and save HTML.") # Update description
    # Use a positional argument for the IP address
    parser.add_argument('ip_address', help='IP Address to search for on Bing (e.g., 8.8.8.8)') # Update help
    args = parser.parse_args()

    ip_address = args.ip_address

    # Basic IP format validation (optional but recommended)
    # Add more robust validation if needed (e.g., using ipaddress module)
    if '.' not in ip_address and ':' not in ip_address:
         print(f"[!] Error: '{ip_address}' does not look like a valid IPv4 or IPv6 address.", file=sys.stderr)
         return 1 # Keep exit code for invalid format

    # Define outputs directory
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True) # Create directory if it doesn't exist

    # Construct the Bing search URL
    search_query = f"ip:{ip_address}"
    bing_url = f"https://www.bing.com/search?q={search_query}" # Basic URL encoding might be needed for complex cases, but fine for IP addresses

    print(f"[*] Fetching Bing search results for: {search_query}") # Update message
    print(f"[*] URL: {bing_url}")

    try:
        # Make the request using curl_cffi
        response = requests.get(bing_url, impersonate="chrome110") # Use requests.get
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        print(f"[+] Successfully fetched URL. Status code: {response.status_code}")

        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # Replace ':' with '_' in IPv6 addresses for valid filenames
        safe_ip = ip_address.replace(':', '_')
        filename = f"{timestamp}-ip_{safe_ip}.html"
        filepath = os.path.join(output_dir, filename)

        # Save the HTML content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"[*] Saved HTML results to: {filepath}")

        # Optional: Print page title or snippet if needed
        # print(f"[*] Page Title: {response.text[response.text.find('<title>')+7:response.text.find('</title>')]...}") # Example
        return 0 # Success
    except requests.errors.RequestsError as e: # Catch curl_cffi specific errors
        print(f"[!] Error fetching URL: {e}", file=sys.stderr)
        return 1 # Failure
    except Exception as e: # Catch other potential errors
        print(f"[!] An unexpected error occurred: {e}", file=sys.stderr)
        return 1 # Failure


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

if __name__ == "__main__":
    # Use sys.exit() to ensure the exit code is propagated correctly
    sys.exit(main())