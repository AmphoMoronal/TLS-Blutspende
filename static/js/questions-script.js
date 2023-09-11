function toggleCheck(checkbox) {
    // Suchen Sie das übergeordnete <div> des geänderten Kontrollkästchens
    let parentDiv = checkbox.closest('.card');

    // Durchlaufen Sie die Checkboxen innerhalb des übergeordneten <div>
    let checkboxes = parentDiv.querySelectorAll('input[type="checkbox"]');
    for (const element of checkboxes) {
        if (element !== checkbox) {
            element.checked = false; // Anderes Kontrollkästchen abwählen
        }
    }
}

function checkButtons() {
    let cards = document.querySelectorAll('.card');
    let button = document.getElementById('weiterbtn');
    let allCardsHaveCheckboxChecked = true;

    // Überprüfen, ob in jedem .card-Div mindestens eine Checkbox ausgewählt ist
    for (const element of cards) {
        let checkboxes = element.querySelectorAll('input[type="checkbox"]');
        let atLeastOneChecked = false;

        // Überprüfen, ob mindestens eine Checkbox in diesem .card-Div ausgewählt ist
        for (let j of checkboxes.length) {
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
    button.disabled = !allCardsHaveCheckboxChecked;
}