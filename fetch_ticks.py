import urllib.request
import json
import os
from datetime import datetime

# Target NSE Tickers (Add as many as you need)
TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "^NSEI"] 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
}

def fetch_and_process():
    # Create the output directory which will be served by GitHub Pages
    output_dir = 'public_data'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting data fetch at {datetime.now().isoformat()}...")

    for ticker in TICKERS:
        print(f"Fetching {ticker}...")
        # 1m interval, 7d range (Maximum allowed for 1m data on Yahoo)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=7d"
        
        req = urllib.request.Request(url, headers=HEADERS)
        
        try:
            with urllib.request.urlopen(req) as response:
                raw_data = json.loads(response.read().decode())
                
                # Check for valid data
                if not raw_data['chart']['result']:
                    print(f"No data returned for {ticker}.")
                    continue

                result = raw_data['chart']['result'][0]
                timestamps = result.get('timestamp', [])
                indicators = result['indicators']['quote'][0]
                
                # Compress into a flat structure (Array of Structs style for Zig)
                clean_data = {
                    "symbol": ticker,
                    "t": timestamps,
                    "o": indicators.get('open', []),
                    "h": indicators.get('high', []),
                    "l": indicators.get('low', []),
                    "c": indicators.get('close', []),
                    "v": indicators.get('volume', [])
                }
                
                # Save as minified JSON to save bandwidth
                file_path = os.path.join(output_dir, f"{ticker}.json")
                with open(file_path, 'w') as f:
                    json.dump(clean_data, f, separators=(',', ':'))
                    
                print(f"Successfully saved {ticker}.json")
                    
        except Exception as e:
            print(f"Failed to fetch {ticker}: {str(e)}")

if __name__ == "__main__":
    fetch_and_process()
    print("Market Data Engine complete.")
