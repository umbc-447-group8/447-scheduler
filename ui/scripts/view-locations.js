$('.modal').modal();
var locations_path = apiPath + "/locations";
console.log(locations_path);

//Initialize the table that displays the locations
var table = $('#location_table').DataTable( {
  ajax: {
       url: locations_path,
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

// Event handler for delete button
$('#employee_table tbody').on('click', '.delete_button', function() {
  var data = table.row($(this).parents('tr')).data();
  $('#employee_id_delete').html(data['employee_id']);
});

// End modal initizing

// API handling

//Function to edit an location entry
function put_location() {
    var name = $("#name").val();
    var coverage = [
        [+ $("#mon_shift1").prop('checked'), + $("#mon_shift2").prop('checked'), + $("#mon_shift3").prop('checked')],
        [+ $("#tue_shift1").prop('checked'), + $("#tue_shift2").prop('checked'), + $("#tue_shift3").prop('checked')],
        [+ $("#wen_shift1").prop('checked'), + $("#wen_shift2").prop('checked'), + $("#wen_shift3").prop('checked')],
        [+ $("#thu_shift1").prop('checked'), + $("#thu_shift2").prop('checked'), + $("#thu_shift3").prop('checked')],
        [+ $("#fri_shift1").prop('checked'), + $("#fri_shift2").prop('checked'), + $("#fri_shift3").prop('checked')],
        [+ $("#sat_shift1").prop('checked'), + $("#sat_shift2").prop('checked'), + $("#sat_shift3").prop('checked')],
        [+ $("#sun_shift1").prop('checked'), + $("#sun_shift2").prop('checked'), + $("#sun_shift3").prop('checked')],
    ];
  // Make API call
  axios.put(apiPath + '/locations/' + name, {
      name: name,
      coverage: coverage,
    })
    .then(function (response) {
      console.log(response);
      M.toast({html: name + " has been updated", classes: 'rounded green accent-4'});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Error, update failed", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when we are done
    M.Modal.getInstance(document.getElementById('edit_location_modal')).close();
}

//Handle the delete location event
function delete_location() {
  var name = $('#location_delete').html()
  //Make API call
  axios.delete(apiPath + '/locations/' + name)
    .then(function (response) {
      console.log(response);
      M.toast({html: name + " has been deleted", classes: 'rounded'});
      table.ajax.reload();
    })
    .catch(function (error) {
      M.toast({html: "Error, could not complete request ", classes: 'rounded red'});
      console.log(error);
    });

    // Close modal when we are done
    M.Modal.getInstance(document.getElementById('delete_location_modal')).close();
}

// End API handling

// Initialize datatables select box
$('select').formSelect();
