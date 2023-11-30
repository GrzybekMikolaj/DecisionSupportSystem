// Pobierz wszystkie sekcje
const sections = document.querySelectorAll('.section');

// Funkcja przewijająca do konkretnej sekcji
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// JavaScript function to handle dropdown list selection
function showSelected() {
    var selectedValue = document.getElementById("algorithm").value;
    alert("Selected: " + selectedValue);
}

function createWeightsForm(parameters) {
    // Utwórz formularz
    var form = document.createElement('weights-form');
    var target_div  =document.getElementById('weightsForm');
    var wght_str = 'weight';
    // Iteruj przez tablicę z nazwami wartości
    for (var i = 2; i < parameters.length; i++) {
      // Utwórz pole tekstowe dla każdej nazwy wartości
      var input = document.createElement('input');
      input.type = 'number'; // Ustaw typ pola na liczbowy
      input.name = parameters[i]; // Ustaw nazwę pola na wartość z tablicy
      input.id = wght_str.concat('', i-2);
      // Utwórz etykietę dla pola tekstowego
      var label = document.createElement('label');
      label.innerHTML = parameters[i]; // Ustaw tekst etykiety na nazwę wartości
      // Dodaj etykietę i pole tekstowe do formularza
      form.appendChild(label);
      form.appendChild(input);
      // Dodaj odstęp pomiędzy polami
      form.appendChild(document.createElement('br'));
    }
    // Dodaj formularz do elementu body (możesz dostosować to, gdzie chcesz dodać formularz)
    target_div.appendChild(form);
  }


  function showFields() {
    // Ukryj wszystkie pola formularza
    document.getElementById('topsisFields').classList.add('hidden');
    document.getElementById('rsmFields').classList.add('hidden');
    document.getElementById('spcsFields').classList.add('hidden');

    // Pobierz wybraną wartość z rozwijanej listy
    var selectedAlgorithm = document.getElementById('algorithm').value;

    // Wyświetl odpowiednie pola formularza w zależności od wybranej opcji
    if (selectedAlgorithm === 'topsis') {
        document.getElementById('topsisFields').classList.remove('hidden');
    } else if (selectedAlgorithm === 'rsm') {
        document.getElementById('rsmFields').classList.remove('hidden');
    } else if (selectedAlgorithm === 'spcs') {
        document.getElementById('spcsFields').classList.remove('hidden');
    }
}
