/**
 * NFL Stats Dashboard - Main JavaScript
 * 
 * This file handles data loading and dynamic content for the dashboard.
 * Currently uses placeholder data; will be replaced with real API calls
 * and GitHub Actions automation in future iterations.
 */

// ==========================================
// Data Storage Objects
// ==========================================

// Sample schedule data
const scheduleData = [
    {
        date: "2025-12-07",
        time: "1:00 PM ET",
        awayTeam: "Kansas City Chiefs",
        awayRecord: "11-1",
        homeTeam: "Los Angeles Chargers",
        homeRecord: "8-4",
        venue: "SoFi Stadium"
    },
    {
        date: "2025-12-07",
        time: "1:00 PM ET",
        awayTeam: "Pittsburgh Steelers",
        awayRecord: "9-3",
        homeTeam: "Cleveland Browns",
        homeRecord: "3-9",
        venue: "Huntington Bank Field"
    },
    {
        date: "2025-12-08",
        time: "4:05 PM ET",
        awayTeam: "Detroit Lions",
        awayRecord: "11-1",
        homeTeam: "Green Bay Packers",
        homeRecord: "9-3",
        venue: "Lambeau Field"
    },
    {
        date: "2025-12-08",
        time: "4:25 PM ET",
        awayTeam: "Buffalo Bills",
        awayRecord: "10-2",
        homeTeam: "Los Angeles Rams",
        homeRecord: "7-5",
        venue: "SoFi Stadium"
    },
    {
        date: "2025-12-08",
        time: "8:20 PM ET",
        awayTeam: "Cincinnati Bengals",
        awayRecord: "5-7",
        homeTeam: "Dallas Cowboys",
        homeRecord: "5-7",
        venue: "AT&T Stadium"
    }
];

// Sample team statistics
const teamStatsData = [
    { rank: 1, team: "Detroit Lions", wins: 11, losses: 1, ties: 0, winPct: ".917", pointsScored: 372, pointsAllowed: 248, differential: 124 },
    { rank: 2, team: "Kansas City Chiefs", wins: 11, losses: 1, ties: 0, winPct: ".917", pointsScored: 315, pointsAllowed: 248, differential: 67 },
    { rank: 3, team: "Buffalo Bills", wins: 10, losses: 2, ties: 0, winPct: ".833", pointsScored: 358, pointsAllowed: 270, differential: 88 },
    { rank: 4, team: "Philadelphia Eagles", wins: 10, losses: 2, ties: 0, winPct: ".833", pointsScored: 314, pointsAllowed: 245, differential: 69 },
    { rank: 5, team: "Green Bay Packers", wins: 9, losses: 3, ties: 0, winPct: ".750", pointsScored: 308, pointsAllowed: 272, differential: 36 },
    { rank: 6, team: "Pittsburgh Steelers", wins: 9, losses: 3, ties: 0, winPct: ".750", pointsScored: 297, pointsAllowed: 251, differential: 46 },
    { rank: 7, team: "Minnesota Vikings", wins: 10, losses: 2, ties: 0, winPct: ".833", pointsScored: 304, pointsAllowed: 232, differential: 72 },
    { rank: 8, team: "Los Angeles Chargers", wins: 8, losses: 4, ties: 0, winPct: ".667", pointsScored: 288, pointsAllowed: 245, differential: 43 },
    { rank: 9, team: "Baltimore Ravens", wins: 8, losses: 5, ties: 0, winPct: ".615", pointsScored: 362, pointsAllowed: 295, differential: 67 },
    { rank: 10, team: "Washington Commanders", wins: 8, losses: 5, ties: 0, winPct: ".615", pointsScored: 325, pointsAllowed: 306, differential: 19 }
];

// Sample quarterback statistics
const qbLeadersData = [
    { rank: 1, name: "Lamar Jackson", team: "BAL", games: 13, completions: 268, attempts: 379, compPct: "70.7%", yards: 3290, tds: 33, ints: 3, rating: 119.2 },
    { rank: 2, name: "Jared Goff", team: "DET", games: 12, completions: 288, attempts: 404, compPct: "71.3%", yards: 3265, tds: 25, ints: 10, rating: 106.8 },
    { rank: 3, name: "Josh Allen", team: "BUF", games: 12, completions: 254, attempts: 388, compPct: "65.5%", yards: 3033, tds: 23, ints: 5, rating: 100.7 },
    { rank: 4, name: "Joe Burrow", team: "CIN", games: 12, completions: 297, attempts: 413, compPct: "71.9%", yards: 3337, tds: 30, ints: 5, rating: 109.9 },
    { rank: 5, name: "Jalen Hurts", team: "PHI", games: 11, completions: 239, attempts: 351, compPct: "68.1%", yards: 2903, tds: 18, ints: 5, rating: 102.9 },
    { rank: 6, name: "Patrick Mahomes", team: "KC", games: 12, completions: 282, attempts: 406, compPct: "69.5%", yards: 3348, tds: 23, ints: 11, rating: 97.4 },
    { rank: 7, name: "Baker Mayfield", team: "TB", games: 12, completions: 283, attempts: 420, compPct: "67.4%", yards: 3290, tds: 28, ints: 12, rating: 99.6 },
    { rank: 8, name: "Sam Darnold", team: "MIN", games: 12, completions: 251, attempts: 370, compPct: "67.8%", yards: 2953, tds: 25, ints: 10, rating: 103.4 },
    { rank: 9, name: "Tua Tagovailoa", team: "MIA", games: 8, completions: 199, attempts: 281, compPct: "70.8%", yards: 2160, tds: 15, ints: 7, rating: 100.4 },
    { rank: 10, name: "Matthew Stafford", team: "LAR", games: 12, completions: 264, attempts: 393, compPct: "67.2%", yards: 2888, tds: 16, ints: 7, rating: 92.5 }
];

// Sample receiver statistics
const receiverLeadersData = [
    { rank: 1, name: "Ja'Marr Chase", team: "CIN", games: 12, receptions: 93, targets: 127, yards: 1319, avg: 14.2, tds: 15, long: 70, ypg: 109.9 },
    { rank: 2, name: "Amon-Ra St. Brown", team: "DET", games: 12, receptions: 84, targets: 110, yards: 945, avg: 11.3, tds: 11, long: 45, ypg: 78.8 },
    { rank: 3, name: "Justin Jefferson", team: "MIN", games: 12, receptions: 79, targets: 112, yards: 1079, avg: 13.7, tds: 8, long: 68, ypg: 89.9 },
    { rank: 4, name: "CeeDee Lamb", team: "DAL", games: 12, receptions: 82, targets: 119, yards: 1005, avg: 12.3, tds: 6, long: 55, ypg: 83.8 },
    { rank: 5, name: "Zay Flowers", team: "BAL", games: 13, receptions: 60, targets: 90, yards: 1047, avg: 17.5, tds: 4, long: 62, ypg: 80.5 },
    { rank: 6, name: "Terry McLaurin", team: "WAS", games: 13, receptions: 68, targets: 105, yards: 982, avg: 14.4, tds: 10, long: 61, ypg: 75.5 },
    { rank: 7, name: "Mike Evans", team: "TB", games: 11, receptions: 57, targets: 96, yards: 850, avg: 14.9, tds: 8, long: 57, ypg: 77.3 },
    { rank: 8, name: "A.J. Brown", team: "PHI", games: 11, receptions: 56, targets: 88, yards: 830, avg: 14.8, tds: 7, long: 67, ypg: 75.5 },
    { rank: 9, name: "George Pickens", team: "PIT", games: 12, receptions: 55, targets: 91, yards: 900, avg: 16.4, tds: 3, long: 74, ypg: 75.0 },
    { rank: 10, name: "Tyreek Hill", team: "MIA", games: 12, receptions: 60, targets: 98, yards: 879, avg: 14.7, tds: 6, long: 80, ypg: 73.3 }
];

