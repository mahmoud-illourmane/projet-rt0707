$(document).ready(function() {

    function generalsInfosUser() {    

        $.ajax({
            url: '/api/admin/get/all-users', 
            method: 'GET',
            dataType: 'json',                           
            success: function(response) {
                if(response.status == 200) {
                    var users = response.users;
                    if (users && users.length > 0) {
                        // Sélectionnez le 'tbody' dans votre tableau Bootstrap
                        var tbody = $('.table-tickets-badges-users tbody');
                        var body = $('.container');

                        // Videz le 'tbody' pour vous assurer qu'il n'y a pas de lignes précédentes
                        tbody.empty();
                    
                        // Boucle à travers chaque utilisateur
                        $.each(users, function(index, user) {
                            // Une nouvelle ligne pour chaque utilisateur
                            var row = `
                                <tr>
                                    <td>${user.firstName}</td>
                                    <td>${user.tickets.total_tickets}</td>
                                    <td>${user.tickets.N_tickets}</td>
                                    <td>${user.tickets.V_tickets}</td>
                                    <td>${user.tickets.P_tickets}</td>
                                    <td>${user.badges.total_badges}</td>
                                    <td>${user.badges.N_badges}</td>
                                    <td>${user.badges.V_badges}</td>
                                    <td>${user.badges.P_badges}</td>
                                    <td>
                                        <a type="button" class="material-icons color_7" data-bs-toggle="modal" data-bs-target="#modalDeleteUser${user._id}">
                                            delete
                                        </a>
                                    </td>
                                </tr>
                                
                            `;

                            // Le modal qui permet de confirmer la suppression d'un utilisateur
                            var modal_qrcode = `
                                <!-- Modal Confirm delete-->
                                <div class="modal fade" id="modalDeleteUser${user._id}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="modalDeleteUser${user._id}" aria-hidden="true">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h3 class="modal-title fs-5">Confirmer la suppression du compte</h3>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
        
                                            <div class="modal-body text-center">
                                                <p>
                                                    <strong>Cette action est irréversible.</strong>
                                                </p>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                                <button type="submit" class="btn btn-danger btn-confirm-delete-account d-flex gap-2" data-user-id="${user._id}">
                                                    <span class="material-icons color_6">delete</span>
                                                    Supprimer Ce Compte
                                                </button>
                                            </div>
                                        </div>
                                    </div>                        
                                </div>
                            `;
                            tbody.append(row);
                            body.append(modal_qrcode);
                        });
                    }
                    else {
                        var row = `
                            <tr>
                                <th scope="row" class="text-center" colspan="10">Aucun Utilisateur</th>
                            </tr>
                        `;
                        var tbody = $('.table-tickets-badges-users tbody');
                        tbody.append(row);
                    }
                }else {
                    showToastMessage(response.error, "text-danger");
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                var errorMessage = 'Erreur inconnue';
    
                // Vérifie si la réponse est du JSON
                if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (xhr.status) {
                    // Si la réponse n'est pas du JSON, utilise le statut HTTP
                    errorMessage = "Erreur HTTP " + xhr.status + ": " + (errorThrown ? errorThrown : "Erreur inconnue");
                } else if (textStatus !== 'error') {
                    // Erreur avec un texte d'état fourni par jQuery
                    errorMessage = textStatus;
                } else if (errorThrown) {
                    // Message d'erreur par défaut fourni par le navigateur
                    errorMessage = errorThrown;
                }
    
                console.log(errorMessage);
            },
            complete: function() {
                stopLoadingAnimation();
            }
        });
    } 

    generalsInfosUser();

    // Un écouteur d'événement pour gérer le clic sur le bouton de suppression
    $(document).on('click', '.btn-confirm-delete-account', function(event) {
        event.preventDefault(); // Empêcher la soumission du formulaire

        // Récupérer l'élément du bouton de suppression
        var deleteButton = $(this);

        // Afficher le spinner et désactiver le bouton
        deleteButton.prop('disabled', true).prepend('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ');

        // Préparer les données à envoyer
        var userId = deleteButton.data("user-id");
        var donnees = {
            user_id: userId
        };

        // Envoi de la requête AJAX avec les données préparées
        $.ajax({
            url: '/api/admin/delete/account',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(donnees),
            dataType: 'json',
            success: function(response) {
                if(response.status == 200) {
                    showToastMessage(response.message, 'text-success');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                var errorMessage = 'Erreur inconnue';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (xhr.status) {
                    errorMessage = "Erreur HTTP " + xhr.status + ": " + errorThrown || "Erreur inconnue";
                } else {
                    errorMessage = textStatus || errorThrown;
                }
                console.log(errorMessage);
                showToastMessage(errorMessage, 'text-danger');
            },
            complete: function() {
                // Enlever le spinner et réactiver le bouton
                deleteButton.prop('disabled', false);
                deleteButton.find('.spinner-border').remove();
                
                // Fermer le modal
                $('#modalDeleteUser' + userId).modal('hide');
                generalsInfosUser();
            }
        });

    });

});