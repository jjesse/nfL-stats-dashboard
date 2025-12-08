/**
 * NFL Stats Dashboard - API Integration Module
 * 
 * This module handles all API calls to fetch NFL data from ESPN's public API.
 * ESPN API is used because it's free, reliable, and doesn't require authentication.
 * 
 * API Documentation (unofficial):
 * - Base URL: https://site.api.espn.com/apis/site/v2/sports/football/nfl/
 * - Endpoints: scoreboard, teams, standings, athletes, etc.
 */

// ==========================================
// Configuration
// ==========================================

const API_CONFIG = {
    baseUrl: 'https://site.api.espn.com/apis/site/v2/sports/football/nfl',
    corsProxy: '', // Add CORS proxy if needed: 'https://cors-anywhere.herokuapp.com/'
    timeout: 10000, // 10 seconds
    currentSeason: 2025,
    currentWeek: 14
};

// ==========================================
// Utility Functions
// ==========================================

/**
 * Make a fetch request with timeout and error handling
 * @param {string} url - The URL to fetch
 * @param {number} timeout - Timeout in milliseconds
 * @returns {Promise<any>} - Parsed JSON response
 */
async function fetchWithTimeout(url, timeout = API_CONFIG.timeout) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(API_CONFIG.corsProxy + url, {
            signal: controller.signal,
            headers: {
                'Accept': 'application/json'
            }
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout - please try again');
        }
        throw error;
    }
}

/**
 * Handle API errors gracefully
 * @param {Error} error - The error object
 * @param {string} context - Context description for the error
 */
function handleApiError(error, context) {
    console.error(`API Error (${context}):`, error);
    
    // Return user-friendly error message
    if (error.message.includes('timeout')) {
        return 'Request timed out. Please check your connection and try again.';
    } else if (error.message.includes('HTTP error')) {
        return 'Unable to fetch data from the server. Please try again later.';
    } else if (error.message.includes('Failed to fetch')) {
        return 'Network error. Please check your internet connection.';
    } else {
        return 'An unexpected error occurred. Please try again.';
    }
}

// ==========================================
// Schedule API Functions
// ==========================================

/**
 * Fetch NFL schedule/scoreboard data
 * @param {number} week - Week number (optional, defaults to current week)
 * @param {number} year - Season year (optional, defaults to current season)
 * @returns {Promise<Array>} - Array of game objects
 */
async function fetchSchedule(week = API_CONFIG.currentWeek, year = API_CONFIG.currentSeason) {
    try {
        const url = `${API_CONFIG.baseUrl}/scoreboard?seasontype=2&week=${week}`;
        console.log('Fetching schedule from:', url);
        const data = await fetchWithTimeout(url);
        
        if (!data.events || data.events.length === 0) {
            console.warn('No games found for this week');
            return [];
        }
        
        return data.events.map(event => {
            const competition = event.competitions[0];
            const homeTeam = competition.competitors.find(team => team.homeAway === 'home');
            const awayTeam = competition.competitors.find(team => team.homeAway === 'away');
            
            return {
                date: event.date,
                time: new Date(event.date).toLocaleTimeString('en-US', { 
                    hour: 'numeric', 
                    minute: '2-digit',
                    timeZoneName: 'short'
                }),
                awayTeam: awayTeam.team.displayName,
                awayRecord: awayTeam.records?.[0]?.summary || 'N/A',
                homeTeam: homeTeam.team.displayName,
                homeRecord: homeTeam.records?.[0]?.summary || 'N/A',
                venue: competition.venue.fullName,
                status: competition.status.type.description,
                awayScore: awayTeam.score || '0',
                homeScore: homeTeam.score || '0'
            };
        });
    } catch (error) {
        throw new Error(handleApiError(error, 'fetchSchedule'));
    }
}

// ==========================================
// Team Stats API Functions
// ==========================================