// Sample rushing statistics
const rushingLeadersData = [
    { rank: 1, name: "Saquon Barkley", team: "PHI", games: 12, attempts: 255, yards: 1499, avg: 5.9, tds: 11, long: 72, ypg: 124.9, fumbles: 2 },
    { rank: 2, name: "Derrick Henry", team: "BAL", games: 13, attempts: 243, yards: 1407, avg: 5.8, tds: 13, long: 87, ypg: 108.2, fumbles: 1 },
    { rank: 3, name: "Josh Jacobs", team: "GB", games: 12, attempts: 228, yards: 1024, avg: 4.5, tds: 11, long: 58, ypg: 85.3, fumbles: 0 },
    { rank: 4, name: "Jahmyr Gibbs", team: "DET", games: 12, attempts: 176, yards: 1019, avg: 5.8, tds: 11, long: 70, ypg: 84.9, fumbles: 2 },
    { rank: 5, name: "De'Von Achane", team: "MIA", games: 11, attempts: 144, yards: 701, avg: 4.9, tds: 6, long: 50, ypg: 63.7, fumbles: 1 },
    { rank: 6, name: "James Cook", team: "BUF", games: 12, attempts: 165, yards: 757, avg: 4.6, tds: 12, long: 44, ypg: 63.1, fumbles: 0 },
    { rank: 7, name: "Jordan Mason", team: "SF", games: 11, attempts: 161, yards: 789, avg: 4.9, tds: 3, long: 38, ypg: 71.7, fumbles: 1 },
    { rank: 8, name: "Kyren Williams", team: "LAR", games: 11, attempts: 167, yards: 665, avg: 4.0, tds: 11, long: 26, ypg: 60.5, fumbles: 3 },
    { rank: 9, name: "Kenneth Walker III", team: "SEA", games: 11, attempts: 153, yards: 644, avg: 4.2, tds: 8, long: 26, ypg: 58.5, fumbles: 2 },
    { rank: 10, name: "Bijan Robinson", team: "ATL", games: 12, attempts: 172, yards: 840, avg: 4.9, tds: 6, long: 37, ypg: 70.0, fumbles: 1 }
];

// ==========================================
// Table Population Functions
// ==========================================

/**
 * Populate the schedule table with game data
 * Now uses live API data and fetches remaining weeks of the season
 */
