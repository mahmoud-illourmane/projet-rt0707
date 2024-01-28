

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

// Toats IDs
var liveToastMsgServer = $('#liveToastMsgServer');                      
var liveToastMsgServerContent = $('#liveToastMsgServerContent');      

/**
* Affiche un message toast de bootstrap.
*
* @param {string} message - Le message à afficher dans le toast.
* @param {string} cssClass - La classe CSS à appliquer au toast pour le style personnalisé.
*/
function showToastMessage(message, cssClass) {
    // Sélectionne l'élément .toast-body dans le toast
    var toastBody = liveToastMsgServer.find('.toast-body');
    
    // Définit le texte du message
    toastBody.text(message);
    
    // Supprime toutes les classes de l'élément toast-body et ajoute la classe de style personnalisée
    toastBody.removeClass().addClass('toast-body ' + cssClass);
    
    // Affiche le toast
    liveToastMsgServer.toast('show');
}


$(document).ready(function(){
    stopLoadingAnimation();

    /*== UX ==*/
        /*== Gestion des collapses qui affiche les menus disponible ==*/
            $('.settings-items [data-bs-toggle="collapse"]').on('click', function(){
                var target = $(this).data('bs-target');
                $('.settings-items-content .collapse').not(target).collapse('hide');
            });
        /*== END/Gestion des collapses qui affiche les menus disponible ==*/

        /*== Gestionnaire d'événements au clic sur tous les éléments ayant la classe "setting-item-div" ==*/
            $('.setting-item-div').click(function() {
                $('.setting-item-div').removeClass('setting-active');
                $(this).addClass('setting-active');
            });
        /*== END/Gestionnaire d'événements au clic sur tous les éléments ayant la classe "setting-item-div" ==*/
    /*== UX ==*/

    /*== Gestion de la modification du mot de passe ==*/
            
        // Gestionnaire d'événement qui permet d'afficher le contenu du mot de passe
        $(".showPasswordBtn").click(function() {
            // Trouve le champ de mot de passe associé dans le même groupe d'entrée
            var passwordField = $(this).closest('.input-group').find('.password-field');
            var type = passwordField.attr('type'); // Récupère le type de l'input
        
            // Basculer entre le type 'password' et 'text'
            if (type === 'password') {
                passwordField.attr('type', 'text');
                $(this).text('visibility_off');
            } else {
                passwordField.attr('type', 'password');
                $(this).text('visibility');
            }
        });
    
        // Password rules
        const uppercaseRegex = /[A-Z]/;
        const lowercaseRegex = /[a-z]/;
        const digitRegex = /[0-9]/;
        const specialCharRegex = /[#?!@$%^&*-]/;
        const lengthRegex = /^.{6,}$/;

        // Le champ du nouveau mot de passe
        var oldPassword = $("#oldPassword");   
        var newPassword = $("#newPassword");   
        var confirmPassword = $("#confirmPassword")

        // Les balises html
        const uppercaseRule = $("#uppercaseRule");
        const lowercaseRule = $("#lowercaseRule");
        const digitRule = $("#digitRule");
        const specialCharRule = $("#specialCharRule");
        const lengthRule = $("#lengthRule");

        newPassword.on("input", function() {
            var password = $(this).val();

            uppercaseRule.css("color", uppercaseRegex.test(password) ? "green" : "red");
            lowercaseRule.css("color", lowercaseRegex.test(password) ? "green" : "red");
            digitRule.css("color", digitRegex.test(password) ? "green" : "red");
            specialCharRule.css("color", specialCharRegex.test(password) ? "green" : "red");
            lengthRule.css("color", lengthRegex.test(password) ? "green" : "red");
        });

        // Initialement je désactive le bouton de soumission
        $('#btnSubmitPasswordUpdate').prop('disabled', true);

        // Fonction pour vérifier si le mot de passe est valide
        function isPasswordValid(password) {
            return (
                uppercaseRegex.test(password) &&
                lowercaseRegex.test(password) &&
                digitRegex.test(password) &&
                specialCharRegex.test(password) &&
                lengthRegex.test(password)
            );
        }

        // Fonction pour activer ou désactiver le bouton de soumission
        function updateSubmitButtonState() {
            var oldPasswordValue = oldPassword.val();
            var newPasswordValue = newPassword.val();
            var confirmPasswordValue = confirmPassword.val();
    
            // Vérifie si tous les champs sont remplis et si les mots de passe correspondent
            if (newPasswordValue && confirmPasswordValue && oldPasswordValue && newPasswordValue === confirmPasswordValue && isPasswordValid(newPasswordValue)) {
                $('#btnSubmitPasswordUpdate').prop('disabled', false);
            } else {
                $('#btnSubmitPasswordUpdate').prop('disabled', true);
            }
        }

        // Appeler la fonction pour vérifier l'état du bouton lorsqu'un champ est modifié
        $(".password-field").on("input", function() {
            updateSubmitButtonState();
        });

        $('#btnSubmitPasswordUpdate').click(function(){
            if(!$('#btnSubmitPasswordUpdate').prop('disabled')) {
                $("#formulaire").submit(function(e) {
                    $('#btnSubmitPasswordUpdate').prop('disabled', true);
                    $('#spinner').removeClass('d-none');
                    e.preventDefault();
                
                    // Convertir les données du formulaire en objet JavaScript
                    var dataObj = {};
                    $.each($(this).serializeArray(), function(i, field) {
                        dataObj[field.name] = field.value;
                    });
                    dataObj["operation_id"] = 3;

                    // Convertir l'objet JavaScript en chaîne JSON
                    var jsonData = JSON.stringify(dataObj);
                
                    $.ajax({
                        url: '/api/settings',
                        type: 'PUT',
                        dataType: 'json',
                        contentType: 'application/json',
                        data: jsonData,
                        success: function(response) {
                            if(response.status == 200) {
                                showToastMessage(response.message, "text-success");
                            }
                            else {
                                showToastMessage(response.error, "text-danger");
                            }
                            $('#formulaire')[0].reset();
                        },
                        error: function(xhr) {
                            $('#formulaire')[0].reset();
                            
                            var errorMessage = 'Erreur inconnue';
                            // Vérifier si la réponse contient un code de statut et un message d'erreur personnalisé
                            if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
                                errorMessage = xhr.responseJSON.error;
                            } else if (textStatus !== 'error') {
                                // Erreur avec un texte d'état fourni par jQuery (par exemple, "timeout", "abort", etc.)
                                errorMessage = 'Erreur AJAX: ' + textStatus;
                            } else if (errorThrown) {
                                // Message d'erreur par défaut fourni par le navigateur
                                errorMessage = 'Erreur exceptionnelle: ' + errorThrown;
                            }
                            console.log(errorMessage);
                            showToastMessage(errorMessage, 'text-danger'); 
                        },
                        complete: function() {
                            $('#spinner').addClass('d-none');
                        }
                    });
                });
                
            }
        });

    /*== END/Gestion de la modification du mot de passe ==*/

    /*== Modifications des NOM & EMAIL ==*/
        var originData = null;

        // Désactive tous les champs input dans l'onglet "compte"
        $('.info-input').prop('disabled', true);
        // Désactive tous les butons qui permettent de confirmer une modification
        $('.confirm-operation').prop('disabled', true);
        // Ajoute la couleur grise à tous ces butons
        $('.confirm-operation').addClass('color_8');

        // Lorsque l'utilisateur clique sur le bouton "edit"
        $('.edit-operation').click(function(){
            var input = null;
            var confirm_button = null;

            // Je désactive le bouton sur lequel l'utilisateur a cliqué
            $(this).prop('disabled', true);
            // J'enlève la couleur noir du bouton et je met une couleur grise
            $(this).removeClass('color_3').addClass('color_8');
            
            // Trouve le div parent '.user-info' le plus proche
            // Ensuite l'input à l'intérieur
            input = $(this).closest('.user-info').find('.info-input');

            // Trouve le button qui confirm la modification de l'input
            confirm_button = $(this).closest('.user-info').find('.confirm-operation');
            // Je réactive le bouton qui permet de confirmer la modification
            confirm_button.prop('disabled', false);
            // Je lui met une couleur verte pour le signaler
            confirm_button.removeClass('color_8').addClass('color_11');

            // Je stock la valeur originelle de l'input
            originData = input.val();

            // Activer l'input pour modification
            input.prop('disabled', false);
        });

        // Lorsque l'utilisateur clique sur l'icône "done"
        $('.confirm-operation').click(function(){    
            // Vérifie si le bouton est désactivé
            if ($(this).prop('disabled')) {
                return;
            }

            var input = null;               // La valeur saisi par l'utilisateur
            var inputName = null;           // Le nom du champ choisi par l'utilisateur pour modification

            var edit_button = null;
            var jsonData = {}; // 2 : last_name, 4 : email

            // Lorsque l'utilisateur clique sur le bouton pour confirmer le changement
            // J'enlève la couleur verte et je remet sa couleur initial grise      
            $(this).removeClass('color_11').addClass('color_8');
            // Je désactive de nouveau le bouton
            $(this).prop('disabled', true);

            // Trouver le div parent '.user-info' le plus proche
            // Ensuite l'input à l'intérieur
            input = $(this).closest('.user-info').find('.info-input');
            // Récupérer la valeur du name de i'input séléctionné pour forger la requête Ajax
            inputName = input.attr('name');

            // Trouve le button qui permet de modifier l'input
            edit_button = $(this).closest('.user-info').find('.edit-operation');
            // Je le désactive pour empecher un deuxième clique inutile
            edit_button.prop('disabled', false).removeClass('color_8').addClass('color_3');

            // Vérification que la donnée saisie ne soit pas identique à l'originale
            if(input.val() == originData || (input.val() == originData) ) {
                showToastMessage("Aucune modification n'a été apporté", "text-success");
                input.prop('disabled', true);
                $('.phone-indicatif').prop('disabled', true);
                return;
            }
            
            // Je forge la requête Ajax avec l'id du traitement adéquat
            switch (inputName) {
                case 'last_name':
                    jsonData.operation_id = 1;
                    jsonData.data = input.val();
                break;

                case 'email':
                    jsonData.operation_id = 2;
                    jsonData.data = input.val();
                break;
                default:
                    showToastMessage("Une erreur est survenue lors de votre modification.", "text-danger");
                    return;
            }
           
            $.ajax({
                url: '/api/settings',
                type: 'PUT',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(jsonData),
                success: function(response) {
                    if(response.status == 200) {
                        showToastMessage(response.message, "text-success");
                    }
                    else {
                        showToastMessage(response.error, "text-danger");
                    }
                },
                error: function(xhr) {
                    var errorMessage = 'Erreur inconnue';
                    if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
                        errorMessage = xhr.responseJSON.error;
                    } else if (textStatus !== 'error') {
                        errorMessage = 'Erreur AJAX: ' + textStatus;
                    } else if (errorThrown) {
                        errorMessage = 'Erreur exceptionnelle: ' + errorThrown;
                    }
                    console.log(errorMessage);
                    showToastMessage(errorMessage, 'text-danger');
                },
                complete: function() {
                    if (!$(this).prop('disabled')) {
                        // Désactive l'input après modification
                        input.prop('disabled', true);
                    }
                }
            });    
        });
    /*== END/Modifications des NOM & EMAIL ==*/


    /*== Gestion du bouton suppression du comtpe ==*/
        $('#deleteAccountForm').submit(function(){ 
            $('.btn-confirm-delete-account').prop('disabled', true);
        });
    /*== END/Gestion du bouton suppression du comtpe ==*/
});
