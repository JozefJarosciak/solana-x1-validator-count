import pandas as pd
from solana.rpc.api import Client
import time
from tabulate import tabulate

class Config:
    SOLANA_ENDPOINTS = {
        "Solana Devnet": "https://api.devnet.solana.com",  # Solana development network endpoint
        "Solana Testnet": "https://api.testnet.solana.com",  # Solana testing network endpoint
        "Solana Mainnet": "https://api.mainnet-beta.solana.com",  # Solana mainnet endpoint
        "X1 Testnet": "https://xolana.xen.network"  # X1 testnet endpoint
    }
    RETRIES = 3  # Number of retry attempts for failed requests (default: 3)
    DELAY = 2  # Delay between retries in seconds (default: 2)

def get_validators_breakdown(endpoint):
    for attempt in range(Config.RETRIES):
        try:
            client = Client(endpoint)
            response = client.get_vote_accounts()
            current_validators = response.value.current
            delinquent_validators = response.value.delinquent
            active_count = len([validator for validator in current_validators if float(validator.activated_stake) > 0])
            inactive_count = len(delinquent_validators)
            return active_count, inactive_count
        except Exception as e:
            if attempt < Config.RETRIES - 1:
                time.sleep(Config.DELAY)
            else:
                print(f"Failed to fetch data from {endpoint} after {Config.RETRIES} attempts.")
                return "Error", "Error"

def main():
    # Fetch and process validator breakdown for each Solana network
    data = []
    for network_name, url in Config.SOLANA_ENDPOINTS.items():
        active, inactive = get_validators_breakdown(url)
        total = active + inactive if isinstance(active, int) and isinstance(inactive, int) else "Error"
        data.append({
            "Network": network_name,
            "Active Validators": active,
            "Inactive Validators": inactive,
            "Total": total
        })
    # Create a pandas DataFrame from the collected data
    df = pd.DataFrame(data)
    # Display the formatted table
    print()
    tabulate_df = tabulate(df, headers="keys", tablefmt="grid", showindex=False)  # Format the DataFrame as a table using tabulate
    print(tabulate_df)  # Print the formatted table

if __name__ == "__main__":
    main()