/**
 * Fetch NFL team standings/statistics
 * Uses team IDs to get individual team records
 * @returns {Promise<Array>} - Array of team stat objects
 */
async function fetchTeamStats() {
    try {
        // ESPN team IDs (all 32 NFL teams)
        const teamIds = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
            17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 34
        ];
        
        console.log('Fetching team stats for', teamIds.length, 'teams');
        
        // Fetch all teams in parallel for better performance
        const teamPromises = teamIds.map(async (teamId) => {
            try {
                const url = `${API_CONFIG.baseUrl}/teams/${teamId}`;
                const teamData = await fetchWithTimeout(url);
                const team = teamData.team;
                
                // Get record from team data
                const record = team.record?.items?.[0] || {};
                const stats = record.stats || [];
                
                // Helper to find stat by name
                const getStat = (name) => {
                    const stat = stats.find(s => s.name === name);
                    return stat ? stat.value : 0;
                };
                
                const wins = getStat('wins') || 0;
                const losses = getStat('losses') || 0;
                const ties = getStat('ties') || 0;
                const total = wins + losses + ties;
                const winPct = total > 0 ? (wins / total).toFixed(3) : '.000';
                
                return {
                    rank: 0, // Will be set after sorting
                    team: team.displayName,
                    wins,
                    losses,
                    ties,
                    winPct,
                    pointsScored: getStat('pointsFor') || 0,
                    pointsAllowed: getStat('pointsAgainst') || 0,
                    differential: getStat('pointDifferential') || 0
                };
            } catch (error) {
                console.error(`Error fetching team ${teamId}:`, error.message);
                return null;
            }
        });
        
        // Wait for all teams to be fetched
        const allTeamsResults = await Promise.all(teamPromises);
        
        // Filter out any null results from errors
        const allTeams = allTeamsResults.filter(team => team !== null);
        
        // Sort by win percentage
        allTeams.sort((a, b) => parseFloat(b.winPct) - parseFloat(a.winPct));
        
        // Assign ranks
        allTeams.forEach((team, index) => {
            team.rank = index + 1;
        });
        
        console.log(`Fetched ${allTeams.length} teams successfully`);
        return allTeams;
    } catch (error) {
        throw new Error(handleApiError(error, 'fetchTeamStats'));
    }
}

/**
 * Fetch NFL standings organized by division
 * @returns {Promise<Object>} - Object with divisions as keys
 */
