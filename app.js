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
    tbody.innerHTML = '<tr><td colspan="7" class="loading">Loading schedule data...</td></tr>';

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
            tbody.innerHTML = '<tr><td colspan="7" class="loading">No games scheduled.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        
        let lastWeek = null;
        allGames.forEach(game => {
            // Add week separator row
            if (game.week !== lastWeek) {
                const weekRow = tbody.insertRow();
                weekRow.className = 'week-separator';
                weekRow.innerHTML = `<td colspan="7" style="background-color: var(--primary-color); color: white; font-weight: bold; padding: 0.75rem; text-align: center;">Week ${game.week}</td>`;
                lastWeek = game.week;
            }
            
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${formatDate(game.date)}</td>
                <td>${game.time}</td>
                <td>${game.awayTeam}</td>
                <td>${game.awayRecord}</td>
                <td>${game.homeTeam}</td>
                <td>${game.homeRecord}</td>
                <td>${game.venue}</td>
            `;
        });
        
        console.log(`Loaded ${allGames.length} games from weeks ${currentWeek}-${finalWeek}`);
    } catch (error) {
        console.error('Error loading schedule:', error);
        tbody.innerHTML = '<tr><td colspan="7" class="loading" style="color: #D50A0A;">Error loading schedule. Please refresh the page to try again.</td></tr>';
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
