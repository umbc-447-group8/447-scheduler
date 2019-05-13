//Get the value of the select box
function post_employee() {
  var employee_type = $("#employee_type").val();
  var first_name = $("#first_name").val();
  var last_name = $("#last_name").val();
  var employee_id = $("#employee_id").val();
  var moonlighter = $("#moonlighter").val();
  if(moonlighter == 'false'){
    moonlighter = false;
  }
  else{
    moonlighter = true;
  }

  axios.post(apiPath + '/employees', {
      employee_id: employee_id,
      firstName: first_name,
      lastName: last_name,
      type: employee_type,
      moonlighter: moonlighter,
    })
    .then(function (response) {
      document.getElementById("add_employee_form").reset();
      M.toast({html: first_name + " " + last_name + " has been added"})
    })
    .catch(function (error) {
      console.log(error);
    });
}

var elems = document.querySelectorAll('select');
var instances = M.FormSelect.init(elems);
