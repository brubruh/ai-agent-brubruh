#!/usr/bin/env python3
"""
API Connectivity Test Script
Quick diagnostic tool to check if the agent can reach the API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection_agent import DataCollectionAgent

def main():
    """Test API connectivity without full data collection"""
    print("🔧 API CONNECTIVITY DIAGNOSTIC")
    print("=" * 50)
    
    try:
        # Initialize agent
        config_file = 'config.json'
        agent = DataCollectionAgent(config_file)
        
        print(f"✅ Agent initialized successfully")
        print(f"🎯 Target API: Clash Royale Cards API")
        
        # Run connectivity test
        print("\n🧪 Running connectivity tests...")
        is_connected = agent.test_api_connectivity()
        
        print("\n" + "=" * 50)
        if is_connected:
            print("🎉 RESULT: API is reachable and working!")
            print("✅ Your agent should be able to collect data")
        else:
            print("❌ RESULT: API connectivity issues detected")
            print("🔧 Check the diagnostic messages above for solutions")
            
            # Provide troubleshooting tips
            print("\n💡 TROUBLESHOOTING TIPS:")
            print("1. Verify your API key in config.json")
            print("2. Check your internet connection")
            print("3. Ensure no firewall is blocking the requests")
            print("4. Try visiting https://api.clashroyale.com in your browser")
        
        print(f"\n📊 Agent Statistics:")
        print(f"   Total requests: {agent.collection_stats['total_requests']}")
        print(f"   Successful: {agent.collection_stats['successful_requests']}")
        print(f"   Failed: {agent.collection_stats['failed_requests']}")
        
    except Exception as e:
        print(f"❌ Error during connectivity test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()