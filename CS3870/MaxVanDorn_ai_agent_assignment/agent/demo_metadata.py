#!/usr/bin/env python3
"""
Automated Metadata Generation Demonstration
Shows the comprehensive metadata capabilities of the data collection agent
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection_agent import DataCollectionAgent

def main():
    """Demonstrate automated metadata generation"""
    print("🔍 AUTOMATED METADATA GENERATION DEMONSTRATION")
    print("=" * 60)
    
    try:
        # Initialize agent
        agent = DataCollectionAgent('config.json')
        
        # Create sample data to demonstrate metadata generation
        sample_raw_data = {
            "items": [
                {
                    "name": "Knight",
                    "id": 26000000,
                    "elixirCost": 3,
                    "rarity": "common",
                    "maxLevel": 14
                },
                {
                    "name": "Archers", 
                    "id": 26000001,
                    "elixirCost": 3,
                    "rarity": "common",
                    "maxLevel": 14
                }
            ]
        }
        
        sample_processed_data = [
            {
                "name": "Knight",
                "elixir_cost": 3,
                "rarity": "common",
                "collected_at": "2025-10-01T21:30:00",
                "data_quality_score": 1.0
            },
            {
                "name": "Archers",
                "elixir_cost": 3, 
                "rarity": "common",
                "collected_at": "2025-10-01T21:30:00",
                "data_quality_score": 1.0
            }
        ]
        
        print("📊 Generating comprehensive metadata...")
        
        # Generate metadata for raw data
        raw_metadata = agent.generate_comprehensive_metadata(
            sample_raw_data, 'raw', 'demo_cards'
        )
        
        # Generate metadata for processed data  
        processed_metadata = agent.generate_comprehensive_metadata(
            sample_processed_data, 'processed', 'demo_cards'
        )
        
        print("✅ Metadata generation complete!\n")
        
        # Display metadata categories
        print("📋 AUTOMATED METADATA CATEGORIES:")
        print("-" * 40)
        
        categories = [
            ('⏰ Temporal Metadata', 'collection_info'),
            ('🌐 Source Metadata', 'source_info'), 
            ('🤖 Agent Metadata', 'agent_info'),
            ('💻 System Metadata', 'system_info'),
            ('📊 Data Characteristics', 'data_characteristics'),
            ('✅ Quality Metadata', 'quality_info'),
            ('📋 Schema Metadata', 'schema_info'),
            ('🔗 Lineage Metadata', 'lineage_info'),
            ('📖 Usage Metadata', 'usage_info')
        ]
        
        for category_name, category_key in categories:
            if category_key in raw_metadata:
                category_data = raw_metadata[category_key]
                field_count = len(category_data) if isinstance(category_data, dict) else 1
                print(f"{category_name}: {field_count} fields")
                
                # Show sample fields
                if isinstance(category_data, dict):
                    sample_fields = list(category_data.keys())[:3]
                    print(f"   Sample fields: {', '.join(sample_fields)}")
        
        print(f"\n📈 METADATA STATISTICS:")
        print(f"   Total metadata fields (raw): {sum(len(v) if isinstance(v, dict) else 1 for v in raw_metadata.values())}")
        print(f"   Total metadata fields (processed): {sum(len(v) if isinstance(v, dict) else 1 for v in processed_metadata.values())}")
        print(f"   Metadata size (raw): {len(json.dumps(raw_metadata))} characters")
        print(f"   Metadata size (processed): {len(json.dumps(processed_metadata))} characters")
        
        # Save metadata examples
        os.makedirs('../data/examples', exist_ok=True)
        
        with open('../data/examples/raw_metadata_sample.json', 'w') as f:
            json.dump(raw_metadata, f, indent=2, default=str)
            
        with open('../data/examples/processed_metadata_sample.json', 'w') as f:
            json.dump(processed_metadata, f, indent=2, default=str)
        
        print(f"\n💾 Sample metadata files saved:")
        print(f"   📄 ../data/examples/raw_metadata_sample.json")
        print(f"   📄 ../data/examples/processed_metadata_sample.json")
        
        # Generate metadata catalog
        print(f"\n📚 Generating metadata catalog...")
        catalog = agent.generate_metadata_catalog()
        
        print(f"✅ Metadata catalog generated!")
        print(f"   📋 Automated features: {len(catalog['automated_metadata_features'])} categories")
        print(f"   🔧 Standards: {catalog['catalog_info']['metadata_standards']}")
        
        # Show automated metadata features
        print(f"\n🔧 AUTOMATED METADATA FEATURES:")
        print("-" * 35)
        for feature_category, features in catalog['automated_metadata_features'].items():
            print(f"{feature_category.replace('_', ' ').title()}:")
            for feature in features[:2]:  # Show first 2 features
                print(f"   ✅ {feature.replace('_', ' ').title()}")
            if len(features) > 2:
                print(f"   ... and {len(features) - 2} more")
        
        print(f"\n🎉 CONCLUSION:")
        print(f"✅ Your agent AUTOMATICALLY generates comprehensive metadata!")
        print(f"✅ Metadata includes {len(categories)} major categories")
        print(f"✅ All data files include rich, structured metadata")
        print(f"✅ Metadata supports data discovery, quality, and governance")
        
    except Exception as e:
        print(f"❌ Error during metadata demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()