async function populateScheduleTable() {
    const table = document.getElementById('schedule-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '<tr><td colspan="10" class="loading">Loading schedule data...</td></tr>';

    try {
        const allGames = [];
        const currentWeek = 14;
        const finalWeek = 18; // Regular season ends at week 18
        
        // Fetch remaining weeks of the season
        for (let week = currentWeek; week <= finalWeek; week++) {
            try {
                const weekGames = await NFLAPI.getSchedule(week);
                if (weekGames && weekGames.length > 0) {
                    // Add week header information to each game
                    weekGames.forEach(game => {
                        game.week = week;
                    });
                    allGames.push(...weekGames);
                }
            } catch (error) {
                console.warn(`Could not load week ${week}:`, error.message);
            }
        }
        
        if (allGames.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" class="loading">No games scheduled.</td></tr>';
            return;
        }

        // Try to load betting odds
        let oddsData = null;
        try {
            oddsData = await loadBettingOdds();
        } catch (error) {
            console.warn('Could not load betting odds:', error.message);
        }

        tbody.innerHTML = '';
        
        let lastWeek = null;
        allGames.forEach(game => {
            // Add week separator row
            if (game.week !== lastWeek) {
                const weekRow = tbody.insertRow();
                weekRow.className = 'week-separator';
                weekRow.innerHTML = `<td colspan="10" style="background-color: var(--primary-color); color: white; font-weight: bold; padding: 0.75rem; text-align: center;">Week ${game.week}</td>`;
                lastWeek = game.week;
            }
            
            // Find odds for this game
            const gameOdds = findOddsForGame(game, oddsData);
            
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${formatDate(game.date)}</td>
                <td>${game.time}</td>
                <td>${game.awayTeam}</td>
                <td>${game.awayRecord}</td>
                <td>${game.homeTeam}</td>
                <td>${game.homeRecord}</td>
                <td>${game.venue}</td>
                <td class="odds-column odds-cell" style="display: none;">${gameOdds.spread}</td>
                <td class="odds-column odds-cell" style="display: none;">${gameOdds.moneyline}</td>
                <td class="odds-column odds-cell" style="display: none;">${gameOdds.total}</td>
            `;
        });
        
        console.log(`Loaded ${allGames.length} games from weeks ${currentWeek}-${finalWeek}`);
        
        // Initialize odds toggle functionality
        initializeOddsToggle();
    } catch (error) {
        console.error('Error loading schedule:', error);
        tbody.innerHTML = '<tr><td colspan="10" class="loading" style="color: #D50A0A;">Error loading schedule. Please refresh the page to try again.</td></tr>';
    }
}

/**
 * Populate the team statistics table
 * Now uses live API data instead of placeholder data
 */
async function populateTeamStatsTable() {
    const table = document.getElementById('team-stats-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '<tr><td colspan="9" class="loading">Loading team statistics...</td></tr>';

    try {
        // Fetch team stats from API
        const teamStatsData = await NFLAPI.getTeamStats();
        
        if (!teamStatsData || teamStatsData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="loading">No team data available.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        
        teamStatsData.forEach(team => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${team.rank}</td>
                <td>${team.team}</td>
                <td>${team.wins}</td>
                <td>${team.losses}</td>
                <td>${team.ties}</td>
                <td>${team.winPct}</td>
                <td>${team.pointsScored}</td>
                <td>${team.pointsAllowed}</td>
                <td>${team.differential > 0 ? '+' : ''}${team.differential}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading team stats:', error);
        tbody.innerHTML = '<tr><td colspan="9" class="loading" style="color: #D50A0A;">Error loading team statistics. Please refresh the page to try again.</td></tr>';
    }
}

/**
 * Populate the quarterback leaders table
 * Now uses live API data instead of placeholder data
 */
async function populateQBLeadersTable() {
    const table = document.getElementById('qb-leaders-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '<tr><td colspan="11" class="loading">Loading quarterback statistics...</td></tr>';

    try {
        // Fetch QB stats from API
        const qbLeadersData = await NFLAPI.getQBStats();
        
        if (!qbLeadersData || qbLeadersData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="11" class="loading">No quarterback data available.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        
        qbLeadersData.forEach(qb => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${qb.rank}</td>
                <td>${qb.name}</td>
                <td>${qb.team}</td>
                <td>${qb.games}</td>
                <td>${qb.completions}</td>
                <td>${qb.attempts}</td>
                <td>${qb.compPct}</td>
                <td>${qb.yards}</td>
                <td>${qb.tds}</td>
                <td>${qb.ints}</td>
                <td>${qb.rating}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading QB stats:', error);
        tbody.innerHTML = '<tr><td colspan="11" class="loading" style="color: #D50A0A;">Error loading quarterback statistics. Please refresh the page to try again.</td></tr>';
    }
}

/**
 * Populate the receiver leaders table
 * Now uses live API data instead of placeholder data
 */
async function populateReceiverLeadersTable() {
    const table = document.getElementById('receiver-leaders-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '<tr><td colspan="11" class="loading">Loading receiver statistics...</td></tr>';

    try {
        // Fetch receiver stats from API
        const receiverLeadersData = await NFLAPI.getReceiverStats();
        
        if (!receiverLeadersData || receiverLeadersData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="11" class="loading">No receiver data available.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        
        receiverLeadersData.forEach(receiver => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${receiver.rank}</td>
                <td>${receiver.name}</td>
                <td>${receiver.team}</td>
                <td>${receiver.games}</td>
                <td>${receiver.receptions}</td>
                <td>${receiver.targets}</td>
                <td>${receiver.yards}</td>
                <td>${receiver.avg}</td>
                <td>${receiver.tds}</td>
                <td>${receiver.long}</td>
                <td>${receiver.ypg}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading receiver stats:', error);
        tbody.innerHTML = '<tr><td colspan="11" class="loading" style="color: #D50A0A;">Error loading receiver statistics. Please refresh the page to try again.</td></tr>';
    }
}

/**
 * Populate the rushing leaders table
 * Now uses live API data instead of placeholder data
 */
async function populateRushingLeadersTable() {
    const table = document.getElementById('rushing-leaders-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '<tr><td colspan="11" class="loading">Loading rushing statistics...</td></tr>';

    try {
        // Fetch rushing stats from API
        const rushingLeadersData = await NFLAPI.getRushingStats();
        
        if (!rushingLeadersData || rushingLeadersData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="11" class="loading">No rushing data available.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        
        rushingLeadersData.forEach(rusher => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${rusher.rank}</td>
                <td>${rusher.name}</td>
                <td>${rusher.team}</td>
                <td>${rusher.games}</td>
                <td>${rusher.attempts}</td>
                <td>${rusher.yards}</td>
                <td>${rusher.avg}</td>
                <td>${rusher.tds}</td>
                <td>${rusher.long}</td>
                <td>${rusher.ypg}</td>
                <td>${rusher.fumbles}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading rushing stats:', error);
        tbody.innerHTML = '<tr><td colspan="11" class="loading" style="color: #D50A0A;">Error loading rushing statistics. Please refresh the page to try again.</td></tr>';
    }
}

// ==========================================
// Utility Functions
// ==========================================

/**
 * Format date string to more readable format
 * @param {string} dateString - Date in YYYY-MM-DD format
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { weekday: 'short', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// ==========================================
// Initialization
// ==========================================

/**
 * Initialize the dashboard based on current page
 */
document.addEventListener('DOMContentLoaded', async function() {
    // Initialize common features on all pages
    initializeScrollToTop();
    initializeKeyboardNavigation();
    
    // Determine which page we're on and populate accordingly
    if (document.getElementById('schedule-table')) {
        await populateScheduleTable();
        makeTableSortable('schedule-table');
    }
    
    if (document.getElementById('team-stats-table')) {
        await populateTeamStatsTable();
        makeTableSortable('team-stats-table');
    }
    
    if (document.getElementById('qb-leaders-table')) {
        await populateQBLeadersTable();
        makeTableSortable('qb-leaders-table');
        // Initialize search and filter for QB leaders
        initializeSearch('qb-search', 'qb-leaders-table', 1);
        initializeTeamFilter('qb-team-filter', 'qb-leaders-table', 2);
    }
    
    if (document.getElementById('receiver-leaders-table')) {
        await populateReceiverLeadersTable();
        makeTableSortable('receiver-leaders-table');
        // Initialize search and filter for receivers
        initializeSearch('receiver-search', 'receiver-leaders-table', 1);
        initializeTeamFilter('receiver-team-filter', 'receiver-leaders-table', 2);
    }
    
    if (document.getElementById('rushing-leaders-table')) {
        await populateRushingLeadersTable();
        makeTableSortable('rushing-leaders-table');
        // Initialize search and filter for rushers
        initializeSearch('rushing-search', 'rushing-leaders-table', 1);
        initializeTeamFilter('rushing-team-filter', 'rushing-leaders-table', 2);
    }
    
    // Check if we're on the defensive leaders page
    if (document.getElementById('tackles-leaders-table')) {
        initializeStatTabs();
        await populateDefensiveLeadersTables();
        // Make all defensive tables sortable
        makeTableSortable('tackles-leaders-table');
        makeTableSortable('sacks-leaders-table');
        makeTableSortable('interceptions-leaders-table');
        // Initialize search and filters for each category
        initializeSearch('tackles-search', 'tackles-leaders-table', 1);
        initializeTeamFilter('tackles-team-filter', 'tackles-leaders-table', 2);
        initializeSearch('sacks-search', 'sacks-leaders-table', 1);
        initializeTeamFilter('sacks-team-filter', 'sacks-leaders-table', 2);
        initializeSearch('interceptions-search', 'interceptions-leaders-table', 1);
        initializeTeamFilter('interceptions-team-filter', 'interceptions-leaders-table', 2);
    }
    
    // Check if we're on the special teams page
    if (document.getElementById('kickers-leaders-table')) {
        initializeStatTabs();
        await populateSpecialTeamsTables();
        // Make all special teams tables sortable
        makeTableSortable('kickers-leaders-table');
        makeTableSortable('punters-leaders-table');
        makeTableSortable('returners-leaders-table');
        // Initialize search and filters
        initializeSearch('kickers-search', 'kickers-leaders-table', 1);
        initializeTeamFilter('kickers-team-filter', 'kickers-leaders-table', 2);
        initializeSearch('punters-search', 'punters-leaders-table', 1);
        initializeTeamFilter('punters-team-filter', 'punters-leaders-table', 2);
        initializeSearch('returners-search', 'returners-leaders-table', 1);
        initializeTeamFilter('returners-team-filter', 'returners-leaders-table', 2);
    }
    
    // Check if we're on the league leaders page
    if (document.getElementById('passing-yards-leaders')) {
        await populateLeagueLeaders();
    }
    
    // Check if we're on the playoff picture page
    if (document.querySelector('.playoff-conferences')) {
        await populatePlayoffPicture();
    }
    
    // Check if we're on the standings page
    if (document.getElementById('afc-east-table')) {
        await populateStandingsTables();
        // Make all division tables sortable
        ['afc-east', 'afc-north', 'afc-south', 'afc-west',
         'nfc-east', 'nfc-north', 'nfc-south', 'nfc-west'].forEach(divId => {
            makeTableSortable(`${divId}-table`);
        });
    }
});

// ==========================================
// Future Enhancement Placeholders
// ==========================================

/**
 * TODO: Implement API data fetching
 * This function will replace hardcoded data with real API calls
 */
function fetchDataFromAPI() {
    // Will be implemented with GitHub Actions automation
    // to fetch real-time NFL data
}

/**
 * TODO: Implement data caching
 * Cache API responses to reduce load times
 */
function cacheData() {
    // Will use localStorage or sessionStorage
    // to cache API responses
}

// ==========================================
// Table Sorting Functionality
// ==========================================

/**
 * Make a table sortable by clicking column headers
 * @param {string} tableId - The ID of the table element
 */
function makeTableSortable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const headers = table.querySelectorAll('thead th');
    const tbody = table.querySelector('tbody');
    
    headers.forEach((header, columnIndex) => {
        // Skip if header is not sortable (has class 'no-sort')
        if (header.classList.contains('no-sort')) return;
        
        // Add sorting indicator
        header.style.cursor = 'pointer';
        header.title = 'Click to sort';
        
        // Add click event listener
        header.addEventListener('click', () => {
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const currentDirection = header.dataset.sortDirection || 'none';
            const isAscending = currentDirection !== 'asc';
            
            // Remove sort indicators from all headers
            headers.forEach(h => {
                h.classList.remove('sort-asc', 'sort-desc');
                h.dataset.sortDirection = 'none';
            });
            
            // Add sort indicator to clicked header
            if (isAscending) {
                header.classList.add('sort-asc');
                header.dataset.sortDirection = 'asc';
            } else {
                header.classList.add('sort-desc');
                header.dataset.sortDirection = 'desc';
            }
            
            // Sort rows
            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[columnIndex]?.textContent.trim() || '';
                const cellB = rowB.cells[columnIndex]?.textContent.trim() || '';
                
                // Try to parse as numbers (handle percentages, decimals, commas)
                const numA = parseFloat(cellA.replace(/[,%+]/g, ''));
                const numB = parseFloat(cellB.replace(/[,%+]/g, ''));
                
                let comparison = 0;
                
                // If both are valid numbers, compare numerically
                if (!isNaN(numA) && !isNaN(numB)) {
                    comparison = numA - numB;
                } 
                // Otherwise compare as strings
                else {
                    comparison = cellA.localeCompare(cellB, undefined, { numeric: true });
                }
                
                return isAscending ? comparison : -comparison;
            });
            
            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });
}

/**
 * Populate standings tables organized by division
 */
async function populateStandingsTables() {
    try {
        // Show loading state
        const divisionIds = [
            'afc-east', 'afc-north', 'afc-south', 'afc-west',
            'nfc-east', 'nfc-north', 'nfc-south', 'nfc-west'
        ];
        
        divisionIds.forEach(divId => {
            const tableBody = document.querySelector(`#${divId}-table tbody`);
            if (tableBody) {
                tableBody.innerHTML = '<tr><td colspan="9" class="loading">Loading...</td></tr>';
            }
        });
        
        // Fetch standings data
        const standings = await fetchStandings();
        
        // Populate each division table
        for (const [divisionKey, teams] of Object.entries(standings)) {
            const tableBody = document.querySelector(`#${divisionKey}-table tbody`);
            if (!tableBody) continue;
            
            if (teams.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="9">No data available</td></tr>';
                continue;
            }
            
            // Create rows for each team
            const rows = teams.map(team => `
                <tr>
                    <td>${team.team}</td>
                    <td>${team.wins}</td>
                    <td>${team.losses}</td>
                    <td>${team.ties}</td>
                    <td>${team.winPct}</td>
                    <td>${team.pointsScored}</td>
                    <td>${team.pointsAllowed}</td>
                    <td>${team.differential > 0 ? '+' : ''}${team.differential}</td>
                    <td>${team.streak}</td>
                </tr>
            `).join('');
            
            tableBody.innerHTML = rows;
        }
        
        console.log('Standings tables populated successfully');
    } catch (error) {
        console.error('Error populating standings:', error);
        
        // Show error in all tables
        const divisionIds = [
            'afc-east', 'afc-north', 'afc-south', 'afc-west',
            'nfc-east', 'nfc-north', 'nfc-south', 'nfc-west'
        ];
        
        divisionIds.forEach(divId => {
            const tableBody = document.querySelector(`#${divId}-table tbody`);
            if (tableBody) {
                tableBody.innerHTML = `<tr><td colspan="9" class="error">Error loading standings: ${error.message}</td></tr>`;
            }
        });
    }
}

/**
 * Initialize sorting for all tables on the page
 */
function initializeTableSorting() {
    // Find all tables with data-sortable attribute or specific IDs
    const sortableTables = [
        'schedule-table',
        'team-stats-table',
        'qb-leaders-table',
        'receiver-leaders-table',
        'rushing-leaders-table',
        'afc-east-table',
        'afc-north-table',
        'afc-south-table',
        'afc-west-table',
        'nfc-east-table',
        'nfc-north-table',
        'nfc-south-table',
        'nfc-west-table'
    ];
    
    sortableTables.forEach(tableId => {
        makeTableSortable(tableId);
    });
}

// ==========================================
// Search and Filter Functions
// ==========================================

/**
 * Initialize search functionality for a table
 * @param {string} searchInputId - ID of the search input
 * @param {string} tableId - ID of the table to search
 * @param {number} nameColumnIndex - Index of the column containing names
 */
function initializeSearch(searchInputId, tableId, nameColumnIndex = 1) {
    const searchInput = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    
    if (!searchInput || !table) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const tbody = table.querySelector('tbody');
        const rows = tbody.querySelectorAll('tr');
        
        let visibleCount = 0;
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length === 0) return; // Skip empty rows
            
            const nameCell = cells[nameColumnIndex];
            if (!nameCell) return;
            
            const name = nameCell.textContent.toLowerCase();
            if (name.includes(searchTerm)) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Show message if no results
        if (visibleCount === 0 && rows.length > 0) {
            const loadingRow = tbody.querySelector('.loading');
            if (!loadingRow) {
                const messageRow = document.createElement('tr');
                messageRow.className = 'no-results';
                messageRow.innerHTML = `<td colspan="${table.querySelector('thead tr').cells.length}" style="text-align: center; padding: 2rem;">No players found matching "${e.target.value}"</td>`;
                tbody.appendChild(messageRow);
            }
        } else {
            const noResultsRow = tbody.querySelector('.no-results');
            if (noResultsRow) {
                noResultsRow.remove();
            }
        }
    });
}