async function fetchStandings() {
    try {
        // Division mappings based on ESPN group IDs
        const divisions = {
            'afc-east': { name: 'AFC East', groupId: '1', teams: [17, 21, 22, 2] }, // BUF, NE, NYJ, MIA
            'afc-north': { name: 'AFC North', groupId: '2', teams: [3, 5, 23, 4] }, // BAL, CIN, PIT, CLE
            'afc-south': { name: 'AFC South', groupId: '3', teams: [11, 34, 10, 30] }, // HOU, JAX, IND, TEN
            'afc-west': { name: 'AFC West', groupId: '4', teams: [12, 7, 13, 25] }, // KC, DEN, LV, LAC
            'nfc-east': { name: 'NFC East', groupId: '5', teams: [6, 19, 28, 27] }, // DAL, PHI, WAS, NYG
            'nfc-north': { name: 'NFC North', groupId: '6', teams: [8, 14, 9, 16] }, // DET, GB, MIN, CHI
            'nfc-south': { name: 'NFC South', groupId: '7', teams: [1, 18, 29, 15] }, // ATL, NO, CAR, TB
            'nfc-west': { name: 'NFC West', groupId: '8', teams: [26, 24, 20, 33] }  // SEA, ARI, LAR, SF
        };

        const standings = {};
        
        // Fetch all teams data (reuse existing function)
        const allTeamsData = await fetchTeamStats();
        
        // Organize teams by division
        for (const [divisionKey, divisionInfo] of Object.entries(divisions)) {
            const divisionTeams = allTeamsData
                .filter(team => {
                    // Match teams to division by checking if team name contains division team names
                    return divisionInfo.teams.some(teamId => {
                        // This is a simple approach; we'll match by checking the teams we fetched
                        return true; // We'll filter properly below
                    });
                })
                .map(team => ({
                    ...team,
                    divisionName: divisionInfo.name
                }));
            
            standings[divisionKey] = divisionTeams;
        }
        
        // Better approach: organize by matching team data
        // Clear and rebuild with proper matching
        const teamsByDivision = {};
        
        for (const [divisionKey, divisionInfo] of Object.entries(divisions)) {
            teamsByDivision[divisionKey] = [];
            
            for (const teamId of divisionInfo.teams) {
                try {
                    const url = `${API_CONFIG.baseUrl}/teams/${teamId}`;
                    const teamData = await fetchWithTimeout(url);
                    const team = teamData.team || teamData;
                    
                    const record = team.record?.items?.[0] || {};
                    const stats = record.stats || [];
                    
                    const getStat = (name) => {
                        const stat = stats.find(s => s.name === name);
                        return stat ? stat.value : 0;
                    };
                    
                    const wins = getStat('wins') || 0;
                    const losses = getStat('losses') || 0;
                    const ties = getStat('ties') || 0;
                    const total = wins + losses + ties;
                    const winPct = total > 0 ? (wins / total).toFixed(3) : '.000';
                    const streak = getStat('streak') || 0;
                    
                    teamsByDivision[divisionKey].push({
                        team: team.displayName,
                        abbreviation: team.abbreviation,
                        wins,
                        losses,
                        ties,
                        winPct,
                        pointsScored: getStat('pointsFor') || 0,
                        pointsAllowed: getStat('pointsAgainst') || 0,
                        differential: getStat('pointDifferential') || 0,
                        streak: streak > 0 ? `W${Math.abs(streak)}` : streak < 0 ? `L${Math.abs(streak)}` : '-'
                    });
                } catch (error) {
                    console.error(`Error fetching team ${teamId}:`, error.message);
                }
            }
            
            // Sort by win percentage within division
            teamsByDivision[divisionKey].sort((a, b) => parseFloat(b.winPct) - parseFloat(a.winPct));
        }
        
        console.log('Fetched standings for all divisions');
        return teamsByDivision;
    } catch (error) {
        throw new Error(handleApiError(error, 'fetchStandings'));
    }
}

// ==========================================
// Player Stats API Functions
// ==========================================

/**
 * Fetch quarterback statistics using ESPN Core API
 * @returns {Promise<Array>} - Array of QB stat objects
 */
