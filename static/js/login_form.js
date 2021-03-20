const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});

const newtogglePassword = document.querySelector('#newtogglePassword');
const new_password = document.querySelector('#new_password');

newtogglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = new_password.getAttribute('type') === 'password' ? 'text' : 'password';
    new_password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});

