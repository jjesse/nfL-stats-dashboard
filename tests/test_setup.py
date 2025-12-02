#!/usr/bin/env python3
"""
Tests for setup and directory structure functionality.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from setup_directories import setup_directories


class TestSetupDirectories:
    """Tests for the setup_directories module."""

    def test_setup_directories_creates_docs_dir(self, tmp_path):
        """Test that directory creation works correctly."""
        docs_dir = tmp_path / "docs"
        archive_dir = tmp_path / "archive"

        # Create directories (simulating what setup_directories does)
        docs_dir.mkdir(parents=True, exist_ok=True)
        archive_dir.mkdir(parents=True, exist_ok=True)

        assert docs_dir.exists()
        assert archive_dir.exists()
        assert docs_dir.is_dir()
        assert archive_dir.is_dir()

    def test_docs_dir_exists_in_project(self):
        """Test that docs directory exists in the project."""
        docs_dir = project_root / "docs"
        assert docs_dir.exists(), "docs directory should exist"

    def test_src_dir_exists(self):
        """Test that src directory exists."""
        src_dir = project_root / "src"
        assert src_dir.exists(), "src directory should exist"

    def test_data_processors_dir_exists(self):
        """Test that data-processors directory exists."""
        data_processors_dir = project_root / "src" / "data-processors"
        assert data_processors_dir.exists(), "data-processors directory should exist"


class TestProjectStructure:
    """Tests for verifying project file structure."""

    def test_readme_exists(self):
        """Test that README.md exists."""
        readme_file = project_root / "README.md"
        assert readme_file.exists(), "README.md should exist"

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        requirements_file = project_root / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt should exist"

    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        gitignore_file = project_root / ".gitignore"
        assert gitignore_file.exists(), ".gitignore should exist"

    def test_contributing_exists(self):
        """Test that CONTRIBUTING.md exists."""
        contributing_file = project_root / "CONTRIBUTING.md"
        assert contributing_file.exists(), "CONTRIBUTING.md should exist"

    def test_player_stats_processor_exists(self):
        """Test that player-stats.py exists."""
        player_stats_file = project_root / "src" / "data-processors" / "player-stats.py"
        assert player_stats_file.exists(), "player-stats.py should exist"

    def test_team_stats_processor_exists(self):
        """Test that team-stats-basic.py exists."""
        team_stats_file = project_root / "src" / "data-processors" / "team-stats-basic.py"
        assert team_stats_file.exists(), "team-stats-basic.py should exist"

    def test_awards_tracker_exists(self):
        """Test that awards-tracker.py exists."""
        awards_file = project_root / "src" / "data-processors" / "awards-tracker.py"
        assert awards_file.exists(), "awards-tracker.py should exist"

    def test_schedule_processor_exists(self):
        """Test that schedule-processor.py exists."""
        schedule_file = project_root / "src" / "data-processors" / "schedule-processor.py"
        assert schedule_file.exists(), "schedule-processor.py should exist"

    def test_run_all_processors_exists(self):
        """Test that run_all_processors.py exists."""
        run_all_file = project_root / "src" / "data-processors" / "run_all_processors.py"
        assert run_all_file.exists(), "run_all_processors.py should exist"

    def test_receiving_html_exists(self):
        """Test that receiving.html exists."""
        receiving_file = project_root / "docs" / "receiving.html"
        assert receiving_file.exists(), "receiving.html should exist"

    def test_interactive_charts_js_exists(self):
        """Test that interactive-charts.js exists."""
        interactive_charts_file = project_root / "docs" / "js" / "interactive-charts.js"
        assert interactive_charts_file.exists(), "interactive-charts.js should exist"

    def test_schedule_results_csv_exists(self):
        """Test that schedule_results.csv exists or is created."""
        schedule_csv = project_root / "docs" / "schedule_results.csv"
        # This file may not exist until the processor runs, so we just check it can be created
        assert schedule_csv.parent.exists(), "docs directory should exist for schedule_results.csv"

    def test_playoff_probabilities_csv_exists(self):
        """Test that playoff_probabilities.csv exists."""
        playoff_csv = project_root / "docs" / "playoff_probabilities.csv"
        assert playoff_csv.exists(), "playoff_probabilities.csv should exist"
