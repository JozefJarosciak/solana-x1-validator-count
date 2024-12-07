# Importing Libraries
import pandas as pd  # Import the pandas library for data manipulation
from solana.rpc.api import Client  # Import the Solana RPC client API
import time  # Import the time library for implementing delays
from tabulate import tabulate  # Import the tabulate function from the tabulate module

# Config Settings
class Config:
    """
    A class to store configuration settings.
    """
    SOLANA_ENDPOINTS = {
        "Solana Devnet": "https://api.devnet.solana.com",  # Solana development network endpoint
        "Solana Testnet": "https://api.testnet.solana.com",  # Solana testing network endpoint
        "Solana Mainnet": "https://api.mainnet-beta.solana.com",  # Solana mainnet endpoint
        "X1 Testnet": "https://xolana.xen.network"  # X1 testnet endpoint
    }

    RETRIES = 3  # Number of retry attempts for failed requests (default: 3)
    DELAY = 2  # Delay between retries in seconds (default: 2)

def get_validators_breakdown(endpoint):
    """
    Fetches validator breakdown with retry logic.

    Args:
        endpoint (str): The RPC endpoint to query.

    Returns:
        Tuple[int, int]: Active and inactive validator counts.
    """
    for attempt in range(Config.RETRIES):
        try:
            # Create a new Solana client instance
            client = Client(endpoint)

            # Fetch vote accounts from the Solana cluster
            response = client.get_vote_accounts()

            # Access the current and delinquent validators
            current_validators = response.value.current  # Current validators
            delinquent_validators = response.value.delinquent  # Delinquent validators

            # Count active and inactive validators
            active_count = len([validator for validator in current_validators if float(validator.activated_stake) > 0])  # Active validators count
            inactive_count = len(delinquent_validators)  # Inactive validators count

            return active_count, inactive_count  # Return the active and inactive counts
        except Exception as e:
            # Retry logic for failed requests
            if attempt < Config.RETRIES - 1:
                time.sleep(Config.DELAY)  # Pause for the specified delay before retrying
            else:
                print(f"Failed to fetch data from {endpoint} after {Config.RETRIES} attempts.")  # Print an error message
                return "Error", "Error"  # Return an error tuple

def main():
    """
    The main function that executes when running the script.
    """
    # Fetch and process validator breakdown for each Solana network
    data = []
    for network_name, url in Config.SOLANA_ENDPOINTS.items():  # Iterate through the configured endpoints
        active, inactive = get_validators_breakdown(url)  # Get the active and inactive counts for the current endpoint
        total = active + inactive if isinstance(active, int) and isinstance(inactive, int) else "Error"  # Calculate the total count (if possible)
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
    main()  # Run the main function when executing the script directly (not imported)