/**
 * Initialize team filter functionality for a table
 * @param {string} selectId - ID of the select dropdown
 * @param {string} tableId - ID of the table to filter
 * @param {number} teamColumnIndex - Index of the column containing team abbreviations
 */
function initializeTeamFilter(selectId, tableId, teamColumnIndex = 2) {
    const select = document.getElementById(selectId);
    const table = document.getElementById(tableId);
    
    if (!select || !table) return;
    
    // Populate team filter options from table data
    const populateTeamOptions = () => {
        const tbody = table.querySelector('tbody');
        const rows = tbody.querySelectorAll('tr');
        const teams = new Set();
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length > teamColumnIndex) {
                const team = cells[teamColumnIndex].textContent.trim();
                if (team && team !== 'Team') {
                    teams.add(team);
                }
            }
        });
        
        // Sort teams alphabetically
        const sortedTeams = Array.from(teams).sort();
        
        // Clear existing options (except "All Teams")
        select.innerHTML = '<option value="">All Teams</option>';
        
        // Add team options
        sortedTeams.forEach(team => {
            const option = document.createElement('option');
            option.value = team;
            option.textContent = team;
            select.appendChild(option);
        });
    };
    
    // Filter table by selected team
    select.addEventListener('change', (e) => {
        const selectedTeam = e.target.value;
        const tbody = table.querySelector('tbody');
        const rows = tbody.querySelectorAll('tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length === 0) return;
            
            const teamCell = cells[teamColumnIndex];
            if (!teamCell) return;
            
            if (selectedTeam === '' || teamCell.textContent.trim() === selectedTeam) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
    
    // Populate options when table data is loaded
    const observer = new MutationObserver(() => {
        const tbody = table.querySelector('tbody');
        if (tbody && tbody.querySelectorAll('tr:not(.loading)').length > 0) {
            populateTeamOptions();
            observer.disconnect();
        }
    });
    
    observer.observe(table, { childList: true, subtree: true });
}

// ==========================================
// Scroll to Top Button
// ==========================================

/**
 * Initialize scroll to top button functionality
 */
function initializeScrollToTop() {
    const scrollBtn = document.getElementById('scroll-to-top');
    if (!scrollBtn) return;
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });
    
    // Scroll to top when clicked
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Keyboard support (Enter or Space)
    scrollBtn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    });
}

// ==========================================
// Stat Tabs for Multi-Category Pages
// ==========================================

/**
 * Initialize stat category tabs (for defensive leaders, etc.)
 */
function initializeStatTabs() {
    const tabs = document.querySelectorAll('.stat-tab');
    const sections = document.querySelectorAll('.stat-section');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const category = tab.dataset.category;
            
            // Remove active class from all tabs and sections
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding section
            tab.classList.add('active');
            const activeSection = document.getElementById(`${category}-section`);
            if (activeSection) {
                activeSection.classList.add('active');
            }
        });
        
        // Keyboard support
        tab.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                tab.click();
            }
        });
    });
}

// ==========================================
// Defensive Stats Population
// ==========================================

/**
 * Populate all defensive leaders tables
 */
async function populateDefensiveLeadersTables() {
    // For now, use placeholder data until ESPN API defensive stats are implemented
    populateTacklesLeadersTable();
    populateSacksLeadersTable();
    populateInterceptionsLeadersTable();
}

/**
 * Populate tackles leaders table
 */
function populateTacklesLeadersTable() {
    const tableBody = document.querySelector('#tackles-leaders-table tbody');
    if (!tableBody) return;
    
    // Placeholder data - will be replaced with API data
    const tacklesData = [
        { rank: 1, name: "Bobby Wagner", team: "SEA", games: 13, total: 142, solo: 89, assisted: 53, tfl: 8, sacks: 2.0, avg: 10.9 },
        { rank: 2, name: "Roquan Smith", team: "BAL", games: 13, total: 138, solo: 92, assisted: 46, tfl: 12, sacks: 3.5, avg: 10.6 },
        { rank: 3, name: "Fred Warner", team: "SF", games: 13, total: 135, solo: 85, assisted: 50, tfl: 7, sacks: 1.5, avg: 10.4 },
        { rank: 4, name: "Zaire Franklin", team: "IND", games: 13, total: 128, solo: 78, assisted: 50, tfl: 5, sacks: 1.0, avg: 9.8 },
        { rank: 5, name: "Foyesade Oluokun", team: "JAX", games: 13, total: 125, solo: 81, assisted: 44, tfl: 6, sacks: 0.5, avg: 9.6 },
        { rank: 6, name: "CJ Mosley", team: "NYJ", games: 13, total: 122, solo: 74, assisted: 48, tfl: 9, sacks: 2.5, avg: 9.4 },
        { rank: 7, name: "TJ Edwards", team: "CHI", games: 13, total: 118, solo: 72, assisted: 46, tfl: 4, sacks: 1.0, avg: 9.1 },
        { rank: 8, name: "Devin Lloyd", team: "JAX", games: 13, total: 115, solo: 70, assisted: 45, tfl: 10, sacks: 3.0, avg: 8.8 },
        { rank: 9, name: "Ernest Jones", team: "LAR", games: 13, total: 112, solo: 68, assisted: 44, tfl: 6, sacks: 1.5, avg: 8.6 },
        { rank: 10, name: "Demario Davis", team: "NO", games: 13, total: 110, solo: 67, assisted: 43, tfl: 7, sacks: 2.0, avg: 8.5 }
    ];
    
    const rows = tacklesData.map(player => `
        <tr>
            <td>${player.rank}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.games}</td>
            <td>${player.total}</td>
            <td>${player.solo}</td>
            <td>${player.assisted}</td>
            <td>${player.tfl}</td>
            <td>${player.sacks}</td>
            <td>${player.avg}</td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = rows;
}

/**
 * Populate sacks leaders table
 */
function populateSacksLeadersTable() {
    const tableBody = document.querySelector('#sacks-leaders-table tbody');
    if (!tableBody) return;
    
    // Placeholder data
    const sacksData = [
        { rank: 1, name: "TJ Watt", team: "PIT", games: 13, sacks: 14.5, tfl: 18, qbHits: 28, tackles: 52, ff: 4, avg: 1.12 },
        { rank: 2, name: "Myles Garrett", team: "CLE", games: 13, sacks: 13.0, tfl: 16, qbHits: 26, tackles: 48, ff: 3, avg: 1.00 },
        { rank: 3, name: "Micah Parsons", team: "DAL", games: 13, sacks: 12.5, tfl: 15, qbHits: 25, tackles: 55, ff: 5, avg: 0.96 },
        { rank: 4, name: "Maxx Crosby", team: "LV", games: 13, sacks: 11.5, tfl: 14, qbHits: 24, tackles: 60, ff: 2, avg: 0.88 },
        { rank: 5, name: "Nick Bosa", team: "SF", games: 13, sacks: 11.0, tfl: 13, qbHits: 22, tackles: 50, ff: 3, avg: 0.85 },
        { rank: 6, name: "Chris Jones", team: "KC", games: 13, sacks: 10.5, tfl: 12, qbHits: 21, tackles: 45, ff: 2, avg: 0.81 },
        { rank: 7, name: "Danielle Hunter", team: "HOU", games: 13, sacks: 10.0, tfl: 11, qbHits: 20, tackles: 42, ff: 3, avg: 0.77 },
        { rank: 8, name: "Josh Allen", team: "JAX", games: 13, sacks: 9.5, tfl: 10, qbHits: 19, tackles: 38, ff: 1, avg: 0.73 },
        { rank: 9, name: "Rashan Gary", team: "GB", games: 13, sacks: 9.0, tfl: 9, qbHits: 18, tackles: 40, ff: 2, avg: 0.69 },
        { rank: 10, name: "Montez Sweat", team: "CHI", games: 13, sacks: 8.5, tfl: 8, qbHits: 17, tackles: 35, ff: 1, avg: 0.65 }
    ];
    
    const rows = sacksData.map(player => `
        <tr>
            <td>${player.rank}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.games}</td>
            <td>${player.sacks}</td>
            <td>${player.tfl}</td>
            <td>${player.qbHits}</td>
            <td>${player.tackles}</td>
            <td>${player.ff}</td>
            <td>${player.avg}</td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = rows;
}