async function fetchQBStats() {
    try {
        const url = `https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/${API_CONFIG.currentSeason}/types/2/leaders?limit=10`;
        console.log('Fetching QB stats from:', url);
        const data = await fetchWithTimeout(url);
        
        if (!data.categories) {
            throw new Error('No QB stats available');
        }
        
        // Find passing yards category
        const passingCategory = data.categories.find(cat => 
            cat.name === 'passingYards' || cat.displayName === 'Passing Yards'
        );
        
        if (!passingCategory || !passingCategory.leaders) {
            throw new Error('No QB stats available');
        }
        
        // Fetch all QB data in parallel
        const qbPromises = passingCategory.leaders.slice(0, 10).map(async (leader, index) => {
            try {
                // Fetch athlete, team, and statistics data in parallel
                const [athleteData, teamData, statsData] = await Promise.all([
                    fetchWithTimeout(leader.athlete.$ref),
                    leader.team?.$ref ? fetchWithTimeout(leader.team.$ref) : Promise.resolve(null),
                    leader.statistics?.$ref ? fetchWithTimeout(leader.statistics.$ref) : Promise.resolve(null)
                ]);
                
                const athlete = athleteData;
                const teamAbbr = teamData?.abbreviation || 'N/A';
                
                // Extract passing stats
                let games = 0, completions = 0, attempts = 0, compPct = 0, tds = 0, ints = 0, rating = 0;
                
                if (statsData && statsData.splits && statsData.splits.categories) {
                    const passingStats = statsData.splits.categories.find(cat => cat.name === 'passing');
                    if (passingStats && passingStats.stats) {
                        const getStat = (name) => {
                            const stat = passingStats.stats.find(s => s.name === name);
                            return stat ? stat.value : 0;
                        };
                        
                        games = getStat('gamesPlayed') || getStat('teamGamesPlayed') || 0;
                        completions = getStat('completions') || 0;
                        attempts = getStat('passingAttempts') || 0;
                        compPct = getStat('completionPct') || 0;
                        tds = getStat('passingTouchdowns') || 0;
                        ints = getStat('interceptions') || 0;
                        rating = getStat('quarterbackRating') || getStat('QBRating') || 0;
                    }
                }
                
                return {
                    rank: index + 1,
                    name: athlete.displayName || athlete.fullName || 'Unknown',
                    team: teamAbbr,
                    games: Math.round(games),
                    completions: Math.round(completions),
                    attempts: Math.round(attempts),
                    compPct: compPct.toFixed(1) + '%',
                    yards: Math.round(leader.value || 0),
                    tds: Math.round(tds),
                    ints: Math.round(ints),
                    rating: rating.toFixed(1)
                };
            } catch (error) {
                console.error(`Error fetching QB ${index + 1} details:`, error.message);
                return null;
            }
        });
        
        // Wait for all QBs to be fetched
        const qbResults = await Promise.all(qbPromises);
        const qbStats = qbResults.filter(qb => qb !== null);
        
        console.log(`Fetched ${qbStats.length} QB stats`);
        return qbStats;
    } catch (error) {
        throw new Error(handleApiError(error, 'fetchQBStats'));
    }
}

/**
 * Fetch receiving statistics using ESPN Core API
 * @returns {Promise<Array>} - Array of receiver stat objects
 */
async function fetchReceiverStats() {
    try {
        const url = `https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/${API_CONFIG.currentSeason}/types/2/leaders?limit=10`;
        console.log('Fetching receiver stats from:', url);
        const data = await fetchWithTimeout(url);
        
        if (!data.categories) {
            throw new Error('No receiver stats available');
        }
        
        // Find receiving yards category
        const receivingCategory = data.categories.find(cat => 
            cat.name === 'receivingYards' || cat.displayName === 'Receiving Yards'
        );
        
        if (!receivingCategory || !receivingCategory.leaders) {
            throw new Error('No receiver stats available');
        }
        
        // Fetch all receiver data in parallel
        const receiverPromises = receivingCategory.leaders.slice(0, 10).map(async (leader, index) => {
            try {
                // Fetch athlete, team, and statistics data in parallel
                const [athleteData, teamData, statsData] = await Promise.all([
                    fetchWithTimeout(leader.athlete.$ref),
                    leader.team?.$ref ? fetchWithTimeout(leader.team.$ref) : Promise.resolve(null),
                    leader.statistics?.$ref ? fetchWithTimeout(leader.statistics.$ref) : Promise.resolve(null)
                ]);
                
                const athlete = athleteData;
                const teamAbbr = teamData?.abbreviation || 'N/A';
                
                // Extract receiving stats
                let games = 0, receptions = 0, targets = 0, tds = 0, longRec = 0, avg = 0, ypg = 0;
                
                if (statsData && statsData.splits && statsData.splits.categories) {
                    const receivingStats = statsData.splits.categories.find(cat => cat.name === 'receiving');
                    if (receivingStats && receivingStats.stats) {
                        const getStat = (name) => {
                            const stat = receivingStats.stats.find(s => s.name === name);
                            return stat ? stat.value : 0;
                        };
                        
                        games = getStat('gamesPlayed') || getStat('teamGamesPlayed') || 0;
                        receptions = getStat('receptions') || 0;
                        targets = getStat('receivingTargets') || 0;
                        tds = getStat('receivingTouchdowns') || 0;
                        longRec = getStat('longReception') || 0;
                        avg = getStat('yardsPerReception') || 0;
                        ypg = getStat('receivingYardsPerGame') || 0;
                    }
                }
                
                return {
                    rank: index + 1,
                    name: athlete.displayName || athlete.fullName || 'Unknown',
                    team: teamAbbr,
                    games: Math.round(games),
                    receptions: Math.round(receptions),
                    targets: Math.round(targets),
                    yards: Math.round(leader.value || 0),
                    avg: avg.toFixed(1),
                    tds: Math.round(tds),
                    long: Math.round(longRec),
                    ypg: ypg.toFixed(1)
                };
            } catch (error) {
                console.error(`Error fetching receiver ${index + 1} details:`, error.message);
                return null;
            }
        });
        
        // Wait for all receivers to be fetched
        const receiverResults = await Promise.all(receiverPromises);
        const receiverStats = receiverResults.filter(receiver => receiver !== null);
        
        console.log(`Fetched ${receiverStats.length} receiver stats`);
        return receiverStats;
    } catch (error) {
        throw new Error(handleApiError(error, 'fetchReceiverStats'));
    }
}

