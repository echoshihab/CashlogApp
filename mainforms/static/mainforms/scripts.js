//jquery functions

//datepicker function
//.datepicker is for cashlog form
$( function() {
    $( ".datepicker" ).datepicker().datepicker("setDate", new Date());
  } );

//.datepay is for patient pay form
$( function() {
    $( ".datePay" ).datepicker().datepicker("setDate", new Date());

  } );

//.datepicker update is for superuser update page
$(function(){
    $(".datepickerupdate").datepicker();
});

//auditdate is for audit search page


$(function(){
    $(".auditdate").datepicker();
});


//modal open function