/**
 * Populate interceptions leaders table
 */
function populateInterceptionsLeadersTable() {
    const tableBody = document.querySelector('#interceptions-leaders-table tbody');
    if (!tableBody) return;
    
    // Placeholder data
    const interceptionsData = [
        { rank: 1, name: "DaRon Bland", team: "DAL", games: 13, ints: 7, intYards: 165, intTDs: 3, pd: 12, ff: 2, long: 54 },
        { rank: 2, name: "Trevon Diggs", team: "DAL", games: 13, ints: 6, intYards: 142, intTDs: 2, pd: 15, ff: 1, long: 61 },
        { rank: 3, name: "Devon Witherspoon", team: "SEA", games: 13, ints: 6, intYards: 128, intTDs: 1, pd: 11, ff: 3, long: 48 },
        { rank: 4, name: "Jaylon Johnson", team: "CHI", games: 13, ints: 5, intYards: 115, intTDs: 2, pd: 13, ff: 0, long: 52 },
        { rank: 5, name: "Patrick Surtain II", team: "DEN", games: 13, ints: 5, intYards: 98, intTDs: 1, pd: 14, ff: 1, long: 45 },
        { rank: 6, name: "Sauce Gardner", team: "NYJ", games: 13, ints: 5, intYards: 82, intTDs: 0, pd: 16, ff: 2, long: 38 },
        { rank: 7, name: "CJ Gardner-Johnson", team: "PHI", games: 13, ints: 4, intYards: 105, intTDs: 1, pd: 10, ff: 1, long: 44 },
        { rank: 8, name: "Kerby Joseph", team: "DET", games: 13, ints: 4, intYards: 92, intTDs: 1, pd: 9, ff: 0, long: 42 },
        { rank: 9, name: "Brian Branch", team: "DET", games: 13, ints: 4, intYards: 78, intTDs: 0, pd: 8, ff: 2, long: 36 },
        { rank: 10, name: "Kyle Hamilton", team: "BAL", games: 13, ints: 4, intYards: 65, intTDs: 0, pd: 7, ff: 1, long: 31 }
    ];
    
    const rows = interceptionsData.map(player => `
        <tr>
            <td>${player.rank}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.games}</td>
            <td>${player.ints}</td>
            <td>${player.intYards}</td>
            <td>${player.intTDs}</td>
            <td>${player.pd}</td>
            <td>${player.ff}</td>
            <td>${player.long}</td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = rows;
}

// ==========================================
// Special Teams Stats Population
// ==========================================

/**
 * Populate all special teams tables
 */
async function populateSpecialTeamsTables() {
    populateKickersLeadersTable();
    populatePuntersLeadersTable();
    populateReturnersLeadersTable();
}

/**
 * Populate kickers leaders table
 */
function populateKickersLeadersTable() {
    const tableBody = document.querySelector('#kickers-leaders-table tbody');
    if (!tableBody) return;
    
    // Placeholder data
    const kickersData = [
        { rank: 1, name: "Harrison Butker", team: "KC", fgm: 28, fga: 30, fgPct: "93.3%", long: 58, xpm: 45, xpa: 46, points: 129 },
        { rank: 2, name: "Justin Tucker", team: "BAL", fgm: 27, fga: 31, fgPct: "87.1%", long: 61, xpm: 42, xpa: 43, points: 123 },
        { rank: 3, name: "Jake Moody", team: "SF", fgm: 26, fga: 29, fgPct: "89.7%", long: 57, xpm: 44, xpa: 45, points: 122 },
        { rank: 4, name: "Brandon Aubrey", team: "DAL", fgm: 29, fga: 32, fgPct: "90.6%", long: 60, xpm: 35, xpa: 36, points: 122 },
        { rank: 5, name: "Cameron Dicker", team: "LAC", fgm: 25, fga: 28, fgPct: "89.3%", long: 55, xpm: 43, xpa: 44, points: 118 },
        { rank: 6, name: "Jason Myers", team: "SEA", fgm: 24, fga: 27, fgPct: "88.9%", long: 56, xpm: 46, xpa: 47, points: 118 },
        { rank: 7, name: "Tyler Bass", team: "BUF", fgm: 26, fga: 30, fgPct: "86.7%", long: 54, xpm: 40, xpa: 41, points: 118 },
        { rank: 8, name: "Jake Elliott", team: "PHI", fgm: 25, fga: 29, fgPct: "86.2%", long: 59, xpm: 41, xpa: 42, points: 116 },
        { rank: 9, name: "Younghoe Koo", team: "ATL", fgm: 23, fga: 26, fgPct: "88.5%", long: 53, xpm: 44, xpa: 45, points: 113 },
        { rank: 10, name: "Chris Boswell", team: "PIT", fgm: 24, fga: 28, fgPct: "85.7%", long: 57, xpm: 38, xpa: 39, points: 110 }
    ];
    
    const rows = kickersData.map(player => `
        <tr>
            <td>${player.rank}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.fgm}</td>
            <td>${player.fga}</td>
            <td>${player.fgPct}</td>
            <td>${player.long}</td>
            <td>${player.xpm}</td>
            <td>${player.xpa}</td>
            <td>${player.points}</td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = rows;
}

/**
 * Populate punters leaders table
 */
