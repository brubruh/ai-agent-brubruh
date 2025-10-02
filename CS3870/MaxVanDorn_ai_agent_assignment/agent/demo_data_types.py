#!/usr/bin/env python3
"""
Demonstration of Raw vs Processed Data
Shows the clear differences between the two data types
"""

import json
from datetime import datetime

def create_sample_raw_data():
    """Example of raw data as received from an API"""
    raw_data = {
        "items": [
            {
                "name": "Knight",
                "id": 26000000,
                "maxLevel": 13,
                "maxEvolutionLevel": 1,
                "elixirCost": 3,
                "type": "Troop",
                "rarity": "Common",
                "arena": 0,
                "description": "A tough melee fighter. The Barbarian's handsome, cultured cousin. Rumor has it that he was knighted based on the sheer awesomeness of his mustache alone.",
                "sc_key": "knight",
                "iconUrls": {
                    "medium": "https://api-assets.clashroyale.com/cards/300/STTQ8322DD2Z8QJ2VL3S7R4LKC1XN2QV.png",
                    "evolutionMedium": "https://api-assets.clashroyale.com/cards/300/STTQ8322DD2Z8QJ2VL3S7R4LKC1XN2QV_EVO.png"
                }
            },
            {
                "name": "Archers",
                "id": 26000001,
                "maxLevel": 13,
                "maxEvolutionLevel": 1,
                "elixirCost": 3,
                "type": "Troop",
                "rarity": "Common",
                "arena": 0,
                "description": "A pair of lightly armored ranged attackers. They'll help you take down ground and air units, but you're on your own with hair coloring advice.",
                "sc_key": "archers",
                "iconUrls": {
                    "medium": "https://api-assets.clashroyale.com/cards/300/1ArIcOUX_VDYVLRjZ5Q3qUOH7a5xPYK6.png",
                    "evolutionMedium": "https://api-assets.clashroyale.com/cards/300/1ArIcOUX_VDYVLRjZ5Q3qUOH7a5xPYK6_EVO.png"
                }
            }
        ],
        "supportItems": []
    }
    return raw_data

def create_sample_processed_data():
    """Example of processed data - cleaned and transformed"""
    processed_data = [
        {
            "name": "Knight",
            "elixir_cost": 3,
            "type": "Troop",
            "rarity": "Common",
            "is_evolution_available": True,
            "collected_at": "2025-10-01T20:37:20.123456",
            "data_quality_score": 1.0
        },
        {
            "name": "Archers",
            "elixir_cost": 3,
            "type": "Troop", 
            "rarity": "Common",
            "is_evolution_available": True,
            "collected_at": "2025-10-01T20:37:20.123456",
            "data_quality_score": 1.0
        }
    ]
    return processed_data

def demonstrate_data_differences():
    """Show the key differences between raw and processed data"""
    
    print("🔍 RAW vs PROCESSED DATA DEMONSTRATION")
    print("=" * 60)
    
    # Create sample data
    raw_data = create_sample_raw_data()
    processed_data = create_sample_processed_data()
    
    print("\n📥 RAW DATA (As received from API):")
    print("-" * 40)
    print("✅ Contains ALL original fields")
    print("✅ Preserves exact API structure")
    print("✅ Includes metadata, URLs, IDs")
    print("✅ Used for backup and debugging")
    print(f"✅ Size: {len(json.dumps(raw_data))} characters")
    
    print("\nSample raw data structure:")
    print(json.dumps(raw_data['items'][0], indent=2)[:500] + "...")
    
    print("\n\n🎯 PROCESSED DATA (Cleaned and transformed):")
    print("-" * 45)
    print("✅ Only relevant fields extracted")
    print("✅ Standardized field names (snake_case)")
    print("✅ Added calculated fields")
    print("✅ Ready for analysis/application use")
    print(f"✅ Size: {len(json.dumps(processed_data))} characters")
    
    print("\nSample processed data structure:")
    print(json.dumps(processed_data[0], indent=2))
    
    print("\n\n💡 KEY DIFFERENCES:")
    print("-" * 20)
    
    # Compare specific aspects
    raw_item = raw_data['items'][0]
    processed_item = processed_data[0]
    
    print(f"🔸 Field Count:")
    print(f"   Raw: {len(raw_item)} fields")
    print(f"   Processed: {len(processed_item)} fields")
    
    print(f"\n🔸 Field Names:")
    print(f"   Raw: {list(raw_item.keys())[:5]}...")
    print(f"   Processed: {list(processed_item.keys())}")
    
    print(f"\n🔸 Data Size Reduction:")
    raw_size = len(json.dumps(raw_item))
    processed_size = len(json.dumps(processed_item))
    reduction = ((raw_size - processed_size) / raw_size) * 100
    print(f"   Raw item size: {raw_size} chars")
    print(f"   Processed item size: {processed_size} chars") 
    print(f"   Size reduction: {reduction:.1f}%")
    
    print(f"\n🔸 Added Value in Processed Data:")
    print("   ✅ Timestamp when collected")
    print("   ✅ Data quality scoring")
    print("   ✅ Boolean flags (is_evolution_available)")
    print("   ✅ Consistent field naming")
    
    # Save examples to files
    import os
    os.makedirs('../data/examples', exist_ok=True)
    
    with open('../data/examples/raw_data_sample.json', 'w') as f:
        json.dump({
            'metadata': {
                'description': 'Example of raw data as received from API',
                'created_at': datetime.now().isoformat(),
                'type': 'raw_example'
            },
            'data': raw_data
        }, f, indent=2)
    
    with open('../data/examples/processed_data_sample.json', 'w') as f:
        json.dump({
            'metadata': {
                'description': 'Example of processed, cleaned data',
                'created_at': datetime.now().isoformat(),
                'type': 'processed_example',
                'transformations': [
                    'field_extraction',
                    'field_renaming',
                    'boolean_conversion',
                    'timestamp_addition'
                ]
            },
            'data': processed_data
        }, f, indent=2)
    
    print(f"\n💾 Sample files saved to ../data/examples/")
    print("   - raw_data_sample.json")
    print("   - processed_data_sample.json")
    
    print(f"\n🎉 This demonstrates why we separate raw and processed data!")

if __name__ == "__main__":
    demonstrate_data_differences()