// trazenje studenta

$('#student_filter option[contains(.,"Iman")]')

$('#student_filter span:contains("Aljohani")')

// nadji student id

$('#student_filter').val()

// prebaciti na studenta po ID-u

$('#student_filter').select2().val(5613).trigger('change')

// napraviti event sa IDs novih kurseva
var event = jQuery.Event( "select2:select" );

// unijeti ID svih kurseva

event.params = {'data': {'course_id':'4752'}}

//trigger eventa

$('#all-registration-courses').select2().trigger(event)

// prebaciit na studenta po prezimenu

$('#student_filter').select2('open');

setTimeout(function() {
    $('.select2-search__field').val('Aljohani').trigger('input'); 

    setTimeout(function() {
        $('.select2-results__option:contains("Aljohani")').trigger('mouseup'); 
        $('#student_filter').trigger('change');
    }, 500);
}, 300);



// 1. Proci kroz cijelu listu
// Fetchati svako prezime i izvuci ID za njega
// Spasiti ID u kolonu

// 2. Napraviti novu skriptu
// Koja prolazi kroz sve IDs i za svaki ID bira predmete

// Array of last names extracted from the CSV file
const lastNames = [ "Kablaoui", "Husić",
    "Okanović", "Skeledžija", "Bešić", "Dupanović", "Mujić", "Hadžihasanović", "Memić", "Kapetanović", "El Idrissi", "Šoja",
    "Ćebić", "Hodžić", "Brčaninović", "Hrabač", "Morankić", "Prlenda", "Jovanović", "Ibrić", "Simjanoski", "Alić", "Ertunç",
    "Balihodžić", "Durak", "Alić", "Šahbegović", "Osmanović", "Čakal", "Kanurić", "Sarajlić", "Šekić", "Hasanović", "Milanović",
    "Avdukić", "Kusturica", "Smajić", "Hasanović", "Mizdrak", "Zurapi", "Keçici", "Pleho", "Pozder", "Radonja", "Melunović",
    "Alshanwan", "Alqahtani", "Hadrović", "Korman", "Kurtović", "Maksumić", "Trbović", "Tufo", "Delibašić", "Akyol", "Šemić",
    "Čakanović"
];

function selectStudent(lastName, index) {
    setTimeout(function() {
        // Open the Select2 dropdown
        $('#student_filter').select2('open');
        
        setTimeout(function() {
            let searchField = $('.select2-search__field');
            if (searchField.length) {
                searchField.val(lastName).trigger('input');
                
                setTimeout(function() {
                    let option = $('.select2-results__option:contains("' + lastName + '")');
                    if (option.length) {
                        option.trigger('mouseup');
                        $('#student_filter').trigger('change');
                    } else {
                        console.warn("No match found for:", lastName);
                    }
                    
                    // Proceed to the next student
                    if (index + 1 < lastNames.length) {
                        selectStudent(lastNames[index + 1], index + 1);
                    }
                }, 800); // Allow extra time for results to appear
            } else {
                console.warn("Search field not found for:", lastName);
            }
        }, 400); // Slightly longer delay to ensure dropdown is fully loaded
    }, 1200 * index); // Adjusted delay to prevent overlapping executions
}

// Start processing students
if (lastNames.length > 0) {
    selectStudent(lastNames[0], 0);
}

var event = jQuery.Event( "select2:select" );

var courseIds = [4793, 4792, 4794, 4795, 4038];

for (var i = 0; i < courseIds.length; i++) {
  event.params = { 'data': { 'course_id': String(courseIds[i]) } };
  $('#all-registration-courses').select2().trigger(event);
}