function populatePuntersLeadersTable() {
    const tableBody = document.querySelector('#punters-leaders-table tbody');
    if (!tableBody) return;
    
    // Placeholder data
    const puntersData = [
        { rank: 1, name: "Bryan Anger", team: "DAL", punts: 58, yards: 2784, avg: 48.0, netAvg: 42.8, long: 72, inside20: 22, tb: 8 },
        { rank: 2, name: "AJ Cole", team: "LV", punts: 72, yards: 3456, avg: 48.0, netAvg: 42.1, long: 68, inside20: 28, tb: 10 },
        { rank: 3, name: "Jake Bailey", team: "MIA", punts: 65, yards: 3120, avg: 48.0, netAvg: 41.9, long: 70, inside20: 25, tb: 9 },
        { rank: 4, name: "Tommy Townsend", team: "HOU", punts: 60, yards: 2880, avg: 48.0, netAvg: 42.5, long: 69, inside20: 24, tb: 7 },
        { rank: 5, name: "Logan Cooke", team: "JAX", punts: 68, yards: 3264, avg: 48.0, netAvg: 41.7, long: 71, inside20: 26, tb: 11 },
        { rank: 6, name: "Bradley Pinion", team: "ATL", punts: 70, yards: 3360, avg: 48.0, netAvg: 41.5, long: 67, inside20: 27, tb: 12 },
        { rank: 7, name: "Jack Fox", team: "DET", punts: 52, yards: 2496, avg: 48.0, netAvg: 43.2, long: 73, inside20: 20, tb: 6 },
        { rank: 8, name: "Tress Way", team: "WSH", punts: 75, yards: 3600, avg: 48.0, netAvg: 41.3, long: 66, inside20: 29, tb: 13 },
        { rank: 9, name: "Mitch Wishnowsky", team: "SF", punts: 55, yards: 2640, avg: 48.0, netAvg: 42.9, long: 68, inside20: 21, tb: 7 },
        { rank: 10, name: "Ryan Stonehouse", team: "TEN", punts: 78, yards: 3744, avg: 48.0, netAvg: 41.0, long: 70, inside20: 30, tb: 14 }
    ];
    
    const rows = puntersData.map(player => `
        <tr>
            <td>${player.rank}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.punts}</td>
            <td>${player.yards}</td>
            <td>${player.avg}</td>
            <td>${player.netAvg}</td>
            <td>${player.long}</td>
            <td>${player.inside20}</td>
            <td>${player.tb}</td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = rows;
}

/**
 * Populate return specialists leaders table
 */
function populateReturnersLeadersTable() {
    const tableBody = document.querySelector('#returners-leaders-table tbody');
    if (!tableBody) return;
    
    // Placeholder data
    const returnersData = [
        { rank: 1, name: "KaVontae Turpin", team: "DAL", kr: 28, krYards: 756, krAvg: 27.0, pr: 22, prYards: 308, prAvg: 14.0, tds: 2 },
        { rank: 2, name: "Derius Davis", team: "LAC", kr: 30, krYards: 780, krAvg: 26.0, pr: 18, prYards: 252, prAvg: 14.0, tds: 1 },
        { rank: 3, name: "DeeJay Dallas", team: "ARI", kr: 32, krYards: 800, krAvg: 25.0, pr: 15, prYards: 195, prAvg: 13.0, tds: 1 },
        { rank: 4, name: "Jamal Agnew", team: "JAX", kr: 25, krYards: 625, krAvg: 25.0, pr: 20, prYards: 280, prAvg: 14.0, tds: 2 },
        { rank: 5, name: "Brandon Powell", team: "MIN", kr: 22, krYards: 550, krAvg: 25.0, pr: 25, prYards: 325, prAvg: 13.0, tds: 1 },
        { rank: 6, name: "Mecole Hardman", team: "NYJ", kr: 27, krYards: 675, krAvg: 25.0, pr: 16, prYards: 208, prAvg: 13.0, tds: 0 },
        { rank: 7, name: "Kalif Raymond", team: "DET", kr: 18, krYards: 450, krAvg: 25.0, pr: 28, prYards: 364, prAvg: 13.0, tds: 1 },
        { rank: 8, name: "Rondale Moore", team: "ATL", kr: 24, krYards: 600, krAvg: 25.0, pr: 19, prYards: 247, prAvg: 13.0, tds: 0 },
        { rank: 9, name: "Richie James", team: "KC", kr: 26, krYards: 650, krAvg: 25.0, pr: 17, prYards: 221, prAvg: 13.0, tds: 1 },
        { rank: 10, name: "Isaiah McKenzie", team: "IND", kr: 20, krYards: 500, krAvg: 25.0, pr: 23, prYards: 299, prAvg: 13.0, tds: 0 }
    ];
    
    const rows = returnersData.map(player => `
        <tr>
            <td>${player.rank}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.kr}</td>
            <td>${player.krYards}</td>
            <td>${player.krAvg}</td>
            <td>${player.pr}</td>
            <td>${player.prYards}</td>
            <td>${player.prAvg}</td>
            <td>${player.tds}</td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = rows;
}

// ==========================================
// Keyboard Navigation
// ==========================================

/**
 * Initialize keyboard navigation shortcuts
 */
function initializeKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        // Alt+H: Home
        if (e.altKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = 'index.html';
        }
        // Alt+S: Schedule
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            window.location.href = 'schedule.html';
        }
        // Alt+T: Standings
        if (e.altKey && e.key === 't') {
            e.preventDefault();
            window.location.href = 'standings.html';
        }
        // Alt+P: Player Stats
        if (e.altKey && e.key === 'p') {
            e.preventDefault();
            window.location.href = 'qb-leaders.html';
        }
        // Escape: Clear search/filters
        if (e.key === 'Escape') {
            const searchInputs = document.querySelectorAll('input[type="text"]');
            searchInputs.forEach(input => input.value = '');
            const selects = document.querySelectorAll('select');
            selects.forEach(select => select.selectedIndex = 0);
            
            // Trigger change events to reset filters
            searchInputs.forEach(input => input.dispatchEvent(new Event('input')));
            selects.forEach(select => select.dispatchEvent(new Event('change')));
        }
    });
}