/**
 * Fetch rushing statistics using ESPN Core API
 * @returns {Promise<Array>} - Array of rusher stat objects
 */
async function fetchRushingStats() {
    try {
        const url = `https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/${API_CONFIG.currentSeason}/types/2/leaders?limit=10`;
        console.log('Fetching rushing stats from:', url);
        const data = await fetchWithTimeout(url);
        
        if (!data.categories) {
            throw new Error('No rushing stats available');
        }
        
        // Find rushing yards category
        const rushingCategory = data.categories.find(cat => 
            cat.name === 'rushingYards' || cat.displayName === 'Rushing Yards'
        );
        
        if (!rushingCategory || !rushingCategory.leaders) {
            throw new Error('No rushing stats available');
        }
        
        // Fetch all rusher data in parallel
        const rusherPromises = rushingCategory.leaders.slice(0, 10).map(async (leader, index) => {
            try {
                // Fetch athlete, team, and statistics data in parallel
                const [athleteData, teamData, statsData] = await Promise.all([
                    fetchWithTimeout(leader.athlete.$ref),
                    leader.team?.$ref ? fetchWithTimeout(leader.team.$ref) : Promise.resolve(null),
                    leader.statistics?.$ref ? fetchWithTimeout(leader.statistics.$ref) : Promise.resolve(null)
                ]);
                
                const athlete = athleteData;
                const teamAbbr = teamData?.abbreviation || 'N/A';
                
                // Extract rushing stats
                let games = 0, attempts = 0, tds = 0, longRush = 0, avg = 0, ypg = 0, fumbles = 0;
                
                if (statsData && statsData.splits && statsData.splits.categories) {
                    const rushingStats = statsData.splits.categories.find(cat => cat.name === 'rushing');
                    if (rushingStats && rushingStats.stats) {
                        const getStat = (name) => {
                            const stat = rushingStats.stats.find(s => s.name === name);
                            return stat ? stat.value : 0;
                        };
                        
                        games = getStat('gamesPlayed') || getStat('teamGamesPlayed') || 0;
                        attempts = getStat('rushingAttempts') || 0;
                        tds = getStat('rushingTouchdowns') || 0;
                        longRush = getStat('longRushing') || 0;
                        avg = getStat('yardsPerRushAttempt') || 0;
                        ypg = getStat('rushingYardsPerGame') || 0;
                        fumbles = getStat('rushingFumbles') || 0;
                    }
                }
                
                return {
                    rank: index + 1,
                    name: athlete.displayName || athlete.fullName || 'Unknown',
                    team: teamAbbr,
                    games: Math.round(games),
                    attempts: Math.round(attempts),
                    yards: Math.round(leader.value || 0),
                    avg: avg.toFixed(1),
                    tds: Math.round(tds),
                    long: Math.round(longRush),
                    ypg: ypg.toFixed(1),
                    fumbles: Math.round(fumbles)
                };
            } catch (error) {
                console.error(`Error fetching rusher ${index + 1} details:`, error.message);
                return null;
            }
        });
        
        // Wait for all rushers to be fetched
        const rusherResults = await Promise.all(rusherPromises);
        const rushingStats = rusherResults.filter(rusher => rusher !== null);
        
        console.log(`Fetched ${rushingStats.length} rushing stats`);
        return rushingStats;
    } catch (error) {
        throw new Error(handleApiError(error, 'fetchRushingStats'));
    }
}

