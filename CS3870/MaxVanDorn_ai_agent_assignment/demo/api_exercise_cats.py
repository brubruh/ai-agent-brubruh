import requests
import json
import logging
from requests.exceptions import RequestException, Timeout, ConnectionError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_exercises.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Make your first API call to get a random cat fact
def get_cat_fact():
    url = "https://catfact.ninja/fact"
    
    try:
        logger.info(f"Requesting cat fact from {url}")
        
        # Send GET request to the API with timeout
        response = requests.get(url, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            logger.info("Successfully retrieved cat fact")
            # Parse JSON response
            data = response.json()
            
            # Validate that the expected field exists
            if 'fact' not in data:
                logger.error("Response missing 'fact' field")
                return None
                
            fact = data['fact']
            if not fact or not fact.strip():
                logger.warning("Retrieved empty or whitespace-only fact")
                return None
                
            return fact
        else:
            logger.error(f"HTTP Error: {response.status_code} - {response.reason}")
            return None
    
    except Timeout:
        logger.error("Request timed out after 10 seconds")
        return None
    except ConnectionError:
        logger.error("Failed to connect to the API - check your internet connection")
        return None
    except requests.exceptions.JSONDecodeError:
        logger.error("Failed to parse JSON response")
        return None
    except RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return None

# Test your function
cat_facts = []
logger.info("Starting to collect 5 cat facts")

for i in range(5):
    logger.info(f"Attempting to get cat fact {i+1}/5")
    cat_fact = get_cat_fact()
    if cat_fact:
        cat_facts.append({"fact": cat_fact})
        logger.info(f"Successfully collected cat fact {i+1}/5")
    else:
        logger.warning(f"Failed to get cat fact {i+1}/5")

logger.info(f"Collection complete. Got {len(cat_facts)} out of 5 cat facts")

# Write all facts to a json file
try:
    with open('cat_facts.json', 'w', encoding='utf-8') as f:
        json.dump(cat_facts, f, indent=2, ensure_ascii=False)
    logger.info(f"Successfully wrote {len(cat_facts)} cat facts to cat_facts.json")
except IOError as e:
    logger.error(f"Failed to write to file: {e}")
except Exception as e:
    logger.error(f"Unexpected error while writing file: {e}")