// Populate league leaders summary page
async function populateLeagueLeaders() {
    // This function aggregates top performers from all categories
    // In a production environment, this would fetch real data from the API
    // For now, we'll use sample data from our existing datasets
    
    // Helper function to create leader list item
    function createLeaderItem(playerName, team, statValue) {
        return `
            <span class="player-name">${playerName}<span class="player-team">${team}</span></span>
            <span class="stat-value">${statValue}</span>
        `;
    }
    
    // Passing Yards Leaders (top 5 from QB data)
    const passingYardsLeaders = [
        { name: "Jared Goff", team: "DET", yards: 3541 },
        { name: "Joe Burrow", team: "CIN", yards: 3337 },
        { name: "Patrick Mahomes", team: "KC", yards: 3348 },
        { name: "Baker Mayfield", team: "TB", yards: 3290 },
        { name: "Josh Allen", team: "BUF", yards: 3033 }
    ];
    
    // Passing TDs Leaders
    const passingTdsLeaders = [
        { name: "Joe Burrow", team: "CIN", tds: 30 },
        { name: "Baker Mayfield", team: "TB", tds: 28 },
        { name: "Sam Darnold", team: "MIN", tds: 25 },
        { name: "Jared Goff", team: "DET", tds: 24 },
        { name: "Josh Allen", team: "BUF", tds: 23 }
    ];
    
    // Rushing Yards Leaders
    const rushingYardsLeaders = [
        { name: "Saquon Barkley", team: "PHI", yards: 1623 },
        { name: "Derrick Henry", team: "BAL", yards: 1474 },
        { name: "Josh Jacobs", team: "GB", yards: 1050 },
        { name: "Jahmyr Gibbs", team: "DET", yards: 1047 },
        { name: "De'Von Achane", team: "MIA", yards: 857 }
    ];
    
    // Rushing TDs Leaders
    const rushingTdsLeaders = [
        { name: "Saquon Barkley", team: "PHI", tds: 11 },
        { name: "Derrick Henry", team: "BAL", tds: 13 },
        { name: "Jahmyr Gibbs", team: "DET", tds: 13 },
        { name: "Josh Jacobs", team: "GB", tds: 9 },
        { name: "James Conner", team: "ARI", tds: 10 }
    ];
    
    // Receiving Yards Leaders
    const receivingYardsLeaders = [
        { name: "Ja'Marr Chase", team: "CIN", yards: 1319 },
        { name: "Justin Jefferson", team: "MIN", yards: 1079 },
        { name: "Zay Flowers", team: "BAL", yards: 1047 },
        { name: "CeeDee Lamb", team: "DAL", yards: 1005 },
        { name: "Terry McLaurin", team: "WAS", yards: 982 }
    ];
    
    // Receptions Leaders
    const receptionsLeaders = [
        { name: "Ja'Marr Chase", team: "CIN", rec: 93 },
        { name: "Amon-Ra St. Brown", team: "DET", rec: 84 },
        { name: "CeeDee Lamb", team: "DAL", rec: 82 },
        { name: "Justin Jefferson", team: "MIN", rec: 79 },
        { name: "Terry McLaurin", team: "WAS", rec: 68 }
    ];
    
    // Tackles Leaders
    const tacklesLeaders = [
        { name: "Bobby Okereke", team: "NYG", tackles: 148 },
        { name: "Zaire Franklin", team: "IND", tackles: 145 },
        { name: "Roquan Smith", team: "BAL", tackles: 138 },
        { name: "Foyesade Oluokun", team: "JAX", tackles: 135 },
        { name: "Demario Davis", team: "NO", tackles: 128 }
    ];
    
    // Sacks Leaders
    const sacksLeaders = [
        { name: "Trey Hendrickson", team: "CIN", sacks: 13.5 },
        { name: "Myles Garrett", team: "CLE", sacks: 12.0 },
        { name: "Josh Allen", team: "JAX", sacks: 10.5 },
        { name: "Dexter Lawrence", team: "NYG", sacks: 9.0 },
        { name: "Chris Jones", team: "KC", sacks: 9.0 }
    ];
    
    // Interceptions Leaders
    const interceptionsLeaders = [
        { name: "Kerby Joseph", team: "DET", ints: 8 },
        { name: "Xavier McKinney", team: "GB", ints: 8 },
        { name: "Brian Branch", team: "DET", ints: 6 },
        { name: "Derek Stingley Jr.", team: "HOU", ints: 6 },
        { name: "Patrick Surtain II", team: "DEN", ints: 5 }
    ];
    
    // Field Goals Leaders
    const fieldGoalsLeaders = [
        { name: "Justin Tucker", team: "BAL", fgm: 28 },
        { name: "Brandon Aubrey", team: "DAL", fgm: 27 },
        { name: "Jake Moody", team: "SF", fgm: 26 },
        { name: "Chris Boswell", team: "PIT", fgm: 25 },
        { name: "Younghoe Koo", team: "ATL", fgm: 24 }
    ];
    
    // Points Scored Leaders (kickers)
    const pointsLeaders = [
        { name: "Justin Tucker", team: "BAL", pts: 118 },
        { name: "Brandon Aubrey", team: "DAL", pts: 115 },
        { name: "Chris Boswell", team: "PIT", pts: 112 },
        { name: "Jake Moody", team: "SF", pts: 110 },
        { name: "Younghoe Koo", team: "ATL", pts: 108 }
    ];
    
    // Return TDs Leaders
    const returnTdsLeaders = [
        { name: "KaVontae Turpin", team: "DAL", tds: 2 },
        { name: "Brandon Aubrey", team: "DAL", tds: 2 },
        { name: "Marvin Mims", team: "DEN", tds: 2 },
        { name: "Jalen Reagor", team: "LAC", tds: 1 },
        { name: "Xavier Gipson", team: "NYJ", tds: 1 }
    ];
    
    // Populate all leader lists
    const populateList = (listId, leaders, statKey) => {
        const list = document.getElementById(listId);
        if (list) {
            list.innerHTML = leaders.map(leader => 
                `<li>${createLeaderItem(leader.name, leader.team, leader[statKey])}</li>`
            ).join('');
        }
    };
    
    populateList('passing-yards-leaders', passingYardsLeaders, 'yards');
    populateList('passing-tds-leaders', passingTdsLeaders, 'tds');
    populateList('rushing-yards-leaders', rushingYardsLeaders, 'yards');
    populateList('rushing-tds-leaders', rushingTdsLeaders, 'tds');
    populateList('receiving-yards-leaders', receivingYardsLeaders, 'yards');
    populateList('receptions-leaders', receptionsLeaders, 'rec');
    populateList('tackles-leaders', tacklesLeaders, 'tackles');
    populateList('sacks-leaders', sacksLeaders, 'sacks');
    populateList('interceptions-leaders', interceptionsLeaders, 'ints');
    populateList('field-goals-leaders', fieldGoalsLeaders, 'fgm');
    populateList('points-leaders', pointsLeaders, 'pts');
    populateList('return-tds-leaders', returnTdsLeaders, 'tds');
}

// Populate playoff picture page
async function populatePlayoffPicture() {
    try {
        // Fetch current standings data
        const standingsData = await fetchStandings();
        
        if (!standingsData) {
            console.error('Failed to fetch standings data for playoff picture');
            return;
        }
        
        // Reorganize standings data by conference
        // fetchStandings returns keys like 'afc-east', 'nfc-west', etc.
        const afcData = {
            East: standingsData['afc-east'] || [],
            North: standingsData['afc-north'] || [],
            South: standingsData['afc-south'] || [],
            West: standingsData['afc-west'] || []
        };
        
        const nfcData = {
            East: standingsData['nfc-east'] || [],
            North: standingsData['nfc-north'] || [],
            South: standingsData['nfc-south'] || [],
            West: standingsData['nfc-west'] || []
        };
        
        // Calculate playoff seeding for each conference
        const afcSeeds = calculatePlayoffSeeds(afcData);
        const nfcSeeds = calculatePlayoffSeeds(nfcData);
        
        // Populate AFC seeds
        populateConferenceSeeds('afc', afcSeeds);
        
        // Populate NFC seeds
        populateConferenceSeeds('nfc', nfcSeeds);
        
    } catch (error) {
        console.error('Error populating playoff picture:', error);
    }
}

// Calculate playoff seeds from standings data
function calculatePlayoffSeeds(conferenceData) {
    // Flatten all division teams into one array with division info
    const allTeams = [];
    
    for (const [divisionName, teams] of Object.entries(conferenceData)) {
        teams.forEach(team => {
            allTeams.push({
                ...team,
                division: divisionName
            });
        });
    }
    
    // Sort by wins (descending), then losses (ascending)
    allTeams.sort((a, b) => {
        if (b.wins !== a.wins) {
            return b.wins - a.wins;
        }
        return a.losses - b.losses;
    });
    
    // Get division winners (best team from each division)
    const divisions = ['East', 'North', 'South', 'West'];
    const divisionWinners = [];
    const wildCardCandidates = [];
    
    divisions.forEach(div => {
        const divisionTeams = allTeams.filter(t => t.division === div);
        if (divisionTeams.length > 0) {
            divisionWinners.push({
                ...divisionTeams[0],
                isDivisionWinner: true
            });
            // Rest are wild card candidates
            divisionTeams.slice(1).forEach(t => wildCardCandidates.push(t));
        }
    });
    
    // Sort division winners by record
    divisionWinners.sort((a, b) => {
        if (b.wins !== a.wins) {
            return b.wins - a.wins;
        }
        return a.losses - b.losses;
    });
    
    // Sort wild card candidates by record
    wildCardCandidates.sort((a, b) => {
        if (b.wins !== a.wins) {
            return b.wins - a.wins;
        }
        return a.losses - b.losses;
    });
    
    // Top 3 wild cards make playoffs
    const wildCards = wildCardCandidates.slice(0, 3).map(t => ({
        ...t,
        isWildCard: true
    }));
    
    // Seeds 1-4 are division winners, 5-7 are wild cards
    const playoffTeams = [...divisionWinners, ...wildCards];
    
    // In the hunt are next 3 teams
    const inTheHunt = wildCardCandidates.slice(3, 6);
    
    return {
        seeds: playoffTeams.slice(0, 7),
        inTheHunt: inTheHunt
    };
}

// Populate conference seeds in the UI
function populateConferenceSeeds(conference, seedsData) {
    const { seeds, inTheHunt } = seedsData;
    
    // Find all playoff seed elements for this conference
    const conferenceElement = document.querySelector(
        `.conference-playoff .${conference}-header`
    )?.closest('.conference-playoff');
    
    if (!conferenceElement) return;
    
    // Populate seeds 1-7
    seeds.forEach((team, index) => {
        const seedElement = conferenceElement.querySelector(
            `.playoff-seed[data-seed="${index + 1}"]`
        );
        
        if (seedElement) {
            const teamElement = seedElement.querySelector('.seed-team');
            
            if (teamElement) {
                teamElement.classList.remove('loading');
                
                let divisionBadge = '';
                if (team.isDivisionWinner) {
                    divisionBadge = `<span class="team-division">★ ${team.division} Champion</span>`;
                } else if (team.isWildCard) {
                    divisionBadge = `<span class="team-division">Wild Card</span>`;
                }
                
                teamElement.innerHTML = `
                    <span class="team-name">${team.team || team.name}</span>
                    <span class="team-record">${team.wins}-${team.losses}-${team.ties || 0}</span>
                    ${divisionBadge}
                `;
            }
        }
    });
    
    // Populate "In The Hunt" teams
    const huntContainer = conferenceElement.querySelector('.hunt-teams');
    if (huntContainer && inTheHunt.length > 0) {
        huntContainer.innerHTML = inTheHunt.map(team => `
            <div class="hunt-team">
                <span class="team-name">${team.team || team.name}</span>
                <span class="team-record">(${team.wins}-${team.losses}-${team.ties || 0})</span>
            </div>
        `).join('');
    } else if (huntContainer) {
        huntContainer.innerHTML = '<span style="color: #999;">No teams currently in the hunt</span>';
    }
}

