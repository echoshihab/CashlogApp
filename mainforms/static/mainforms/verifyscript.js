// function to set values number values to 0 if nothing is entered;

function nullTester(arg) {
  if (arg == null || arg == ""){
    arg = 0;
    return arg;
  }
  else {
    return arg;
  }
}

// this function removes all validation alert from cashlog form
function clogAlertRemover() {
  document.getElementById("namealert").innerHTML = "";
  document.getElementById("datealert").innerHTML = "";
  document.getElementById("localert").innerHTML = "";
  document.getElementById("shiftalert").innerHTML = "";
  document.getElementById("id_cashlog-staffname").classList.remove('is-invalid');
  document.getElementById("id_entrydate").classList.remove('is-invalid');
}

//this function removes all validation alert from patient pay form
function ptpayAlertRemover() {
  document.getElementById("namealertp").innerHTML = "";
  document.getElementById("datealertp").innerHTML = "";
  document.getElementById("localertp").innerHTML = "";
  document.getElementById("payitemAlert").innerHTML = "";
  document.getElementById("payamountAlert").innerHTML = "";
  document.getElementById("id_ptpay-staffname").classList.remove('is-invalid');
  document.getElementById("id_datepay").classList.remove('is-invalid');
}




//cash log verify button start


document.getElementById("verifyClog").onclick=results;

    function results() {

//remove all previous alerts first
clogAlertRemover();

var onecval = nullTester(document.getElementById('id_onec').value);
var fivecval = nullTester(document.getElementById('id_fivec').value);
var tencval = nullTester(document.getElementById('id_tenc').value);
var twfvcval = nullTester(document.getElementById('id_twfvc').value);
var onedval = nullTester(document.getElementById('id_oned').value);
var twodval = nullTester(document.getElementById('id_twod').value);
var fivedval = nullTester(document.getElementById('id_fived').value);
var tendval = nullTester(document.getElementById('id_tend').value);
var twntdval = nullTester(document.getElementById('id_twntd').value);
var shiftval;
var recountval;

if(document.getElementById('id_shifttime_0').checked == true){
  shiftval = 'Start of Shift';
}
if(document.getElementById('id_shifttime_1').checked == true){
  shiftval = 'End of Shift';
}


if (document.getElementById('id_recount').checked == true) {
  recountval = 'Recount: Yes';
}
else {
  recountval = 'Recount: No';
}


var validName = document.getElementById('id_cashlog-staffname').value;
var validDate = document.getElementById('id_entrydate').value;
var nameMessage = "";
var dateMessage = "";
var locMessage = "";
var shiftMessage = "";
var errorCounter = 0;

if (validName == null || validName == "" )  {
   nameMessage += "<font color='red'>Valid Name Required </font>";
   document.getElementById("id_cashlog-staffname").setAttribute('class', 'form-control is-invalid');
   document.getElementById("namealert").innerHTML = nameMessage;
   errorCounter += 1;

}

if (validDate == null || validDate == "" ) {
  dateMessage += "<font color='red'> Valid Date Required </font>";
   document.getElementById("id_entrydate").setAttribute('class', 'form-control is-invalid')
   document.getElementById("datealert").innerHTML = dateMessage;
   errorCounter += 1;

}

if (document.getElementById('id_cashlog-locname_0').checked == false && document.getElementById('id_cashlog-locname_1').checked ==false  && document.getElementById('id_cashlog-locname_2').checked == false && document.getElementById('id_cashlog-locname_3').checked == false && document.getElementById('id_cashlog-locname_4').checked == false) {
  locMessage += "<font color='red'> Location Required </font>";
  document.getElementById("localert").innerHTML = locMessage;
  errorCounter += 1;
}

if (document.getElementById('id_shifttime_0').checked == false && document.getElementById('id_shifttime_1').checked ==false) {
  shiftMessage += "<font color='red'>Time Required </font>";
  document.getElementById("shiftalert").innerHTML = shiftMessage;
  errorCounter += 1;
}




//if no error messages  following takes place


if (errorCounter == 0 ) {


$("#cModal").modal({backdrop: 'static', keyboard: false}) ;

// logic for showing values in the modal below

document.getElementById("test").innerHTML = "";



var para= document.createElement("div");
para.className = ('container')


var name = document.createTextNode('Name: '+ document.getElementById('id_cashlog-staffname').value);
var datepicker = document.createTextNode('Date: '+ document.getElementById('id_entrydate').value);
var shifttimejs = document.createTextNode(shiftval);
var recountjs = document.createTextNode(recountval);
var onec = document.createTextNode('0.01 x '+ onecval + ' = '+(parseFloat(onecval) * .01).toFixed(2));
var fivec = document.createTextNode('0.05 x '+ fivecval + ' = '+(parseFloat(fivecval) * .05).toFixed(2));
var tenc = document.createTextNode('0.1 x '+ tencval + ' = '+(parseFloat(tencval) * .1).toFixed(2));
var twfvc = document.createTextNode('0.25 x '+ twfvcval + ' = '+(parseFloat(twfvcval) * .25).toFixed(2));
var oned = document.createTextNode('1.00 x '+ onedval + ' = '+(parseFloat(onedval) * 1).toFixed(2));
var twod = document.createTextNode('2.00 x '+ twodval + ' = '+(parseFloat(twodval) * 2).toFixed(2));
var fived = document.createTextNode('5.00 x '+ fivedval + ' = '+(parseFloat(fivedval) * 5).toFixed(2));
var tend = document.createTextNode('10.00 x '+ tendval + ' = '+(parseFloat(tendval) * 10).toFixed(2));
var twntd = document.createTextNode('20.00 x '+ twntdval + ' = '+(parseFloat(twntdval) * 20).toFixed(2));
var totjs = parseFloat((onecval * .01)
  + (fivecval * .05)
  + (tencval * .1)
  + (twfvcval * .25)
  + (onedval * 1)
  + (twodval * 2)
  + (fivedval * 5)
  + (tendval * 10)
  + (twntdval * 20)).toFixed(2);

if (document.getElementById('id_cashlog-locname_0').checked) {
 loc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_0').value);
}
else if (document.getElementById('id_cashlog-locname_1').checked) {
 loc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_1').value);
}
 else if (document.getElementById('id_cashlog-locname_2').checked) {
 loc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_2').value);
}
else if (document.getElementById('id_cashlog-locname_3').checked) {
loc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_3').value);
}
else if (document.getElementById('id_cashlog-locname_4').checked) {
loc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_4').value);
}
else {
  loc = document.createTextNode('none');
}




para.appendChild(name);
para.appendChild(document.createElement("br"));
para.appendChild(datepicker);
para.appendChild(document.createElement("br"));
para.appendChild(loc);
para.appendChild(document.createElement("br"));
para.appendChild(shifttimejs);
para.appendChild(document.createElement("br"));
para.appendChild(recountjs);
para.appendChild(document.createElement("br"));
para.appendChild(onec);
para.appendChild(document.createElement("br"));
para.appendChild(fivec);
para.appendChild(document.createElement("br"));
para.appendChild(tenc);
para.appendChild(document.createElement("br"));
para.appendChild(twfvc);
para.appendChild(document.createElement("br"));
para.appendChild(oned);
para.appendChild(document.createElement("br"));
para.appendChild(twod);
para.appendChild(document.createElement("br"));
para.appendChild(fived);
para.appendChild(document.createElement("br"));
para.appendChild(tend);
para.appendChild(document.createElement("br"));
para.appendChild(twntd);
para.appendChild(document.createElement("br"));
para.appendChild(document.createTextNode('Total Cash: ' + totjs));
para.appendChild(document.createElement("div"));
document.getElementById("test").appendChild(para);
document.getElementById('submitClog').disabled = false;

document.getElementById('modalCloseClog').onclick = disableSubmitClog;

function disableSubmitClog() {
  document.getElementById('submitClog').disabled = true;
}





//showing value on modal


}

}


