/* ==========================================================================
   IPL MATCH WINNER PREDICTION - JAVASCRIPT & CHART.JS UTILITIES (script.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    
    // ----------------------------------------------------------------------
    // 0. MOBILE NAVBAR HAMBURGER TOGGLE
    // ----------------------------------------------------------------------
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Close mobile nav when clicking outside
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }

    // ----------------------------------------------------------------------
    // 1. DYNAMIC FORM INTERACTIVITY (PREDICTION PAGE)
    // ----------------------------------------------------------------------
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const tossSelect = document.getElementById('toss_winner');
    const predictionForm = document.getElementById('predictionForm');

    if (team1Select && team2Select && tossSelect) {
        function updateTossWinnerOptions() {
            const team1 = team1Select.value;
            const team2 = team2Select.value;
            const currentToss = tossSelect.value;

            tossSelect.innerHTML = '<option value="" disabled selected>-- Select Toss Winner --</option>';

            if (team1 && team2 && team1 === team2) {
                alert('Team 1 and Team 2 cannot be the same franchise!');
                team2Select.value = '';
                return;
            }

            if (team1) {
                const opt1 = document.createElement('option');
                opt1.value = team1;
                opt1.textContent = team1;
                if (currentToss === team1) opt1.selected = true;
                tossSelect.appendChild(opt1);
            }

            if (team2 && team2 !== team1) {
                const opt2 = document.createElement('option');
                opt2.value = team2;
                opt2.textContent = team2;
                if (currentToss === team2) opt2.selected = true;
                tossSelect.appendChild(opt2);
            }
        }

        team1Select.addEventListener('change', updateTossWinnerOptions);
        team2Select.addEventListener('change', updateTossWinnerOptions);
        
        if (team1Select.value || team2Select.value) {
            updateTossWinnerOptions();
        }
    }

    if (predictionForm) {
        predictionForm.addEventListener('submit', (e) => {
            const t1 = team1Select.value;
            const t2 = team2Select.value;
            if (t1 === t2) {
                e.preventDefault();
                alert('Validation Error: Team 1 and Team 2 cannot be identical!');
            }
        });
    }

    // ----------------------------------------------------------------------
    // 2. CHART.JS VISUALIZATIONS (DASHBOARD PAGE)
    // ----------------------------------------------------------------------
    if (typeof dashboardData !== 'undefined') {
        
        // --- CHART 1: TEAM TOTAL WINS BAR CHART ---
        const teamWinsCanvas = document.getElementById('teamWinsChart');
        if (teamWinsCanvas) {
            new Chart(teamWinsCanvas.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: dashboardData.teamWinLabels,
                    datasets: [{
                        label: 'Total Match Wins',
                        data: dashboardData.teamWinData,
                        backgroundColor: 'rgba(255, 159, 28, 0.75)',
                        borderColor: '#ff9f1c',
                        borderWidth: 1.5,
                        borderRadius: 6,
                        hoverBackgroundColor: 'rgba(255, 159, 28, 0.95)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#121929',
                            titleColor: '#ff9f1c',
                            bodyColor: '#fff',
                            borderColor: 'rgba(255,159,28,0.3)',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 10 } },
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        },
                        y: {
                            ticks: { color: '#94a3b8' },
                            grid: { color: 'rgba(255, 255, 255, 0.08)' }
                        }
                    }
                }
            });
        }

        // --- CHART 2: TOSS IMPACT DOUGHNUT CHART ---
        const tossImpactCanvas = document.getElementById('tossImpactChart');
        if (tossImpactCanvas) {
            new Chart(tossImpactCanvas.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: dashboardData.tossImpactLabels,
                    datasets: [{
                        data: dashboardData.tossImpactData,
                        backgroundColor: [
                            'rgba(0, 245, 212, 0.8)',
                            'rgba(255, 87, 34, 0.8)'
                        ],
                        borderColor: '#121929',
                        borderWidth: 3,
                        hoverOffset: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#f8f9fa', font: { family: 'Plus Jakarta Sans', size: 12 }, padding: 15 }
                        },
                        tooltip: {
                            backgroundColor: '#121929',
                            bodyColor: '#fff',
                            borderColor: 'rgba(255,255,255,0.1)',
                            borderWidth: 1
                        }
                    },
                    cutout: '65%'
                }
            });
        }

    }
});
