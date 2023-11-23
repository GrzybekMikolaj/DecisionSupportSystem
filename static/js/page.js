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
