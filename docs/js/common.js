/**
 * Common JavaScript Utilities for NFL Stats Dashboard
 * Shared functions used across multiple HTML pages to avoid duplication
 */

(function(window) {
    'use strict';

    // Create a namespace for common utilities
    const NFLCommon = {
        /**
         * Load and display the last updated timestamp for a specific data file
         * @param {string} filename - The timestamp file to load (e.g., 'last_updated_passing.txt')
         * @param {string} elementId - The DOM element ID to update with the timestamp
         */
        loadLastUpdated: function(filename, elementId) {
            elementId = elementId || 'last-update';
            
            fetch(filename)
                .then(response => response.text())
                .then(data => {
                    const element = document.getElementById(elementId);
                    if (element) {
                        element.textContent = data;
                    }
                })
                .catch(error => {
                    const element = document.getElementById(elementId);
                    if (element) {
                        element.textContent = 'No data available yet';
                    }
                });
        },

        /**
         * Load and display last updated timestamp from multiple files (for index.html)
         * Shows the most recent timestamp from the provided list of files
         * @param {Array<string>} timestampFiles - Array of timestamp file names
         * @param {string} elementId - The DOM element ID to update with the timestamp
         */
        loadLastUpdatedMultiple: function(timestampFiles, elementId) {
            elementId = elementId || 'last-update';
            
            Promise.all(timestampFiles.map(file => 
                fetch(file).then(r => r.text()).catch(() => 'Not available')
            )).then(timestamps => {
                const latest = timestamps.filter(t => t !== 'Not available').sort().pop() || 'No data available';
                const element = document.getElementById(elementId);
                if (element) {
                    element.textContent = latest;
                }
            });
        },

        /**
         * Find the player/team with the highest value for a specific stat
         * @param {Array<Object>} data - Array of player/team objects
         * @param {string} statColumn - The column/property name to compare
         * @returns {Object} The player/team with the highest value
         */
        findLeader: function(data, statColumn) {
            if (!data || data.length === 0) {
                return {};
            }
            return data.reduce((leader, item) => {
                const value = parseFloat(item[statColumn]) || 0;
                const leaderValue = parseFloat(leader[statColumn]) || 0;
                return value > leaderValue ? item : leader;
            }, data[0] || {});
        },

        /**
         * Find the player/team with the lowest value for a specific stat (e.g., interceptions)
         * @param {Array<Object>} data - Array of player/team objects
         * @param {string} statColumn - The column/property name to compare
         * @returns {Object} The player/team with the lowest value
         */
        findLowest: function(data, statColumn) {
            if (!data || data.length === 0) {
                return {};
            }
            return data.reduce((lowest, item) => {
                const value = parseFloat(item[statColumn]);
                const lowestValue = parseFloat(lowest[statColumn]);
                
                // Handle cases where stat might be missing
                if (isNaN(value)) return lowest;
                if (isNaN(lowestValue)) return item;
                
                return value < lowestValue ? item : lowest;
            }, data[0] || {});
        },

        /**
         * Parse CSV data and convert it to an array of objects
         * @param {string} csvText - The CSV text content
         * @returns {Object} Object containing headers array and data array
         */
        parseCSV: function(csvText) {
            const lines = csvText.trim().split('\n');
            if (lines.length === 0) {
                return { headers: [], data: [] };
            }

            const headers = lines[0].split(',').map(h => h.trim());
            const dataLines = lines.slice(1).filter(line => line.trim());
            
            const data = dataLines.map(line => {
                const values = line.split(',');
                return headers.reduce((obj, header, index) => {
                    obj[header] = values[index] ? values[index].trim() : '';
                    return obj;
                }, {});
            });

            return { headers, data };
        },

        /**
         * Check if an image/file exists
         * @param {string} url - The URL to check
         * @returns {Promise<boolean>} Promise that resolves to true if file exists
         */
        fileExists: function(url) {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                img.src = url;
            });
        }
    };

    // Expose to global scope
    window.NFLCommon = NFLCommon;

})(window);
