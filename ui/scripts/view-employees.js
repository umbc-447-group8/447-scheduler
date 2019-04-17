$('.modal').modal();
var employees_path = apiPath + "/employees";
console.log(employees_path);

//Initialize the table that displays the employees
var table = $('#employee_table').DataTable( {
  ajax: {
       url: employees_path,
       dataSrc: ''
   },
    "columns": [
        {
            "className":      'details-control',
            "orderable":      false,
            "data":           null,
            "defaultContent": '<button class="expand_button btn-small btn-floating waves-effect waves-light blue"><i class="material-icons">expand_more</i></button>'
        },
        { "data": "name" },
        { "data": "name" },
        { "data": "employee_id" },
        { "data": "type" },
        { data: null },
        {
          data: null,
          render: function ( data, type, row ) {
            return '<button data-target="add_request_modal" data-position="top" data-tooltip="Add Request" class="modal-trigger tooltipped modal-trigger add_request_button btn waves-effect waves-light"><i class="material-icons">add</i></button>';
          },
        },
        {
          data: null,
          render: function ( data, type, row ) {
            return '<button data-target="edit_employee_modal" data-position="top" data-tooltip="Edit Employee" class="tooltipped modal-trigger edit_button btn waves-effect waves-light"><i class="material-icons">edit</i></button>';
          },
        },
        {
          data: null,
          render: function ( data, type, row ) {
            return '<button data-target="delete_employee_modal" data-position="top" data-tooltip="Delete Employee" class="tooltipped red modal-trigger delete_button btn waves-effect waves-light"><i class="material-icons">delete_forever</i></button>';
          },
        },
    ],

    'autoWidth': false,
    'lengthChange': true,
    'ordering': false,
    //Initialize the tool tips when loaded
    "initComplete": function(settings, json) {
      $(".tooltipped").tooltip({enterDelay: 500});
    },
} );
// End table initalization

//Event listener for expand
$('#employee_table tbody').on('click', '.expand_button', function () {
    var tr = $(this).closest('tr');
    var row = table.row( tr );

    if ( row.child.isShown() ) {
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
    }
    else {
        // Open this row
        // Build the table dynamically based off the requests
        axios.get(apiPath + '/requests')
          .then(function (response) {
            request_rows = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
                '<th>Request ID</th>'+
                '<th>Employee Id</th>'+
                '<th>Reqest Day</th>'+
                '<th>Shift</th>'+
                '<th>Weight</th>'+
                '<th>Edit</th>'+
                '<th>Delete</th>'
            // For each response, if response corresponds to current employee,
            // add row.
            response['data'].forEach(function(request) {
              if(request['employee_id'] == row.data()['employee_id']){
                request_rows += '<tr>'+
                                  '<td>'+request['request_id']+'</td>'+
                                  '<td>'+request['employee_id']+'</td>'+
                                  '<td>'+request['day']+'</td>'+
                                  '<td>'+request['shift']+'</td>'+
                                  '<td>'+request['weight']+'</td>'+
                                  '<td><button data-target="edit_request_modal" data-position="top" data-tooltip="Edit Request" class="edit_request_button blue btn-small tooltipped modal-trigger edit_request_button btn waves-effect waves-light"><i class="material-icons">edit</i></button></td>'+
                                  '<td><button data-target="delete_request_modal" data-position="top" data-tooltip="Delete Request" class="delete_request_button btn-small red tooltipped modal-trigger edit_request_button btn waves-effect waves-light"><i class="material-icons">delete_forever</i></button></td></td>'+
                                '</tr>'
              }
            });
            request_rows += '</table>';
            row.child( request_rows ).show();
            tr.addClass('shown');
          })
          .catch(function (error) {
            // handle error
            console.log(error);
          })
    }
});

// xxx modal initizing

// Initialize the edit epmloyee modal
$('#employee_table tbody').on('click', '.edit_button', function() {
  var data = table.row($(this).parents('tr')).data();

  document.getElementById('first_name_put').value = data['name'];
  document.getElementById('last_name_put').value = data['name'];
  document.getElementById('employee_id_put').value = data['employee_id'];
  document.getElementById('employee_type_put').value = data['type'];

  //Reinitalize select
  $('select').formSelect();
  M.updateTextFields();
});