/**
 * Load betting odds from JSON file
 * Data is pre-fetched by GitHub Actions and saved to data/odds.json
 */
async function loadBettingOdds() {
    const CACHE_KEY = 'nfl_betting_odds';
    const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes
    
    // Check localStorage cache first
    const cachedData = getFromCache(CACHE_KEY, CACHE_DURATION);
    if (cachedData) {
        console.log('Using cached betting odds data');
        return cachedData;
    }
    
    try {
        // Fetch from data/odds.json (pre-fetched by GitHub Actions)
        const response = await fetch('data/odds.json');
        
        if (!response.ok) {
            console.warn('Odds data not available');
            return null;
        }
        
        const data = await response.json();
        
        // Cache the data
        saveToCache(CACHE_KEY, data);
        
        console.log(`Loaded betting odds for ${data.length || 0} games`);
        return data;
    } catch (error) {
        console.warn('Could not load betting odds:', error.message);
        return null;
    }
}

/**
 * Find betting odds for a specific game
 * Matches game by team names
 */
function findOddsForGame(game, oddsData) {
    const defaultOdds = {
        spread: '<span class="odds-unavailable">N/A</span>',
        moneyline: '<span class="odds-unavailable">N/A</span>',
        total: '<span class="odds-unavailable">N/A</span>'
    };
    
    if (!oddsData || !Array.isArray(oddsData)) {
        return defaultOdds;
    }
    
    // Find matching game in odds data
    const matchingOdds = oddsData.find(odds => {
        // Match by team names (handle variations)
        const homeMatch = normalizeTeamName(odds.home_team) === normalizeTeamName(game.homeTeam);
        const awayMatch = normalizeTeamName(odds.away_team) === normalizeTeamName(game.awayTeam);
        return homeMatch && awayMatch;
    });
    
    if (!matchingOdds || !matchingOdds.bookmakers || matchingOdds.bookmakers.length === 0) {
        return defaultOdds;
    }
    
    // Use first available bookmaker's odds
    const bookmaker = matchingOdds.bookmakers[0];
    const markets = bookmaker.markets || [];
    
    // Extract spread, moneyline, and totals
    const spreadMarket = markets.find(m => m.key === 'spreads');
    const h2hMarket = markets.find(m => m.key === 'h2h');
    const totalsMarket = markets.find(m => m.key === 'totals');
    
    return {
        spread: formatSpreadOdds(spreadMarket, game.homeTeam, game.awayTeam),
        moneyline: formatMoneylineOdds(h2hMarket, game.homeTeam, game.awayTeam),
        total: formatTotalOdds(totalsMarket)
    };
}

/**
 * Normalize team name for matching
 * Removes city names, handles abbreviations
 */
function normalizeTeamName(name) {
    if (!name) return '';
    
    // Common team name mappings
    const nameMap = {
        'Los Angeles Rams': 'Rams',
        'Los Angeles Chargers': 'Chargers',
        'New York Giants': 'Giants',
        'New York Jets': 'Jets',
        'LA Rams': 'Rams',
        'LA Chargers': 'Chargers',
        'NY Giants': 'Giants',
        'NY Jets': 'Jets'
    };
    
    const mapped = nameMap[name];
    if (mapped) return mapped.toLowerCase();
    
    // Extract team name (last word typically)
    const parts = name.split(' ');
    return parts[parts.length - 1].toLowerCase();
}

/**
 * Format spread odds for display
 */
function formatSpreadOdds(market, homeTeam, awayTeam) {
    if (!market || !market.outcomes || market.outcomes.length < 2) {
        return '<span class="odds-unavailable">N/A</span>';
    }
    
    const homeOutcome = market.outcomes.find(o => 
        normalizeTeamName(o.name) === normalizeTeamName(homeTeam)
    );
    
    if (!homeOutcome) {
        return '<span class="odds-unavailable">N/A</span>';
    }
    
    const point = homeOutcome.point;
    const price = homeOutcome.price;
    
    const spreadValue = point > 0 ? `+${point}` : point;
    const priceValue = price > 0 ? `+${price}` : price;
    
    const favoriteClass = point < 0 ? 'favorite' : 'underdog';
    
    return `
        <span class="odds-label">📊 Spread</span>
        <span class="odds-value ${favoriteClass}">${spreadValue} (${priceValue})</span>
    `;
}

/**
 * Format moneyline odds for display
 */
function formatMoneylineOdds(market, homeTeam, awayTeam) {
    if (!market || !market.outcomes || market.outcomes.length < 2) {
        return '<span class="odds-unavailable">N/A</span>';
    }
    
    const homeOutcome = market.outcomes.find(o => 
        normalizeTeamName(o.name) === normalizeTeamName(homeTeam)
    );
    const awayOutcome = market.outcomes.find(o => 
        normalizeTeamName(o.name) === normalizeTeamName(awayTeam)
    );
    
    if (!homeOutcome || !awayOutcome) {
        return '<span class="odds-unavailable">N/A</span>';
    }
    
    const homePrice = homeOutcome.price > 0 ? `+${homeOutcome.price}` : homeOutcome.price;
    const awayPrice = awayOutcome.price > 0 ? `+${awayOutcome.price}` : awayOutcome.price;
    
    const homeClass = homeOutcome.price < 0 ? 'favorite' : 'underdog';
    const awayClass = awayOutcome.price < 0 ? 'favorite' : 'underdog';
    
    return `
        <span class="odds-label">💰 Moneyline</span>
        <span class="odds-value">
            <span class="${awayClass}">Away: ${awayPrice}</span><br>
            <span class="${homeClass}">Home: ${homePrice}</span>
        </span>
    `;
}

/**
 * Format total (over/under) odds for display
 */
function formatTotalOdds(market) {
    if (!market || !market.outcomes || market.outcomes.length < 2) {
        return '<span class="odds-unavailable">N/A</span>';
    }
    
    const overOutcome = market.outcomes.find(o => o.name === 'Over');
    const underOutcome = market.outcomes.find(o => o.name === 'Under');
    
    if (!overOutcome || !underOutcome) {
        return '<span class="odds-unavailable">N/A</span>';
    }
    
    const point = overOutcome.point;
    const overPrice = overOutcome.price > 0 ? `+${overOutcome.price}` : overOutcome.price;
    const underPrice = underOutcome.price > 0 ? `+${underOutcome.price}` : underOutcome.price;
    
    return `
        <span class="odds-label">🎯 Total</span>
        <span class="odds-value">
            O ${point} (${overPrice})<br>
            U ${point} (${underPrice})
        </span>
    `;
}

/**
 * Initialize odds toggle functionality
 */
function initializeOddsToggle() {
    const toggleBtn = document.getElementById('toggle-odds-btn');
    const disclaimer = document.getElementById('odds-disclaimer');
    const attribution = document.getElementById('odds-attribution');
    
    if (!toggleBtn) return;
    
    let oddsVisible = false;
    
    toggleBtn.addEventListener('click', () => {
        oddsVisible = !oddsVisible;
        
        // Toggle button state
        toggleBtn.classList.toggle('active', oddsVisible);
        toggleBtn.innerHTML = oddsVisible 
            ? '<span class="icon">📊</span> Hide Betting Odds'
            : '<span class="icon">📊</span> Show Betting Odds';
        
        // Toggle odds columns visibility
        const oddsColumns = document.querySelectorAll('.odds-column');
        oddsColumns.forEach(col => {
            col.style.display = oddsVisible ? 'table-cell' : 'none';
        });
        
        // Update week separator colspan
        const weekSeparators = document.querySelectorAll('.week-separator');
        weekSeparators.forEach(sep => {
            const td = sep.querySelector('td');
            if (td) {
                td.setAttribute('colspan', oddsVisible ? '10' : '7');
            }
        });
        
        // Toggle disclaimer and attribution
        if (disclaimer) {
            disclaimer.style.display = oddsVisible ? 'block' : 'none';
        }
        if (attribution) {
            attribution.style.display = oddsVisible ? 'block' : 'none';
        }
    });
}

