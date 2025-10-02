#!/usr/bin/env python3
"""
Test the enhanced metadata generation in the actual agent
"""

import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection_agent import DataCollectionAgent

def test_metadata_generation():
    """Test the comprehensive metadata generation"""
    print("🧪 TESTING COMPREHENSIVE METADATA GENERATION")
    print("=" * 50)
    
    try:
        # Initialize agent
        agent = DataCollectionAgent('config.json')
        
        # Test sample data
        test_data = {
            "items": [
                {
                    "name": "Test Card",
                    "id": 99999999,
                    "elixirCost": 5,
                    "rarity": "legendary",
                    "maxLevel": 16
                }
            ]
        }
        
        print("📊 Testing comprehensive metadata generation...")
        
        # Generate comprehensive metadata using the new method
        metadata = agent.generate_comprehensive_metadata(
            test_data, 'raw', 'test_metadata_demo'
        )
        
        print("✅ Metadata generated successfully!")
        print(f"📋 Metadata categories: {len(metadata)}")
        
        # Count total fields
        total_fields = 0
        for category, data in metadata.items():
            if isinstance(data, dict):
                total_fields += len(data)
            else:
                total_fields += 1
            print(f"   {category}: {len(data) if isinstance(data, dict) else 1} fields")
        
        print(f"📊 Total metadata fields: {total_fields}")
        
        # Save test metadata for inspection
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata_file = f"../data/examples/comprehensive_metadata_test_{timestamp}.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        print(f"💾 Test metadata saved to: {metadata_file}")
        
        # Show a sample of the schema info
        if 'schema_info' in metadata:
            schema = metadata['schema_info']
            print(f"\n📋 Schema Analysis Sample:")
            print(f"   Field count: {schema.get('field_count', 'N/A')}")
            if 'fields' in schema:
                print(f"   Fields analyzed: {list(schema['fields'].keys())}")
        
        # Show data characteristics
        if 'data_characteristics' in metadata:
            chars = metadata['data_characteristics']
            print(f"\n📊 Data Characteristics:")
            print(f"   Total items: {chars.get('total_items', 'N/A')}")
            print(f"   Data size: {chars.get('data_size_bytes', 'N/A')} bytes")
            print(f"   Fingerprint: {chars.get('data_fingerprint', 'N/A')[:16]}...")
        
        print(f"\n🎉 Your agent generates {total_fields} metadata fields automatically!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_metadata_generation()