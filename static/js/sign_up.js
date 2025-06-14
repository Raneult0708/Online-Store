document.addEventListener('DOMContentLoaded', function() {
    // Gestion de l'affichage des infos véhicule
    const roleSelect = document.getElementById('role');
    const vehiculeSection = document.getElementById('vehicule-section');
    
    roleSelect.addEventListener('change', function() {
        vehiculeSection.style.display = this.value === 'conducteur' ? 'block' : 'none';
    });

    // Prévisualisation de la photo
    document.getElementById('photo').addEventListener('change', function(e) {
        const reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('preview').src = event.target.result;
        };
        if(e.target.files[0]) reader.readAsDataURL(e.target.files[0]);
    });
});

// ...existing code...
document.getElementById('email').addEventListener('input', function() {
    const emailInput = this;
    const errorSpan = document.getElementById('email-error');
    if (emailInput.validity.valid) {
        errorSpan.style.display = 'none';
    } else {
        errorSpan.style.display = 'block';
    }
});
// ...existing code...
document.getElementById('numéro').addEventListener('input', function() {
    const phoneInput = this;
    const errorSpan = document.getElementById('phone-error');
    if (phoneInput.value.length === 10) {
        errorSpan.style.display = 'none';
    } else {
        errorSpan.style.display = 'block';
    }
});
// ...existing code...
document.getElementById('mot_de_passe').addEventListener('input', function() {
    const pwdInput = this;
    const errorSpan = document.getElementById('password-error');
    if (pwdInput.validity.valid) {
        errorSpan.style.display = 'none';
    } else {
        errorSpan.style.display = 'block';
    }
});
// ...existing code...
document.querySelector('.profil').style.display = 'none';
document.querySelector('.messages').style.display = 'none';
document.querySelector('.connect').style.display = 'none';
document.querySelector('.sign-up').style.display = 'none';
document.querySelector('.search-ride').style.display = 'none';
document.querySelector('.publish-ride').style.display = 'none';
document.querySelector('.ask-ride').style.display = 'none';