// ==========================================
// Cache Management
// ==========================================

const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes in milliseconds

/**
 * Get cached data if available and not expired
 * @param {string} key - Cache key
 * @returns {any|null} - Cached data or null
 */
function getCachedData(key) {
    try {
        const cached = localStorage.getItem(key);
        if (!cached) return null;
        
        const { data, timestamp } = JSON.parse(cached);
        const now = Date.now();
        
        if (now - timestamp > CACHE_DURATION) {
            localStorage.removeItem(key);
            return null;
        }
        
        return data;
    } catch (error) {
        console.error('Cache retrieval error:', error);
        return null;
    }
}

/**
 * Store data in cache
 * @param {string} key - Cache key
 * @param {any} data - Data to cache
 */
function setCachedData(key, data) {
    try {
        const cacheObject = {
            data: data,
            timestamp: Date.now()
        };
        localStorage.setItem(key, JSON.stringify(cacheObject));
    } catch (error) {
        console.error('Cache storage error:', error);
    }
}

/**
 * Fetch data with caching
 * @param {string} cacheKey - Key for caching
 * @param {Function} fetchFunction - Function to fetch fresh data
 * @returns {Promise<any>} - Cached or fresh data
 */
async function fetchWithCache(cacheKey, fetchFunction) {
    // Try to get cached data first
    const cachedData = getCachedData(cacheKey);
    if (cachedData) {
        console.log(`Using cached data for ${cacheKey}`);
        return cachedData;
    }
    
    // Fetch fresh data
    console.log(`Fetching fresh data for ${cacheKey}`);
    const freshData = await fetchFunction();
    
    // Cache the fresh data
    setCachedData(cacheKey, freshData);
    
    return freshData;
}

// ==========================================
// Public API with Caching
// ==========================================

/**
 * Public API object with caching wrapper
 */
const NFLAPI = {
    /**
     * Get schedule data (with caching)
     */
    async getSchedule(week = API_CONFIG.currentWeek, year = API_CONFIG.currentSeason) {
        return await fetchWithCache(
            `schedule_${week}_${year}`,
            () => fetchSchedule(week, year)
        );
    },
    
    /**
     * Get team statistics (with caching)
     */
    async getTeamStats() {
        return await fetchWithCache(
            'team_stats',
            fetchTeamStats
        );
    },
    
    /**
     * Get QB statistics (with caching)
     */
    async getQBStats() {
        return await fetchWithCache(
            'qb_stats',
            fetchQBStats
        );
    },
    
    /**
     * Get receiver statistics (with caching)
     */
    async getReceiverStats() {
        return await fetchWithCache(
            'receiver_stats',
            fetchReceiverStats
        );
    },
    
    /**
     * Get rushing statistics (with caching)
     */
    async getRushingStats() {
        return await fetchWithCache(
            'rushing_stats',
            fetchRushingStats
        );
    },
    
    /**
     * Clear all cached data
     */
    clearCache() {
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
            if (key.includes('schedule') || key.includes('stats')) {
                localStorage.removeItem(key);
            }
        });
        console.log('Cache cleared');
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NFLAPI;
}
