// var password_check = function() {
//   if (document.getElementById('password').value ===
//     document.getElementById('confirm_password').value) {
//     document.getElementById('message').style.color = 'green';
//     document.getElementById('message').innerHTML = 'matching';
//   } else {
//     document.getElementById('message').style.color = 'red';
//     document.getElementById('message').innerHTML = 'not matching';
//   }
// }
$('form').validate();

$('#password, #passwordConfirm').on('keyup', function() {
  if ($('#password').val() == $('#passwordConfirm').val()) {
    $('#message').html('Matching').css('color', 'green');
    $('#submit').prop('disabled', false);
  } else {
    $('#message').html('Not Matching').css('color', 'red');
    $('#submit').prop('disabled', true);
  }
});