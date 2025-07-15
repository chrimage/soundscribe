#!/usr/bin/env python3
"""
Test network connectivity to Discord voice endpoints.
"""

import socket
import asyncio
import aiohttp
import json

async def test_discord_connectivity():
    """Test basic Discord API connectivity."""
    print("🌐 Testing Discord API connectivity...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test basic API
            async with session.get("https://discord.com/api/v9/gateway") as resp:
                if resp.status == 200:
                    print("✅ Discord API reachable")
                    data = await resp.json()
                    print(f"   Gateway URL: {data.get('url')}")
                else:
                    print(f"❌ Discord API returned {resp.status}")
            
            # Test voice regions
            async with session.get("https://discord.com/api/v9/voice/regions") as resp:
                if resp.status == 200:
                    print("✅ Discord voice regions API reachable")
                    regions = await resp.json()
                    print(f"   Available regions: {len(regions)}")
                else:
                    print(f"❌ Voice regions API returned {resp.status}")
                    
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False
    
    return True

def test_udp_connectivity():
    """Test UDP socket creation (needed for voice)."""
    print("\n🔌 Testing UDP connectivity...")
    
    try:
        # Test UDP socket creation
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)
        
        # Try to connect to Discord's voice endpoint
        # This is just a connectivity test, not actual voice connection
        try:
            sock.connect(("discord.com", 53))  # DNS port for basic connectivity
            print("✅ UDP socket creation works")
            print(f"   Local address: {sock.getsockname()}")
        except Exception as e:
            print(f"⚠️  UDP connectivity test failed: {e}")
        finally:
            sock.close()
            
    except Exception as e:
        print(f"❌ UDP socket creation failed: {e}")
        return False
    
    return True

async def main():
    """Run all connectivity tests."""
    print("🔍 Discord Voice Connectivity Tests\n")
    
    api_ok = await test_discord_connectivity()
    udp_ok = test_udp_connectivity()
    
    print(f"\n📋 Results:")
    print(f"   API Connectivity: {'✅' if api_ok else '❌'}")
    print(f"   UDP Connectivity: {'✅' if udp_ok else '❌'}")
    
    if not api_ok or not udp_ok:
        print(f"\n🔧 Potential issues:")
        print("   - Server firewall blocking outbound connections")
        print("   - ISP/network blocking Discord endpoints")
        print("   - Server in restricted network environment")
        print("   - Try different Discord voice region in server settings")

if __name__ == "__main__":
    asyncio.run(main())