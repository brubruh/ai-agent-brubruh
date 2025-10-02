import requests
import os
import json
import logging
from requests.exceptions import RequestException, Timeout, ConnectionError

#USED CLASH ROYAL FOR MY API EXERCISE
# This is because I already have experience with this API and it was easier to set up since
#  1. Already have an account and keys, 
#  2. I am well informed about the game and was able to pull my own accounts data. 
# Keys are registered via ip address and not email, so no personal info is shared.



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
def load_env_file():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        logger.info("Successfully loaded .env file")
    except FileNotFoundError:
        logger.error(".env file not found")
        return False
    except Exception as e:
        logger.error(f"Error loading .env file: {e}")
        return False
    return True

def get_clash_royale_cards():
    """
    Get list of all Clash Royale cards
    This is a simple endpoint that doesn't require player tags
    """
    # Load environment variables
    if not load_env_file():
        return None
    
    api_key = os.getenv('CLASH_ROYAL_API_KEY')
    if not api_key:
        logger.error("CLASH_ROYAL_API_KEY not found in environment variables")
        return None
    
    url = "https://api.clashroyale.com/v1/cards"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    
    try:
        logger.info(f"Making request to Clash Royale API: {url}")
        logger.info("Using API key from .env file")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ Successfully connected to Clash Royale API!")
            data = response.json()
            return data
        elif response.status_code == 403:
            logger.error("❌ API key is invalid or access is forbidden")
            logger.error("Please check your API key in the .env file")
            return None
        elif response.status_code == 429:
            logger.error("❌ Rate limit exceeded - too many requests")
            return None
        else:
            logger.error(f"❌ HTTP Error: {response.status_code} - {response.reason}")
            try:
                error_data = response.json()
                logger.error(f"Error details: {error_data}")
            except:
                pass
            return None
    
    except Timeout:
        logger.error("❌ Request timed out after 10 seconds")
        return None
    except ConnectionError:
        logger.error("❌ Failed to connect to the API - check your internet connection")
        return None
    except RequestException as e:
        logger.error(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error occurred: {e}")
        return None

def get_player_info(player_tag):
    """
    Get player information by player tag
    Example player tag format: #2PP (without the # in the API call)
    """
    if not load_env_file():
        return None
    
    api_key = os.getenv('CLASH_ROYAL_API_KEY')
    if not api_key:
        logger.error("CLASH_ROYAL_API_KEY not found in environment variables")
        return None
    
    # Remove # from player tag if present
    clean_tag = player_tag.replace('#', '')
    
    url = f"https://api.clashroyale.com/v1/players/%23{clean_tag}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    
    try:
        logger.info(f"Getting player info for tag: #{clean_tag}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ Successfully retrieved player information!")
            return response.json()
        elif response.status_code == 404:
            logger.error(f"❌ Player with tag #{clean_tag} not found")
            return None
        else:
            logger.error(f"❌ HTTP Error: {response.status_code}")
            return None
    
    except Exception as e:
        logger.error(f"❌ Error getting player info: {e}")
        return None

def main():
    """Main function to test the Clash Royale API"""
    print("🏰 CLASH ROYALE API TEST 🏰\n")
    
    # Test 1: Get all cards (simple endpoint)
    print("=== TEST 1: Getting All Cards ===")
    cards_data = get_clash_royale_cards()
    
    if cards_data and 'items' in cards_data:
        cards = cards_data['items']
        print(f"✅ SUCCESS: Retrieved {len(cards)} cards from Clash Royale API")
        print("\n📋 Sample cards:")
        for i, card in enumerate(cards[:5]):  # Show first 5 cards
            print(f"  {i+1}. {card.get('name', 'Unknown')} - Elixir: {card.get('elixirCost', 'N/A')}")
        
        if len(cards) > 5:
            print(f"  ... and {len(cards) - 5} more cards")
            
        # Save to file
        try:
            with open('clash_royale_cards.json', 'w', encoding='utf-8') as f:
                json.dump(cards_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Saved all cards data to 'clash_royale_cards.json'")
        except Exception as e:
            logger.error(f"Failed to save cards data: {e}")
    else:
        print("❌ FAILED: Could not retrieve cards from API")
        return False
    
    print("\n" + "="*50)
    
    # Test 2: Try to get player info (optional)
    print("\n=== TEST 2: Getting Player Info (Optional) ===")
    default_player_tag = os.getenv('DEFAULT_PLAYER_TAG', 'LR09UCJJQ')
    print(f"Trying to get info for player: #{default_player_tag}")
    
    player_data = get_player_info(default_player_tag)
    if player_data:
        print(f"✅ SUCCESS: Retrieved player information!")
        print(f"  Player Name: {player_data.get('name', 'Unknown')}")
        print(f"  Level: {player_data.get('expLevel', 'Unknown')}")
        print(f"  Trophies: {player_data.get('trophies', 'Unknown')}")
        print(f"  Arena: {player_data.get('arena', {}).get('name', 'Unknown')}")
    else:
        print(f"⚠️  Could not retrieve player info for #{default_player_tag}")
        print("   This might be normal if the player tag doesn't exist")
    
    print("\n🎉 API TEST COMPLETED!")
    print("✅ Your Clash Royale API key is working correctly!")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All tests passed! Your API integration is working.")
    else:
        print("\n❌ Some tests failed. Check the logs above for details.")
