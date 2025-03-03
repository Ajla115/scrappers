// Array of last names extracted from the CSV file
const lastNames2 = [ "Beširović", "Zatega", "Mešić", "Isović", "Čalkić", "Šorlija", 





    "Okanović", "Skeledžija", "Bešić", "Dupanović", "Mujić", "Hadžihasanović",  "El Idrissi", "Šoja",
    "Ćebić", "Hodžić", "Brčaninović", "Hrabač", "Morankić", "Prlenda", "Jovanović", "Ibrić", "Simjanoski", "Alić", "Ertunç",
    "Balihodžić", "Durak", "Alić", "Šahbegović", "Osmanović", "Čakal", "Kanurić", "Sarajlić", "Šekić", "Hasanović", "Milanović",
    "Avdukić", "Kusturica", "Smajić", "Hasanović", "Mizdrak", "Zurapi", "Keçici", "Pleho", "Pozder", "Radonja", "Melunović",
    "Alshanwan", "Alqahtani", "Hadrović", "Korman", "Kurtović", "Maksumić", "Trbović", "Tufo", "Delibašić", "Akyol", "Šemić",
    "Čakanović"
];

// Array of last names extracted from the CSV file


const courseIds = [4793, 4792, 4794, 4795, 4038];

// Function that registers courses by triggering the select2:select event
function registerCourses() {
  var event = jQuery.Event("select2:select");
  for (var i = 0; i < courseIds.length; i++) {
    event.params = { 'data': { 'course_id': String(courseIds[i]) } };
    $('#all-registration-courses').select2().trigger(event);
  }
}
const lastNames = [  "Salčinović", "Čuruković", "Mičić", "Kerić" ];

// Function that selects a student and then registers courses for that student
function selectStudent(lastName, index) {
    setTimeout(function() {
      // Open the Select2 dropdown for student selection
      $('#student_filter').select2('open');
      
      setTimeout(function() {
        let searchField = $('.select2-search__field');
        if (searchField.length) {
          // Type the student's last name into the search field
          searchField.val(lastName).trigger('input');
          
          setTimeout(function() {
            // Look for the option that matches the last name
            let option = $('.select2-results__option:contains("' + lastName + '")');
            if (option.length) {
              option.trigger('mouseup');
              $('#student_filter').trigger('change');
              
              // Once the student is selected, register all courses for this student
              registerCourses();
            } else {
              console.warn("No match found for:", lastName);
            }
            
            // After a delay, proceed to the next student (adjust the delay as needed)
            if (index + 1 < lastNames.length) {
              setTimeout(function(){
                selectStudent(lastNames[index + 1], index + 1);
              }, 2000);
            }
          }, 800); // Allow extra time for search results to appear
        } else {
          console.warn("Search field not found for:", lastName);
        }
      }, 400); // Delay to ensure the dropdown is fully loaded
    }, 1200 * index); // Stagger the student processing to prevent overlap
  }
  
  // Start processing the students if the list is not empty
  if (lastNames.length > 0) {
    selectStudent(lastNames[0], 0);
  }