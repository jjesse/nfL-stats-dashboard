#!/usr/bin/env python3
"""
NFL Team Statistics Data Explorer
Test script to see what interesting data we can pull from Pro Football Reference
"""

import requests
import pandas as pd
from datetime import datetime
import time

def get_current_nfl_season():
    """Determine the current/most recent NFL season"""
    now = datetime.now()
    
    # NFL season typically runs September to February
    # If we're in January-July, use previous year
    # If we're in August-December, use current year
    if now.month <= 7:
        return now.year - 1
    else:
        return now.year

def explore_nfl_data():
    """Explore what data is available on Pro Football Reference"""
    
    base_url = "https://www.pro-football-reference.com"
    current_season = get_current_nfl_season()
    print(f"Initial season guess: {current_season}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("🏈 NFL DATA EXPLORATION")
    print("=" * 50)
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Season being analyzed: {current_season}")
    
    # 1. Test multiple seasons to find available data
    print(f"\n🔍 Testing Season Data Availability...")
    test_seasons = [current_season, current_season - 1, current_season - 2, 2023, 2022]
    
    working_season = None
    for season in test_seasons:
        try:
            print(f"\nTesting season {season}...")
            url = f"{base_url}/years/{season}/"
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if it's actually NFL data by looking for team tables
                content = response.text
                if 'AFC East' in content or 'Buffalo Bills' in content or 'standings' in content.lower():
                    tables = pd.read_html(response.content)
                    if tables and len(tables) > 0:
                        print(f"  ✓ Found {len(tables)} data tables")
                        working_season = season
                        break
                    else:
                        print(f"  ⚠️ No data tables found")
                else:
                    print(f"  ⚠️ Page exists but doesn't contain NFL data")
            else:
                print(f"  ✗ Page not accessible (Status: {response.status_code})")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        time.sleep(0.5)
    
    if not working_season:
        print("❌ Could not find any working season data!")
        print("This might be because:")
        print("  - Pro Football Reference website structure changed")
        print("  - Network connectivity issues") 
        print("  - The site is blocking automated requests")
        return
    
    print(f"\n✅ Using Season {working_season} for exploration")
    current_season = working_season
    
    # 1. Main season page - what's available?
    print(f"\n📊 Exploring {current_season} NFL Season Data...")
    try:
        url = f"{base_url}/years/{current_season}/"
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            tables = pd.read_html(response.content)
            print(f"✓ Found {len(tables)} data tables on main season page")
            
            for i, table in enumerate(tables[:5]):  # Show first 5 tables
                print(f"\nTable {i + 1}:")
                print(f"  Shape: {table.shape}")
                print(f"  Columns: {list(table.columns)[:10]}")  # First 10 columns
                
    except Exception as e:
        print(f"Error exploring main page: {e}")
    
    time.sleep(1)
    
    # 2. Team offense/defense stats
    print(f"\n🎯 Exploring Team Offense/Defense Stats...")
    try:
        url = f"{base_url}/years/{current_season}/opp.htm"
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            tables = pd.read_html(response.content)
            print(f"✓ Found {len(tables)} tables on team stats page")
            
            for i, table in enumerate(tables[:3]):
                print(f"\nTeam Stats Table {i + 1}:")
                print(f"  Shape: {table.shape}")
                print(f"  Columns: {list(table.columns)}")
                if not table.empty:
                    print(f"  Sample data:\n{table.head(3)}")
                
    except Exception as e:
        print(f"Error exploring team stats: {e}")
    
    time.sleep(1)
    
    # 3. Advanced stats - Red Zone (try different endpoints)
    print(f"\n🔴 Exploring Red Zone Stats...")
    red_zone_urls = [
        f"{base_url}/years/{current_season}/redzone.htm",
        f"{base_url}/teams/redzone/{current_season}.htm",
        f"{base_url}/years/{current_season}/opp.htm#team_stats"
    ]
    
    for url in red_zone_urls:
        try:
            print(f"Trying: {url}")
            response = requests.get(url, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                tables = pd.read_html(response.content)
                print(f"✓ Found {len(tables)} tables")
                
                if tables:
                    for i, table in enumerate(tables[:2]):
                        print(f"\nTable {i + 1}:")
                        print(f"  Shape: {table.shape}")
                        print(f"  Columns: {list(table.columns)[:5]}")
                    break
            else:
                print(f"  ✗ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
        
        time.sleep(0.5)
    
    time.sleep(1)
    
    # 4. What other interesting pages exist?
    interesting_pages = [
        ('third_down_conversions', f'/years/{current_season}/conv.htm'),
        ('kicking_stats', f'/years/{current_season}/kicking.htm'),
        ('punt_returns', f'/years/{current_season}/returns.htm'),
        ('team_drives', f'/years/{current_season}/drives.htm'),
        ('playoff_picture', f'/years/{current_season}/playoffs.htm')
    ]
    
    print(f"\n🔍 Exploring Other Interesting Stats...")
    for name, endpoint in interesting_pages:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, headers=headers)
            print(f"\n{name}: Status {response.status_code}")
            
            if response.status_code == 200:
                tables = pd.read_html(response.content)
                print(f"  ✓ Found {len(tables)} tables")
                
                if tables:
                    sample_table = tables[0]
                    print(f"  First table shape: {sample_table.shape}")
                    print(f"  Columns: {list(sample_table.columns)[:8]}")
            
            time.sleep(0.5)  # Be respectful
            
        except Exception as e:
            print(f"  Error with {name}: {e}")
    
    print("\n" + "=" * 50)
    print("🏆 DATA EXPLORATION COMPLETE!")
    print("=" * 50)

if __name__ == "__main__":
    explore_nfl_data()