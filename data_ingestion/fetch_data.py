import requests

def fetch_market_data(api_url, params=None):
    """
    Fetch market data from the specified API.

    Args:
        api_url (str): The API endpoint URL.
        params (dict): Optional parameters for the API request.

    Returns:
        dict: JSON response from the API.
    """
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
