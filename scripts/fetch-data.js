#!/usr/bin/env node

/**
 * NFL Stats Data Fetcher
 * 
 * This script fetches NFL statistics from ESPN's public API and saves them
 * as JSON files for GitHub Actions automation.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Disable SSL verification for systems with certificate issues
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const API_CONFIG = {
    baseUrl: 'https://site.api.espn.com/apis/site/v2/sports/football/nfl',
    coreUrl: 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl',
    timeout: 10000
};

/**
 * Make an HTTPS GET request
 */
function fetchUrl(url) {
    return new Promise((resolve, reject) => {
        const req = https.get(url, { timeout: API_CONFIG.timeout }, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        reject(new Error(`Failed to parse JSON from ${url}: ${e.message}`));
                    }
                } else {
                    reject(new Error(`HTTP ${res.statusCode} from ${url}`));
                }
            });
        });
        
        req.on('error', (err) => {
            reject(new Error(`Request failed for ${url}: ${err.message}`));
        });
        
        req.on('timeout', () => {
            req.destroy();
            reject(new Error(`Request timeout for ${url}`));
        });
    });
}

/**
 * Fetch schedule for weeks 14-18
 */
async function fetchSchedule() {
    console.log('Fetching schedule data...');
    const year = 2024;
    const weeks = [14, 15, 16, 17, 18];
    const allGames = [];
    
    for (const week of weeks) {
        try {
            const url = `${API_CONFIG.baseUrl}/scoreboard?dates=${year}&seasontype=2&week=${week}`;
            const data = await fetchUrl(url);
            
            if (data.events) {
                allGames.push(...data.events);
            }
            
            console.log(`  ✓ Week ${week}: ${data.events?.length || 0} games`);
        } catch (error) {
            console.error(`  ✗ Week ${week}: ${error.message}`);
        }
    }
    
    console.log(`Total games fetched: ${allGames.length}`);
    return allGames;
}

/**
 * Fetch team standings data
 */
