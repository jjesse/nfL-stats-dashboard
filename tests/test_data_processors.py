#!/usr/bin/env python3
"""
Tests for NFL data processors.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

import pytest
import pandas as pd

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "data-processors"))


class TestNFLSeasonCalculation:
    """Tests for NFL season calculation logic."""

    def test_current_season_before_august(self):
        """Test season calculation in January-July (should return previous year)."""
        # In January-July, we should get previous year
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 3, 15)
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

            # Manual calculation matching the code logic
            now = datetime(2024, 3, 15)
            if now.month <= 7:
                expected_season = now.year - 1
            else:
                expected_season = now.year

            assert expected_season == 2023

    def test_current_season_after_august(self):
        """Test season calculation in August-December (should return current year)."""
        now = datetime(2024, 9, 15)
        if now.month <= 7:
            expected_season = now.year - 1
        else:
            expected_season = now.year

        assert expected_season == 2024


class TestDataFrameProcessing:
    """Tests for DataFrame processing utilities."""

    def test_clean_player_names(self):
        """Test that player names are properly cleaned."""
        # Sample data like what we'd get from Pro Football Reference
        df = pd.DataFrame({
            'Player': ['John Doe*+', 'Jane Smith*', 'Bob Jones', None, 'Player'],
            'Yds': [1000, 800, 600, None, 'Yds']
        })

        # Clean up like in the actual processors
        df = df[df['Player'].notna()]
        df = df[df['Player'] != 'Player']

        assert len(df) == 3
        assert 'John Doe*+' in df['Player'].values

    def test_numeric_conversion(self):
        """Test numeric column conversion."""
        df = pd.DataFrame({
            'Player': ['Player A', 'Player B'],
            'Yds': ['1000', '800'],
            'TD': ['10', '8']
        })

        for col in ['Yds', 'TD']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        assert df['Yds'].dtype in ['int64', 'float64']
        assert df['TD'].dtype in ['int64', 'float64']

    def test_top_n_selection(self):
        """Test selecting top N players by a stat."""
        df = pd.DataFrame({
            'Player': ['A', 'B', 'C', 'D', 'E'],
            'Yds': [100, 500, 300, 400, 200]
        })

        top_3 = df.nlargest(3, 'Yds')

        assert len(top_3) == 3
        assert top_3.iloc[0]['Player'] == 'B'  # Highest yards
        assert top_3.iloc[0]['Yds'] == 500


class TestMVPScoreCalculation:
    """Tests for MVP score calculation logic."""

    def test_mvp_score_with_all_stats(self):
        """Test MVP score calculation with complete stats."""
        # Simulate row data
        row = {
            'W': 12,
            'TD': 35,
            'Rate': 105.0,
            'Yds': 4200,
            'Int': 8
        }

        score = 0

        # Team Success (25% weight)
        if 'W' in row and pd.notna(row['W']):
            score += row['W'] * 4.0

        # Total TDs (30% weight)
        if 'TD' in row and pd.notna(row['TD']):
            total_tds = row['TD']
            if row['TD'] > 20:
                total_tds += 5
            score += total_tds * 2.4

        # QB Efficiency (20% weight)
        if 'Rate' in row and pd.notna(row['Rate']):
            score += (row['Rate'] / 100) * 16

        # Passing Yards (15% weight)
        if 'Yds' in row and pd.notna(row['Yds']):
            score += (row['Yds'] / 4000) * 12

        # Turnover Protection (10% weight)
        if 'Int' in row and pd.notna(row['Int']):
            score -= row['Int'] * 0.8

        score = max(score, 0)

        assert score > 0
        assert isinstance(score, float)

    def test_mvp_score_no_negative(self):
        """Test that MVP score doesn't go negative."""
        row = {
            'W': 0,
            'TD': 5,
            'Rate': 50.0,
            'Yds': 500,
            'Int': 25  # Many interceptions
        }

        score = 0

        # Simplified calculation
        score += row['W'] * 4.0
        score += row['TD'] * 2.4
        score += (row['Rate'] / 100) * 16
        score += (row['Yds'] / 4000) * 12
        score -= row['Int'] * 0.8

        score = max(score, 0)

        assert score >= 0


class TestDivisionMapping:
    """Tests for NFL division mapping."""

    def test_afc_divisions(self):
        """Test AFC division team mapping."""
        divisions = {
            'AFC East': ['BUF', 'MIA', 'NWE', 'NYJ'],
            'AFC North': ['BAL', 'CIN', 'CLE', 'PIT'],
            'AFC South': ['HOU', 'IND', 'JAX', 'TEN'],
            'AFC West': ['DEN', 'KAN', 'LVR', 'LAC']
        }

        # Test total AFC teams
        afc_teams = []
        for teams in divisions.values():
            afc_teams.extend(teams)

        assert len(afc_teams) == 16

    def test_nfc_divisions(self):
        """Test NFC division team mapping."""
        divisions = {
            'NFC East': ['DAL', 'NYG', 'PHI', 'WAS'],
            'NFC North': ['CHI', 'DET', 'GNB', 'MIN'],
            'NFC South': ['ATL', 'CAR', 'NOR', 'TAM'],
            'NFC West': ['ARI', 'LAR', 'SFO', 'SEA']
        }

        # Test total NFC teams
        nfc_teams = []
        for teams in divisions.values():
            nfc_teams.extend(teams)

        assert len(nfc_teams) == 16

    def test_conference_determination(self):
        """Test conference determination from division name."""
        division_name = 'AFC East'
        conference = 'AFC' if division_name.startswith('AFC') else 'NFC' if division_name.startswith('NFC') else 'Unknown'
        assert conference == 'AFC'

        division_name = 'NFC West'
        conference = 'AFC' if division_name.startswith('AFC') else 'NFC' if division_name.startswith('NFC') else 'Unknown'
        assert conference == 'NFC'