// initalize new request modal
$('#employee_table tbody').on('click', '.add_request_button', function() {
  var data = table.row($(this).parents('tr')).data();

  document.getElementById('employee_id_request').value = data['employee_id'];

  // Reinitalize date picker
  var elems = document.querySelectorAll('.datepicker');
  var instances = M.Datepicker.init(elems);

  //Reinitalize select
  $('select').formSelect();
  M.updateTextFields();
});

// Initialize the edit request modal
$('#employee_table tbody').on('click', '.edit_request_button', function() {
  var data = $(this).parents('tr')[0]['cells']

  document.getElementById('edit_request_id').innerHTML = data[0].innerHTML;
  document.getElementById('employee_id_request_edit').value = data[1].innerHTML;
  document.getElementById('date_request_edit').value = data[2].innerHTML;
  document.getElementById('shift_request_edit').value = data[3].innerHTML;
  document.getElementById('weight_request_edit').value = data[4].innerHTML;

  //Reinitalize select
  $('select').formSelect();
  M.updateTextFields();
});

// Event handler for delete button
$('#employee_table tbody').on('click', '.delete_button', function() {
  var data = table.row($(this).parents('tr')).data();
  $('#employee_id_delete').html(data['employee_id']);
});

$('#employee_table').on('click', '.delete_request_button', function() {
  var data = $(this).parents('tr')[0]['cells'][0].innerHTML
  $('#request_employee_id_delete').html(data);
});

// End modal initizing

// API handling

//Function to edit an employee entry
function put_employee() {
  var employee_type = $("#employee_type_put").val();
  var first_name = $("#first_name_put").val();
  var last_name = $("#last_name_put").val();
  var employee_id = $("#employee_id_put").val();
  var moonlighter = $("#moonlighter_put").val();
  // Make API call
  axios.put(apiPath + '/employees/' + employee_id, {
      employee_id: employee_id,
      name: first_name + " " + last_name,
      type: employee_type,
    })
    .then(function (response) {
      console.log(response);
      M.toast({html: first_name + " " + last_name + " has been updated", classes: 'rounded green accent-4'});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Error, update failed", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when we are done
    M.Modal.getInstance(document.getElementById('edit_employee_modal')).close();
}

//Function to edit a request entry
function put_request() {
  var employee_id = $("#employee_id_request_edit").val();
  var date = $("date_request_edit").val();
  var shift = $("#shift_request_edit").val();
  var weight = $("#weight_request_edit").val();
  var request_id = document.getElementById('edit_request_id').innerHTML;

  // Make API call
  axios.put(apiPath + '/requests/' + request_id, {
      employee_id: employee_id,
      day: date,
      shift: shift,
      weight: weight,
    })
    .then(function (response) {
      console.log(response);
      M.toast({html: request_id + " has been updated", classes: 'rounded green accent-4'});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Update Failed", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when we are done
    M.Modal.getInstance(document.getElementById('edit_request_modal')).close();
}

//Handle the delete exployee event
function delete_employee() {
  var employee_id = $('#employee_id_delete').html()
  //Make API call
  axios.delete(apiPath + '/employees/' + employee_id)
    .then(function (response) {
      console.log(response);
      M.toast({html: employee_id + " has been deleted", classes: 'rounded'});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Error, could not complete request ", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when we are done
    M.Modal.getInstance(document.getElementById('delete_employee_modal')).close();
}

//Handle the delete request event
function delete_request() {
  var employee_id = $('#request_employee_id_delete').html()
  //Make API call
  axios.delete(apiPath + '/requests/' + employee_id)
    .then(function (response) {
      console.log(response);
      M.toast({html: "request for " + employee_id + " has been deleted", classes: 'rounded'});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Error, could not complete request ", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when we are done
    M.Modal.getInstance(document.getElementById('delete_request_modal')).close();
}

// Add a new request to the API
function post_request(){
  var request_date = $("#request_date_request").val();
  var employee_id = $("#employee_id_request").val();
  var shift = $("#shift_request").val();
  var weight = $("#weight_request").val();

  axios.post(apiPath + '/requests', {
      employee_id: employee_id,
      shift: shift,
      weight: weight,
      day: request_date,
    })
    .then(function (response) {
      console.log(response);
      document.getElementById("add_request_form").reset();
      M.toast({html: "The request has been added"});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Error, request Failed", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when done
    M.Modal.getInstance(document.getElementById('add_request_modal')).close();
  }

// End API handling

// Initialize datatables select box
$('select').formSelect();
