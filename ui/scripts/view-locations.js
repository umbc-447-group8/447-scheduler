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
            "data": "name"
        },
        { data:function (data, type, row) {
                return data.coverage[0][0] + data.coverage[0][1] + data.coverage[0][2];
            }
        },
        { data:function (data, type, row) {
                return data.coverage[1][0] + data.coverage[1][1] + data.coverage[1][2];
            }
        },
        { data:function (data, type, row) {
                return data.coverage[2][0] + data.coverage[2][1] + data.coverage[2][2];
            }
        },
        { data:function (data, type, row) {
                return data.coverage[3][0] + data.coverage[3][1] + data.coverage[3][2];
            }
        },
        { data:function (data, type, row) {
                return data.coverage[4][0] + data.coverage[4][1] + data.coverage[4][2];
            }
        },
        { data:function (data, type, row) {
                return data.coverage[5][0] + data.coverage[5][1] + data.coverage[5][2];
            }
        },
        { data:function (data, type, row) {
                return data.coverage[6][0] + data.coverage[6][1] + data.coverage[6][2];
            }
        },
        {
          data: null,
          render: function ( data, type, row ) {
            return '<button data-target="edit_location_modal" data-position="top" data-tooltip="Edit Location" class="tooltipped modal-trigger edit_button btn waves-effect waves-light"><i class="material-icons">edit</i></button>';
          },
        },
        {
          data: null,
          render: function ( data, type, row ) {
            return '<button data-target="delete_location_modal" data-position="top" data-tooltip="Delete Location" class="tooltipped red modal-trigger delete_button btn waves-effect waves-light"><i class="material-icons">delete_forever</i></button>';
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


// xxx modal initizing

// Initialize the edit location modal
$('#location_table tbody').on('click', '.edit_button', function() {
  var data = table.row($(this).parents('tr')).data();

  document.getElementById('name_put').value = data['name'];
  var coverage = data['coverage'];
  document.getElementById('mon_shift1').checked = coverage[0][0];
  document.getElementById('mon_shift2').checked = coverage[0][1];
  document.getElementById('mon_shift3').checked = coverage[0][2];

  document.getElementById('tue_shift1').checked = coverage[1][0];
  document.getElementById('tue_shift2').checked = coverage[1][1];
  document.getElementById('tue_shift3').checked = coverage[1][2];

  document.getElementById('wen_shift1').checked = coverage[2][0];
  document.getElementById('wen_shift2').checked = coverage[2][1];
  document.getElementById('wen_shift3').checked = coverage[2][2];

  document.getElementById('thu_shift1').checked = coverage[3][0];
  document.getElementById('thu_shift2').checked = coverage[3][1];
  document.getElementById('thu_shift3').checked = coverage[3][2];

  document.getElementById('fri_shift1').checked = coverage[4][0];
  document.getElementById('fri_shift2').checked = coverage[4][1];
  document.getElementById('fri_shift3').checked = coverage[4][2];

  document.getElementById('sat_shift1').checked = coverage[5][0];
  document.getElementById('sat_shift2').checked = coverage[5][1];
  document.getElementById('sat_shift3').checked = coverage[5][2];

  document.getElementById('sun_shift1').checked = coverage[6][0];
  document.getElementById('sun_shift2').checked = coverage[6][1];
  document.getElementById('sun_shift3').checked = coverage[6][2];



  //Reinitalize select
  $('select').formSelect();
  M.updateTextFields();
});

// Event handler for delete button
$('#location_table tbody').on('click', '.delete_button', function() {
  var data = table.row($(this).parents('tr')).data();
  $('#location_delete').html(data['name']);
});

// End modal initizing

// API handling

//Function to edit an location entry
function put_location() {
    var name = $("#name_put").val();
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
