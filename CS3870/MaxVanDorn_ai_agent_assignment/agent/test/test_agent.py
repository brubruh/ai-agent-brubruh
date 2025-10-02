#!/usr/bin/env python3
"""
Test script for DataCollectionAgent
Demonstrates how to use the agent with configuration
"""

import sys
import os
# Add parent directory to path to import data_collection_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection_agent import DataCollectionAgent
import json

def main():
    """Test the DataCollectionAgent"""
    print("🤖 TESTING DATA COLLECTION AGENT")
    print("=" * 50)
    
    try:
        # Initialize agent with configuration
        config_file = 'config.json'
        agent = DataCollectionAgent(config_file)
        
        print(f"✅ Agent initialized successfully!")
        print(f"📋 Configuration loaded: {agent.config['agent_settings']['name']}")
        print(f"🎯 Max requests: {agent.config['agent_settings']['max_requests']}")
        print(f"⏱️  Base delay: {agent.config['agent_settings']['base_delay']}s")
        
        # Test a few collection cycles
        print("\n🔄 Starting data collection (limited test)...")
        
        # Override max_requests for testing
        original_max = agent.config['agent_settings']['max_requests']
        agent.config['agent_settings']['max_requests'] = 3  # Just collect 3 for testing
        
        # Run collection
        agent.collect_data()
        
        # Generate and display report
        print("\n📊 COLLECTION REPORT")
        print("-" * 30)
        report = agent.generate_report()
        
        for key, value in report.items():
            if key != 'configuration_used':
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        print(f"\n💾 Sample collected data:")
        if agent.data_store:
            for i, item in enumerate(agent.data_store[:3]):  # Show first 3 items
                print(f"  {i+1}. {item.get('name', 'Unknown')} - {item.get('elixir_cost', 'N/A')} elixir")
        else:
            print("  No data collected (possibly API key issues)")
        
        # Report is automatically saved by the agent
        print(f"\n💾 Full report saved to reports folder")
        
        # Restore original max_requests
        agent.config['agent_settings']['max_requests'] = original_max
        
        print("\n✅ Test completed successfully!")
        
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        print("Make sure the configuration file exists in the same directory.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()