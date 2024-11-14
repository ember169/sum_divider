let envelopeCount = 0;
let envelopesData = [];

// Fonction pour afficher la zone d'ajout de nouvelles enveloppes
function showEnvelopeFields() {
    const envelopeFields = document.getElementById('envelope-fields');
    envelopeFields.style.display = 'block';
}

// Fonction pour annuler l'ajout de nouvelles enveloppes
function cancelEnvelopeFields() {
    const envelopeFields = document.getElementById('envelope-fields');
    envelopeFields.style.display = 'none';

    // Efface les champs de saisie
    document.getElementById('envelope-name').value = '';
    document.getElementById('envelope-percentage').value = '';
}

// Fonction pour valider l'ajout d'une nouvelle enveloppe
function validateEnvelope() {
    const nameInput = document.getElementById('envelope-name');
    const percentageInput = document.getElementById('envelope-percentage');

    const name = nameInput.value.trim();
    const percentage = parseFloat(percentageInput.value);

    if (name && !isNaN(percentage)) {
        envelopeCount++;

        // Ajouter l'enveloppe aux données et au localStorage
        envelopesData.push({ nom: name, pourcentage: percentage });
        saveEnvelopes();

        addEnvelopeToSavedList(name, percentage, envelopeCount);
        createHiddenInputs(name, percentage, envelopeCount);

        // Réinitialise les champs de saisie
        nameInput.value = '';
        percentageInput.value = '';
    } else {
        alert("Veuillez remplir le nom et le pourcentage de l'enveloppe.");
    }
}

// Fonction pour ajouter une enveloppe à la liste affichée
function addEnvelopeToSavedList(name, percentage, count) {
    const envelopeItem = document.createElement('div');
    envelopeItem.classList.add('envelope-item');

    const envelopeText = document.createElement('span');
    envelopeText.innerHTML = `<strong>${name}</strong>: ${percentage}%`;

    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.classList.add('remove-envelope');
    removeButton.innerHTML = '&times;';
    removeButton.onclick = function() {
        envelopeItem.remove();
        document.getElementById(`hidden-name-${count}`).remove();
        document.getElementById(`hidden-percentage-${count}`).remove();

        // Supprimer l'enveloppe des données et mettre à jour le localStorage
        envelopesData = envelopesData.filter((_, index) => index !== count - 1);
        saveEnvelopes();

        // Réindexer les enveloppes restantes
        reindexEnvelopes();
    };

    envelopeItem.appendChild(envelopeText);
    envelopeItem.appendChild(removeButton);

    document.getElementById('saved-envelopes-list').appendChild(envelopeItem);
}

// Fonction pour créer les champs cachés pour soumettre les enveloppes avec le formulaire
function createHiddenInputs(name, percentage, count) {
    const hiddenNameInput = document.createElement('input');
    hiddenNameInput.type = 'hidden';
    hiddenNameInput.name = `enveloppe-nom-${count}`;
    hiddenNameInput.value = name;
    hiddenNameInput.id = `hidden-name-${count}`;

    const hiddenPercentageInput = document.createElement('input');
    hiddenPercentageInput.type = 'hidden';
    hiddenPercentageInput.name = `enveloppe-pourcentage-${count}`;
    hiddenPercentageInput.value = percentage;
    hiddenPercentageInput.id = `hidden-percentage-${count}`;

    document.querySelector('form').appendChild(hiddenNameInput);
    document.querySelector('form').appendChild(hiddenPercentageInput);
}

// Fonction pour charger les enveloppes depuis le localStorage
function loadEnvelopes() {
    const savedEnvelopes = localStorage.getItem('envelopes');
    if (savedEnvelopes) {
        envelopesData = JSON.parse(savedEnvelopes);
        envelopeCount = envelopesData.length;
        for (let i = 0; i < envelopesData.length; i++) {
            const envelope = envelopesData[i];
            addEnvelopeToSavedList(envelope.nom, envelope.pourcentage, i + 1);
            createHiddenInputs(envelope.nom, envelope.pourcentage, i + 1);
        }
    }
}

// Fonction pour sauvegarder les enveloppes dans le localStorage
function saveEnvelopes() {
    localStorage.setItem('envelopes', JSON.stringify(envelopesData));
}

// Fonction pour réindexer les enveloppes après une suppression
function reindexEnvelopes() {
    // Supprimer tous les champs cachés existants
    const form = document.querySelector('form');
    const hiddenInputs = form.querySelectorAll('input[type="hidden"]');
    hiddenInputs.forEach(input => input.remove());

    // Réinitialiser le compteur
    envelopeCount = envelopesData.length;

    // Réajouter les enveloppes et les champs cachés
    const savedEnvelopesList = document.getElementById('saved-envelopes-list');
    savedEnvelopesList.innerHTML = '';
    for (let i = 0; i < envelopesData.length; i++) {
        const envelope = envelopesData[i];
        const count = i + 1;
        addEnvelopeToSavedList(envelope.nom, envelope.pourcentage, count);
        createHiddenInputs(envelope.nom, envelope.pourcentage, count);
    }
}

// Au chargement de la page, charger les enveloppes depuis le localStorage
window.onload = function() {
    loadEnvelopes();
};
