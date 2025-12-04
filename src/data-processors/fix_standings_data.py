#!/usr/bin/env python3
"""
Fix Standings Data
Cleans up the team_standings.csv file by:
1. Removing division header rows
2. Adding proper Division and Conference columns
3. Ensuring all teams have proper mappings
"""

import pandas as pd
from pathlib import Path

# Team to division mapping
TEAM_DIVISIONS = {
    # AFC East
    'Buffalo Bills': 'AFC East',
    'Miami Dolphins': 'AFC East',
    'New England Patriots': 'AFC East',
    'New York Jets': 'AFC East',
    # AFC North
    'Baltimore Ravens': 'AFC North',
    'Cincinnati Bengals': 'AFC North',
    'Cleveland Browns': 'AFC North',
    'Pittsburgh Steelers': 'AFC North',
    # AFC South
    'Houston Texans': 'AFC South',
    'Indianapolis Colts': 'AFC South',
    'Jacksonville Jaguars': 'AFC South',
    'Tennessee Titans': 'AFC South',
    # AFC West
    'Denver Broncos': 'AFC West',
    'Kansas City Chiefs': 'AFC West',
    'Las Vegas Raiders': 'AFC West',
    'Los Angeles Chargers': 'AFC West',
    # NFC East
    'Dallas Cowboys': 'NFC East',
    'New York Giants': 'NFC East',
    'Philadelphia Eagles': 'NFC East',
    'Washington Commanders': 'NFC East',
    'Washington Football Team': 'NFC East',  # Old name
    # NFC North
    'Chicago Bears': 'NFC North',
    'Detroit Lions': 'NFC North',
    'Green Bay Packers': 'NFC North',
    'Minnesota Vikings': 'NFC North',
    # NFC South
    'Atlanta Falcons': 'NFC South',
    'Carolina Panthers': 'NFC South',
    'New Orleans Saints': 'NFC South',
    'Tampa Bay Buccaneers': 'NFC South',
    # NFC West
    'Arizona Cardinals': 'NFC West',
    'Los Angeles Rams': 'NFC West',
    'San Francisco 49ers': 'NFC West',
    'Seattle Seahawks': 'NFC West',
}


def clean_team_name(name):
    """Remove playoff indicators and clean team name"""
    if pd.isna(name):
        return name
    return str(name).replace('*', '').replace('+', '').strip()


def is_division_header_row(row):
    """Check if a row is a division header (division name appears in all columns)"""
    if pd.isna(row['Tm']):
        return False

    # Check if Tm column contains a division name
    divisions = ['AFC East', 'AFC North', 'AFC South', 'AFC West',
                 'NFC East', 'NFC North', 'NFC South', 'NFC West']

    return row['Tm'] in divisions


def fix_standings_data():
    """Clean and fix the standings data"""
    docs_dir = Path(__file__).parent.parent.parent / "docs"
    standings_file = docs_dir / "team_standings.csv"

    print("🔧 Fixing standings data...")
    print(f"📂 Reading from: {standings_file}")

    # Read the CSV
    df = pd.read_csv(standings_file)

    print(f"📊 Original data: {len(df)} rows")

    # Remove division header rows
    # These rows have the division name in the 'W' column
    divisions_list = ['AFC East', 'AFC North', 'AFC South', 'AFC West',
                      'NFC East', 'NFC North', 'NFC South', 'NFC West']

    df_clean = df[~df['W'].isin(divisions_list)].copy()

    print(f"✅ Removed {len(df) - len(df_clean)} division header rows")
    print(f"📊 Clean data: {len(df_clean)} rows (teams)")

    # Clean team names
    df_clean['Team'] = df_clean['Tm'].apply(clean_team_name)

    # Add division and conference
    df_clean['Division'] = df_clean['Team'].map(TEAM_DIVISIONS)
    df_clean['Conference'] = df_clean['Division'].apply(
        lambda x: 'AFC' if pd.notna(x) and x.startswith('AFC')
        else 'NFC' if pd.notna(x) and x.startswith('NFC')
        else 'Unknown'
    )

    # Add T (Ties) column if not present
    if 'T' not in df_clean.columns:
        df_clean['T'] = 0

    # Reorder columns to put Team, Division, Conference first
    cols = ['Team', 'Division', 'Conference', 'Tm', 'W', 'L', 'T']
    other_cols = [c for c in df_clean.columns if c not in cols]
    df_clean = df_clean[cols + other_cols]

    # Sort by conference, division, and wins
    df_clean['W_num'] = pd.to_numeric(df_clean['W'], errors='coerce')
    df_clean = df_clean.sort_values(['Conference', 'Division', 'W_num'],
                                    ascending=[True, True, False])
    df_clean = df_clean.drop('W_num', axis=1)

    # Save the cleaned data
    df_clean.to_csv(standings_file, index=False)
    print(f"✅ Saved cleaned data to: {standings_file}")

    # Print summary
    print("\n📋 Summary:")
    print(f"   Total teams: {len(df_clean)}")

    if 'Division' in df_clean.columns:
        print("   Divisions:")
        for div in sorted(df_clean['Division'].unique()):
            if pd.notna(div) and div != 'Unknown':
                count = len(df_clean[df_clean['Division'] == div])
                print(f"      {div}: {count} teams")

    if 'Conference' in df_clean.columns:
        print("   Conferences:")
        for conf in ['AFC', 'NFC']:
            count = len(df_clean[df_clean['Conference'] == conf])
            print(f"      {conf}: {count} teams")

    # Check for teams without division assignment
    unknown_teams = df_clean[df_clean['Division'].isna() | (df_clean['Division'] == 'Unknown')]
    if len(unknown_teams) > 0:
        print(f"\n⚠️  Warning: {len(unknown_teams)} teams without division assignment:")
        for team in unknown_teams['Team']:
            print(f"      - {team}")

    print("\n✅ Standings data fixed!")
    return df_clean


if __name__ == "__main__":
    fix_standings_data()
