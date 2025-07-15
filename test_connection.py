#!/usr/bin/env python3
"""
Pro Football Reference Connection Test
Quick test to see what's accessible and troubleshoot 404 errors
"""

import requests
import pandas as pd
from datetime import datetime

def test_pfr_connection():
    """Test basic connectivity to Pro Football Reference"""
    
    base_url = "https://www.pro-football-reference.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("🏈 PRO FOOTBALL REFERENCE CONNECTION TEST")
    print("=" * 50)
    
    # Test 1: Basic site connectivity
    print("\n1. Testing basic site connectivity...")
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        print(f"Main site status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Site is accessible")
        else:
            print(f"❌ Site returned status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Test 2: Check what seasons are available
    print("\n2. Testing season availability...")
    current_year = datetime.now().year
    seasons_to_test = [2024, 2023, 2022, 2021, current_year, current_year - 1]
    
    working_seasons = []
    for season in seasons_to_test:
        try:
            url = f"{base_url}/years/{season}/"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                # Check if it actually contains NFL data
                content = response.text
                if any(team in content for team in ['Buffalo Bills', 'AFC East', 'NFC West']):
                    working_seasons.append(season)
                    print(f"✅ Season {season}: Available")
                else:
                    print(f"⚠️ Season {season}: Page exists but no NFL data")
            else:
                print(f"❌ Season {season}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Season {season}: Error - {e}")
    
    if not working_seasons:
        print("\n❌ No working seasons found!")
        return
    
    # Test 3: Try to get actual data from a working season
    print(f"\n3. Testing data extraction from season {working_seasons[0]}...")
    try:
        url = f"{base_url}/years/{working_seasons[0]}/"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            tables = pd.read_html(response.content)
            print(f"✅ Found {len(tables)} data tables")
            
            # Show info about first few tables
            for i, table in enumerate(tables[:3]):
                print(f"  Table {i+1}: {table.shape} - Columns: {list(table.columns)[:5]}")
                
        else:
            print(f"❌ Failed to get data: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Data extraction failed: {e}")
    
    # Test 4: Test specific URLs that were failing
    print(f"\n4. Testing specific URLs that were giving 404s...")
    test_urls = [
        f"/years/{working_seasons[0]}/opp.htm",
        f"/years/{working_seasons[0]}/passing.htm", 
        f"/years/{working_seasons[0]}/rushing.htm",
        f"/years/{working_seasons[0]}/defense.htm"
    ]
    
    for endpoint in test_urls:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: Available")
            else:
                print(f"❌ {endpoint}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print(f"\n🎯 SUMMARY:")
    print(f"Working seasons: {working_seasons}")
    print(f"Recommended season to use: {working_seasons[0] if working_seasons else 'None'}")

if __name__ == "__main__":
    test_pfr_connection()