async function fetchStandings() {
    console.log('Fetching standings data...');
    
    const divisions = {
        'afc-east': { name: 'AFC East', teams: [17, 21, 22, 2] },
        'afc-north': { name: 'AFC North', teams: [3, 5, 23, 4] },
        'afc-south': { name: 'AFC South', teams: [11, 34, 10, 30] },
        'afc-west': { name: 'AFC West', teams: [12, 7, 13, 25] },
        'nfc-east': { name: 'NFC East', teams: [6, 19, 28, 27] },
        'nfc-north': { name: 'NFC North', teams: [8, 14, 9, 16] },
        'nfc-south': { name: 'NFC South', teams: [1, 18, 29, 15] },
        'nfc-west': { name: 'NFC West', teams: [26, 24, 20, 33] }
    };
    
    const standings = {};
    
    for (const [divisionKey, divisionInfo] of Object.entries(divisions)) {
        standings[divisionKey] = [];
        
        for (const teamId of divisionInfo.teams) {
            try {
                const url = `${API_CONFIG.baseUrl}/teams/${teamId}`;
                const teamData = await fetchUrl(url);
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
                
                standings[divisionKey].push({
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
                console.error(`  ✗ Team ${teamId}: ${error.message}`);
            }
        }
        
        // Sort by win percentage
        standings[divisionKey].sort((a, b) => parseFloat(b.winPct) - parseFloat(a.winPct));
        console.log(`  ✓ ${divisionInfo.name}: ${standings[divisionKey].length} teams`);
    }
    
    return standings;
}

/**
 * Fetch team stats
 */
async function fetchTeamStats() {
    console.log('Fetching team stats...');
    
    try {
        const url = `${API_CONFIG.baseUrl}/standings`;
        const data = await fetchUrl(url);
        
        const allTeams = [];
        
        if (data.children) {
            for (const conference of data.children) {
                if (conference.standings?.entries) {
                    for (const entry of conference.standings.entries) {
                        const team = entry.team;
                        const stats = entry.stats || [];
                        
                        const getStat = (name) => {
                            const stat = stats.find(s => s.name === name);
                            return stat ? stat.value : 0;
                        };
                        
                        allTeams.push({
                            team: team.displayName,
                            abbreviation: team.abbreviation,
                            wins: getStat('wins'),
                            losses: getStat('losses'),
                            ties: getStat('ties'),
                            winPct: getStat('winPercent').toFixed(3),
                            pointsScored: getStat('pointsFor'),
                            pointsAllowed: getStat('pointsAgainst'),
                            differential: getStat('pointDifferential')
                        });
                    }
                }
            }
        }
        
        console.log(`  ✓ Fetched ${allTeams.length} teams`);
        return allTeams;
    } catch (error) {
        console.error(`  ✗ ${error.message}`);
        return [];
    }
}

/**
 * Fetch player stats (QB, Receivers, Rushers)
 */
async function fetchPlayerStats() {
    console.log('Fetching player stats...');
    
    const categories = [
        { key: 'qb', name: 'passingyards', label: 'QB Leaders' },
        { key: 'receivers', name: 'receivingyards', label: 'Receiver Leaders' },
        { key: 'rushers', name: 'rushingyards', label: 'Rushing Leaders' }
    ];
    
    const playerStats = {};
    
    for (const category of categories) {
        try {
            const url = `${API_CONFIG.coreUrl}/seasons/2024/types/2/leaders?limit=10`;
            const data = await fetchUrl(url);
            
            let leaders = [];
            
            if (data.categories) {
                const categoryData = data.categories.find(c => c.name === category.name);
                if (categoryData?.leaders) {
                    leaders = categoryData.leaders;
                }
            }
            
            const players = [];
            
            for (const leader of leaders) {
                if (!leader.athlete?.$ref) continue;
                
                try {
                    const athleteData = await fetchUrl(leader.athlete.$ref);
                    const athlete = athleteData;
                    
                    let teamAbbr = 'N/A';
                    if (athlete.team?.$ref) {
                        const teamData = await fetchUrl(athlete.team.$ref);
                        teamAbbr = teamData.abbreviation || 'N/A';
                    }
                    
                    players.push({
                        name: athlete.displayName || leader.displayName,
                        team: teamAbbr,
                        value: leader.value,
                        displayValue: leader.displayValue
                    });
                } catch (error) {
                    console.error(`    ✗ Athlete error: ${error.message}`);
                }
            }
            
            playerStats[category.key] = players;
            console.log(`  ✓ ${category.label}: ${players.length} players`);
        } catch (error) {
            console.error(`  ✗ ${category.label}: ${error.message}`);
            playerStats[category.key] = [];
        }
    }
    
    return playerStats;
}

/**
 * Save data to JSON file
 */
function saveToFile(filename, data) {
    const dataDir = path.join(__dirname, '..', 'data');
    
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
    }
    
    const filepath = path.join(dataDir, filename);
    fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
    console.log(`✓ Saved to ${filename}`);
}

/**
 * Main execution
 */
async function main() {
    console.log('='.repeat(50));
    console.log('NFL Stats Data Fetcher');
    console.log(`Started: ${new Date().toISOString()}`);
    console.log('='.repeat(50));
    console.log();
    
    try {
        // Fetch all data
        const schedule = await fetchSchedule();
        console.log();
        
        const standings = await fetchStandings();
        console.log();
        
        const teamStats = await fetchTeamStats();
        console.log();
        
        const playerStats = await fetchPlayerStats();
        console.log();
        
        // Save to files
        console.log('Saving data files...');
        saveToFile('schedule.json', schedule);
        saveToFile('standings.json', standings);
        saveToFile('team-stats.json', teamStats);
        saveToFile('player-stats.json', playerStats);
        
        // Save metadata
        const metadata = {
            lastUpdated: new Date().toISOString(),
            recordCount: {
                schedule: schedule.length,
                standings: Object.keys(standings).length,
                teamStats: teamStats.length,
                playerStats: {
                    qb: playerStats.qb?.length || 0,
                    receivers: playerStats.receivers?.length || 0,
                    rushers: playerStats.rushers?.length || 0
                }
            }
        };
        saveToFile('metadata.json', metadata);
        
        console.log();
        console.log('='.repeat(50));
        console.log('✓ Data fetch completed successfully');
        console.log('='.repeat(50));
        
    } catch (error) {
        console.error();
        console.error('='.repeat(50));
        console.error('✗ Error:', error.message);
        console.error('='.repeat(50));
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { main, fetchSchedule, fetchStandings, fetchTeamStats, fetchPlayerStats };
