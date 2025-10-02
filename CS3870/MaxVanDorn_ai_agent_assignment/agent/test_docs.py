#!/usr/bin/env python3
"""
Test comprehensive documentation generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection_agent import DataCollectionAgent

def main():
    """Test comprehensive documentation generation"""
    print("📚 TESTING COMPREHENSIVE DOCUMENTATION")
    print("=" * 50)
    
    try:
        # Initialize agent
        agent = DataCollectionAgent('config.json')
        
        # Add some sample data to demonstrate documentation
        agent.data_store = [
            {
                'name': 'Knight',
                'elixir_cost': 3,
                'rarity': 'common',
                'collected_at': '2025-10-01T20:00:00',
                'data_quality_score': 1.0
            }
        ]
        
        # Update stats to show some activity
        agent.collection_stats['total_requests'] = 5
        agent.collection_stats['successful_requests'] = 5
        agent.collection_stats['failed_requests'] = 0
        
        print("🔄 Generating comprehensive documentation...")
        docs = agent.generate_comprehensive_documentation()
        
        print("✅ Documentation generated successfully!")
        print(f"📊 Documentation sections: {len(docs)} sections")
        
        for section in docs.keys():
            if section != 'metadata':
                print(f"   📋 {section}")
        
        print(f"\n💾 Documentation saved to reports/documentation/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()