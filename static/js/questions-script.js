function toggleCheck(checkbox) {
        // Suchen Sie das übergeordnete <div> des geänderten Kontrollkästchens
        var parentDiv = checkbox.closest('.card');

        // Durchlaufen Sie die Checkboxen innerhalb des übergeordneten <div>
        var checkboxes = parentDiv.querySelectorAll('input[type="checkbox"]');
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i] !== checkbox) {
                checkboxes[i].checked = false; // Anderes Kontrollkästchen abwählen
            }
        }
    }

    function checkButtons() {
            var cards = document.querySelectorAll('.card');
            var button = document.getElementById('weiterbtn');
            var allCardsHaveCheckboxChecked = true;

            // Überprüfen, ob in jedem .card-Div mindestens eine Checkbox ausgewählt ist
            for (var i = 0; i < cards.length; i++) {
                var checkboxes = cards[i].querySelectorAll('input[type="checkbox"]');
                var atLeastOneChecked = false;

                // Überprüfen, ob mindestens eine Checkbox in diesem .card-Div ausgewählt ist
                for (var j = 0; j < checkboxes.length; j++) {
                    if (checkboxes[j].checked) {
                        atLeastOneChecked = true;
                        break; // Wenn mindestens eine Checkbox ausgewählt ist, abbrechen
                    }
                }

                if (!atLeastOneChecked) {
                    allCardsHaveCheckboxChecked = false;
                    break; // Wenn mindestens ein .card-Div keine ausgewählte Checkbox hat, abbrechen
                }
            }

            // Button aktivieren oder deaktivieren und Design ändern
            if (allCardsHaveCheckboxChecked) {
                button.disabled = false;
            } else {
                button.disabled = true;
            }
        }