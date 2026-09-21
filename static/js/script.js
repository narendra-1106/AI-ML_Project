/* ==========================================================================
   IPL MATCH WINNER PREDICTION - DYNAMIC FORM INTERACTIVITY (script.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const tossSelect = document.getElementById('toss_winner');
    const predictionForm = document.getElementById('predictionForm');

    if (team1Select && team2Select && tossSelect) {
        
        function updateTossWinnerOptions() {
            const team1 = team1Select.value;
            const team2 = team2Select.value;
            const currentToss = tossSelect.value;

            // Clear existing toss options except default placeholder
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
        
        // Run once on load if values are pre-selected
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
});
