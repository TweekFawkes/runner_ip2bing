import argparse
# import socket # No longer needed for API call
import sys
# from curl_cffi import requests # Use curl_cffi
import requests # Use standard requests library
import datetime # Add datetime import
import os       # Add os import
import json     # Add json import

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

# Bing Search API v7 endpoint
BING_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

def main():
    parser = argparse.ArgumentParser(description="Query Bing Web Search API for 'ip:<IP_ADDRESS>' and save JSON response.")
    # Required arguments
    # parser.add_argument('ip_address', help='IP Address to search for on Bing (e.g., 8.8.8.8)') # Old positional arg
    parser.add_argument('--ip_address', required=True, help='IP Address to search for on Bing (e.g., 8.8.8.8)') # New named arg
    # parser.add_argument('--api-key', required=True, help='Your Bing Search API v7 subscription key.') # Old name
    parser.add_argument('--api_key', required=True, help='Your Bing Search API v7 subscription key.') # New name
    args = parser.parse_args()

    ip_address = args.ip_address
    api_key = args.api_key # Get API key from args (attribute name matches dest)

    # --- Get API Key --- (Removed environment variable logic)
    # api_key = os.environ.get("BING_API_KEY")
    # if not api_key:
    #     print("[!] Error: BING_API_KEY environment variable not set.", file=sys.stderr)
    #     print("[*] Please set the BING_API_KEY environment variable with your Bing Search API subscription key.", file=sys.stderr)
    #     return 1

    # Basic IP format validation (optional but recommended)
    # Add more robust validation if needed (e.g., using ipaddress module)
    if '.' not in ip_address and ':' not in ip_address:
         print(f"[!] Error: '{ip_address}' does not look like a valid IPv4 or IPv6 address.", file=sys.stderr)
         return 1 # Keep exit code for invalid format

    # Define outputs directory
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True) # Create directory if it doesn't exist

    # Construct the API request details
    search_query = f"ip:{ip_address}"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": search_query, "textDecorations": True, "textFormat": "HTML"} # Example params, adjust as needed

    print(f"[*] Querying Bing Web Search API for: {search_query}")
    print(f"[*] API Endpoint: {BING_API_ENDPOINT}")

    try:
        # Make the API request using requests library
        response = requests.get(BING_API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        print(f"[+] Successfully queried API. Status code: {response.status_code}")

        # Parse the JSON response
        search_results = response.json()

        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # Replace ':' with '_' in IPv6 addresses for valid filenames
        safe_ip = ip_address.replace(':', '_')
        filename = f"{timestamp}-ip_{safe_ip}.json" # Save as JSON
        filepath = os.path.join(output_dir, filename)

        # Save the JSON content
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4) # Save formatted JSON
        print(f"[*] Saved JSON response to: {filepath}")

        # Optional: Print specific parts of the response, e.g., number of results
        # if 'webPages' in search_results and 'value' in search_results['webPages']:
        #    print(f"[*] Found {len(search_results['webPages']['value'])} web results.")

        return 0 # Success
    except requests.exceptions.RequestException as e: # Catch requests library errors
        print(f"[!] Error during API request: {e}", file=sys.stderr)
        # Attempt to parse error details from response if available
        try:
            error_details = response.json()
            print(f"[!] API Error Details: {json.dumps(error_details, indent=2)}", file=sys.stderr)
        except (AttributeError, json.JSONDecodeError):
             # Handle cases where response might not exist or isn't valid JSON
             pass # Error already printed above
        return 1 # Failure
    except json.JSONDecodeError as e:
        print(f"[!] Error parsing JSON response: {e}", file=sys.stderr)
        print(f"[*] Raw response text: {response.text[:500]}...", file=sys.stderr) # Show beginning of text
        return 1 # Failure
    except Exception as e: # Catch other potential errors
        print(f"[!] An unexpected error occurred: {e}", file=sys.stderr)
        return 1 # Failure


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

if __name__ == "__main__":
    # Use sys.exit() to ensure the exit code is propagated correctly
    sys.exit(main())