//cashlog reset button

function resetFormc(){
  setTimeout(function(){
  document.getElementById('cashlogform').reset();
  clogAlertRemover();

    }, 50);
  return true;
}


//patient pay verify button

document.getElementById("verifyPlog").onclick=ptpayresults;

    function ptpayresults() {

ptpayAlertRemover();
var validNamep = document.getElementById('id_ptpay-staffname').value;
var validDatep = document.getElementById('id_datepay').value;
var validPayitem = document.getElementById('id_payitem');
var validPaytype = document.getElementById('id_paytype');
var validBreakdown = document.getElementById('id_otherpay').value;
var validPayAmount = document.getElementById('id_amountpay').value;
var selectedPayitem = validPayitem.options[validPayitem.selectedIndex].text;
var selectedPaytype = validPaytype.options[validPaytype.selectedIndex].text;
var nameMessagep = "";
var dateMessagep = "";
var locMessagep = "";
var shiftMessagep = "";
var payitemMessage = "";
var payamountMessage = "";
var ptpayErrorCounter = 0;

if (validNamep == null || validNamep == "" )  {

   nameMessagep += "<font color='red'>Valid Name Required </font>";
   document.getElementById("id_ptpay-staffname").setAttribute('class', 'form-control is-invalid');
   document.getElementById("namealertp").innerHTML = nameMessagep;
   ptpayErrorCounter += 1;

}

if (validDatep == null || validDatep == "" ) {
  dateMessagep += "<font color='red'> Valid Date Required </font>";
   document.getElementById("id_datepay").setAttribute('class', 'form-control is-invalid')
   document.getElementById("datealertp").innerHTML = dateMessagep;
   ptpayErrorCounter += 1;
}

if (document.getElementById('id_ptpay-locname_0').checked == false && document.getElementById('id_ptpay-locname_1').checked ==false  && document.getElementById('id_ptpay-locname_2').checked == false && document.getElementById('id_ptpay-locname_3').checked == false && document.getElementById('id_ptpay-locname_4').checked == false) {
  locMessagep += "<font color='red'> Location Required </font>";
  document.getElementById("localertp").innerHTML = locMessagep;
  ptpayErrorCounter += 1;
}

//payment type validation error display

if ((selectedPayitem == 'None') && (validBreakdown == "" || validBreakdown == null)) {
  payitemMessage += "<font color='red'>Select a payment item or Enter a comment </font>";
  document.getElementById("payitemAlert").innerHTML = payitemMessage;
  ptpayErrorCounter += 1;
}

if ((validPayAmount == "") || (validPayAmount == null)) {
  payamountMessage += "<font color='red'>Enter payment amount </font>";
  document.getElementById("payamountAlert").innerHTML = payamountMessage;
  ptpayErrorCounter += 1;
}

//if no error messages  following takes place

if (ptpayErrorCounter == 0) {

$("#pModal").modal({backdrop: 'static', keyboard: false}) ;
// showing values on modal

document.getElementById("ptpayPreSubmission").innerHTML = "";

// logic for showing values in the modal below
var ptpayModal= document.createElement("div");
ptpayModal.className = ('container')


var ptpayName = document.createTextNode('Name:'+ document.getElementById('id_ptpay-staffname').value);
var ptpayDatepicker = document.createTextNode('Date: '+ document.getElementById('id_datepay').value);
var ptpayPatientName = document.createTextNode('Patient Name: '+ document.getElementById('id_ptnamepay').value);
var ptpayPatientID = document.createTextNode('Patient ID: '+ document.getElementById('id_ptidpay').value);
var ptpayPaymentItem = document.createTextNode('Payment Item: '+ selectedPayitem);
var ptpayBreakdown = document.createTextNode('Breakdown/Comment: '+ document.getElementById('id_otherpay').value);
var ptpayAmount = document.createTextNode('Payment Amount: '+ document.getElementById('id_amountpay').value);
var ptpayPaymentType = document.createTextNode('Payment Type: '+ selectedPaytype);


if (document.getElementById('id_ptpay-locname_0').checked) {
 ptpayLoc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_0').value);
}
else if (document.getElementById('id_ptpay-locname_1').checked) {
 ptpayLoc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_1').value);
}
 else if (document.getElementById('id_ptpay-locname_2').checked) {
 ptpayLoc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_2').value);
}
else if (document.getElementById('id_ptpay-locname_3').checked) {
ptpayLoc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_3').value);
}
else if (document.getElementById('id_ptpay-locname_4').checked) {
ptpayLoc = document.createTextNode('Location: ' + document.getElementById ('id_cashlog-locname_4').value);
}
else {
 ptpayLoc = document.createTextNode('none');
}


ptpayModal.appendChild(ptpayName);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayDatepicker);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayLoc);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayPatientName);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayPatientID);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayPaymentItem);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayPaymentType);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayBreakdown);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(ptpayAmount);
ptpayModal.appendChild(document.createElement("br"));
ptpayModal.appendChild(document.createElement("div"));
document.getElementById("ptpayPreSubmission").appendChild(ptpayModal);
document.getElementById('submitPlog').disabled = false;

document.getElementById('modalClosePlog').onclick = disableSubmitPlog;

function disableSubmitPlog() {
  document.getElementById('submitPlog').disabled = true;
}



}

}

//Patient Pay reset button
function resetFormp(){
  setTimeout(function(){
  document.getElementById('patientpayform').reset();
  ptpayAlertRemover();

    }, 50);
  return true;
}


