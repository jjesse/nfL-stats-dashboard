/**
 * Interactive Charts Enhancement Module
 * Provides zoom, pan, and interactive features for NFL stats charts
 * 
 * Features:
 * - Chart zoom controls (zoom in, zoom out, reset)
 * - Fullscreen mode
 * - Hover tooltips with detailed stats
 * - Click to zoom functionality
 * - Responsive chart sizing
 */

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        zoomStep: 0.2,
        minZoom: 1,
        maxZoom: 3,
        animationDuration: 300,
        tooltipDelay: 200
    };
    
    // State management
    let chartStates = new Map();
    
    /**
     * Initialize interactive features for all charts on the page
     */
    function initializeCharts() {
        const charts = document.querySelectorAll('.chart-container img, img[src$=".png"]');
        
        charts.forEach((chart, index) => {
            if (!chart.id) {
                chart.id = `interactive-chart-${index}`;
            }
            
            // Skip if already initialized
            if (chartStates.has(chart.id)) {
                return;
            }
            
            // Initialize state
            chartStates.set(chart.id, {
                zoom: 1,
                rotation: 0,
                originalSrc: chart.src
            });
            
            // Add interactive controls
            addChartControls(chart);
            
            // Add event listeners
            addChartEventListeners(chart);
        });
        
        console.log(`✅ Initialized ${charts.length} interactive charts`);
    }
    
    /**
     * Add control buttons to a chart
     */
    function addChartControls(chart) {
        const container = chart.closest('.chart-container') || chart.parentElement;
        
        // Check if controls already exist
        if (container.querySelector('.chart-controls')) {
            return;
        }
        
        const controls = document.createElement('div');
        controls.className = 'chart-controls';
        controls.innerHTML = `
            <button class="chart-btn zoom-in" title="Zoom In" aria-label="Zoom In">🔍+</button>
            <button class="chart-btn zoom-out" title="Zoom Out" aria-label="Zoom Out">🔍-</button>
            <button class="chart-btn rotate" title="Rotate" aria-label="Rotate">↻</button>
            <button class="chart-btn fullscreen" title="Fullscreen" aria-label="Fullscreen">⛶</button>
            <button class="chart-btn reset" title="Reset View" aria-label="Reset">⟲</button>
        `;
        
        // Add styles if not already present
        if (!document.querySelector('#interactive-charts-styles')) {
            addControlStyles();
        }
        
        container.style.position = 'relative';
        container.appendChild(controls);
    }
    
    /**
     * Add CSS styles for chart controls
     */
    function addControlStyles() {
        const style = document.createElement('style');
        style.id = 'interactive-charts-styles';
        style.textContent = `
            .chart-controls {
                position: absolute;
                top: 10px;
                right: 10px;
                display: flex;
                gap: 5px;
                z-index: 100;
                opacity: 0.7;
                transition: opacity 0.3s ease;
            }
            
            .chart-controls:hover {
                opacity: 1;
            }
            
            .chart-btn {
                background: rgba(0, 123, 255, 0.9);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            }
            
            .chart-btn:hover {
                background: rgba(0, 123, 255, 1);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
            }
            
            .chart-btn:active {
                transform: translateY(0);
            }
            
            .chart-container img {
                transition: transform 0.3s ease;
                cursor: zoom-in;
            }
            
            .chart-container img.zoomed {
                cursor: zoom-out;
            }
            
            .chart-fullscreen {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0, 0, 0, 0.95);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .chart-fullscreen img {
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
            }
            
            .chart-tooltip {
                position: absolute;
                background: rgba(0, 0, 0, 0.9);
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
                font-size: 14px;
                pointer-events: none;
                z-index: 1000;
                white-space: nowrap;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            }
            
            @media (max-width: 768px) {
                .chart-controls {
                    flex-wrap: wrap;
                    opacity: 1;
                }
                
                .chart-btn {
                    padding: 6px 10px;
                    font-size: 14px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    /**
     * Add event listeners to a chart
     */
    function addChartEventListeners(chart) {
        const container = chart.closest('.chart-container') || chart.parentElement;
        const controls = container.querySelector('.chart-controls');
        
        if (!controls) return;
        
        // Zoom in
        controls.querySelector('.zoom-in')?.addEventListener('click', (e) => {
            e.stopPropagation();
            zoomChart(chart, CONFIG.zoomStep);
        });
        
        // Zoom out
        controls.querySelector('.zoom-out')?.addEventListener('click', (e) => {
            e.stopPropagation();
            zoomChart(chart, -CONFIG.zoomStep);
        });
        
        // Rotate
        controls.querySelector('.rotate')?.addEventListener('click', (e) => {
            e.stopPropagation();
            rotateChart(chart);
        });
        
        // Fullscreen
        controls.querySelector('.fullscreen')?.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFullscreen(chart);
        });
        
        // Reset
        controls.querySelector('.reset')?.addEventListener('click', (e) => {
            e.stopPropagation();
            resetChart(chart);
        });
        
        // Click to zoom
        chart.addEventListener('click', (e) => {
            if (!e.target.classList.contains('chart-btn')) {
                const state = chartStates.get(chart.id);
                if (state.zoom === 1) {
                    zoomChart(chart, 1); // Zoom to 2x
                } else {
                    resetChart(chart);
                }
            }
        });
    }
    
    /**
     * Zoom a chart
     */
    function zoomChart(chart, delta) {
        const state = chartStates.get(chart.id);
        let newZoom = state.zoom + delta;
        
        // Clamp zoom level
        newZoom = Math.max(CONFIG.minZoom, Math.min(CONFIG.maxZoom, newZoom));
        
        state.zoom = newZoom;
        applyTransform(chart);
        
        // Update cursor
        if (newZoom > 1) {
            chart.classList.add('zoomed');
        } else {
            chart.classList.remove('zoomed');
        }
    }
    
    /**
     * Rotate a chart
     */
    function rotateChart(chart) {
        const state = chartStates.get(chart.id);
        state.rotation = (state.rotation + 90) % 360;
        applyTransform(chart);
    }
    
    /**
     * Apply transform to chart
     */
    function applyTransform(chart) {
        const state = chartStates.get(chart.id);
        chart.style.transform = `scale(${state.zoom}) rotate(${state.rotation}deg)`;
    }
    
    /**
     * Reset chart to original state
     */
    function resetChart(chart) {
        const state = chartStates.get(chart.id);
        state.zoom = 1;
        state.rotation = 0;
        applyTransform(chart);
        chart.classList.remove('zoomed');
    }
    
    /**
     * Toggle fullscreen mode
     */
    function toggleFullscreen(chart) {
        // Check if already in fullscreen
        let fullscreenContainer = document.querySelector('.chart-fullscreen');
        
        if (fullscreenContainer) {
            // Exit fullscreen
            fullscreenContainer.remove();
            document.body.style.overflow = '';
            return;
        }
        
        // Enter fullscreen
        fullscreenContainer = document.createElement('div');
        fullscreenContainer.className = 'chart-fullscreen';
        
        const fullscreenImg = chart.cloneNode(true);
        fullscreenImg.style.transform = ''; // Reset transform in fullscreen
        
        fullscreenContainer.appendChild(fullscreenImg);
        document.body.appendChild(fullscreenContainer);
        document.body.style.overflow = 'hidden';
        
        // Click outside to exit
        fullscreenContainer.addEventListener('click', (e) => {
            if (e.target === fullscreenContainer) {
                fullscreenContainer.remove();
                document.body.style.overflow = '';
            }
        });
        
        // ESC to exit
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                fullscreenContainer?.remove();
                document.body.style.overflow = '';
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);
    }
    
    /**
     * Create and show tooltip
     */
    function showTooltip(chart, text, x, y) {
        let tooltip = document.querySelector('.chart-tooltip');
        
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.className = 'chart-tooltip';
            document.body.appendChild(tooltip);
        }
        
        tooltip.textContent = text;
        tooltip.style.left = `${x + 10}px`;
        tooltip.style.top = `${y + 10}px`;
        tooltip.style.display = 'block';
    }
    
    /**
     * Hide tooltip
     */
    function hideTooltip() {
        const tooltip = document.querySelector('.chart-tooltip');
        if (tooltip) {
            tooltip.style.display = 'none';
        }
    }
    
    /**
     * Initialize on DOM ready
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeCharts);
    } else {
        initializeCharts();
    }
    
    // Reinitialize on dynamic content load
    const observer = new MutationObserver((mutations) => {
        let shouldReinitialize = false;
        
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1 && 
                    (node.tagName === 'IMG' || node.querySelector('img'))) {
                    shouldReinitialize = true;
                }
            });
        });
        
        if (shouldReinitialize) {
            setTimeout(initializeCharts, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Export for manual initialization if needed
    window.NFLCharts = {
        initialize: initializeCharts,
        zoom: zoomChart,
        reset: resetChart,
        fullscreen: toggleFullscreen
    };
    
    console.log('🏈 Interactive Charts module loaded');
    
})();
