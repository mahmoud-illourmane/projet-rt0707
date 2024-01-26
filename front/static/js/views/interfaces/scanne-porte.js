$(document).ready(function() {

    /*== Gestion de l'input d'id d'un qrcode ==*/
        // Ciblez l'élément d'entrée (input)
        var inputElement = $('.form-control');
        
        // Ciblez le bouton "Soumettre"
        var submitButton = $('#button-addon2');
        
        // Désactivez le bouton au chargement de la page
        submitButton.prop('disabled', true);
        
        // Écoutez l'événement de saisie dans le champ texte
        inputElement.on('input', function() {
            // Vérifiez si la longueur du texte est d'au moins 10 caractères
            if ($(this).val().length >= 20) {
                // Si oui, activez le bouton
                submitButton.prop('disabled', false);
            } else {
                // Sinon, désactivez le bouton
                submitButton.prop('disabled', true);
            }
        });
    /*== END/Gestion de l'input d'id d'un qrcode ==*/

    function getAllTicketsUser() {    
        $.ajax({
            url: '/api/get/tickets-user', 
            method: 'GET',
            dataType: 'json',                           
            success: function(response) {
                if(response.status == 200) {
                    // Total tickets achetés
                    $('#total-ticket').text(response.ticket_count);

                    // Afficher le tableau des tickets
                    var tickets = response.tickets;
                    if (tickets) {
                        // Sélectionne le 'tbody' dans ton tableau
                        var tbody = $('.table tbody');

                        // Vide le 'tbody' pour s'assurer qu'il n'y a pas de lignes précédentes
                        tbody.empty();

                        // Remplit le 'tbody' avec de nouvelles lignes pour chaque ticket
                        $.each(tickets, function(index, ticket) {
                            // Une nouvelle ligne pour chaque ticket
                            var row = `
                                <tr>
                                    <th scope="row">${ticket._id}</th>
                                    <td>${ticket.date_achat}</td>
                                    <td>${ticket.validite}</td>
                                    <td>${ticket.nb_scannes}</td>
                                    <td>
                                        <button type="button" class="btn btn-sm btn-success btn-rounded" data-bs-toggle="modal" data-bs-target="#ticketModal${ticket._id}">
                                            Afficher
                                        </button>

                                        <button type="button" class="btn btn-sm btn-primary btn-rounded" data-ticket-choice=${ticket._id}>
                                            Scanner
                                        </button>
                                    </td>
                                </tr>
                            `;
                            // Le modal qui permet d'afficher le qrcode pour chaque ticket
                            var modal_qrcode = `
                                <div class="modal fade" id="ticketModal${ticket._id}" tabindex="-1" aria-labelledby="ticketModalLabel${ticket._id}" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-scrollable">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="ticketModalLabel">Détails du Ticket</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <div class="modal-qrcode">
                                                    <div class="modal-qrcode-image">
                                                        <img src="data:image/png;base64,${ticket.qr_code}" width="200"/>
                                                    </div>
                                            
                                                    <div class="modal-qrcode-content">
                                                        <div class="qr-code-id qr-modal">
                                                            <span class="material-icons">widgets</span>
                                                            <h6>Identification : ${ticket.qr_code_info.id}</h6>
                                                        </div>
                                                        <div class="date-creation qr-modal">
                                                            <span class="material-icons">calendar_month</span>
                                                            <h6>Date de création : ${ticket.qr_code_info.date_achat}</h6>
                                                        </div>
                                                        <div class="type-ticket-badge qr-modal">
                                                            <span class="material-icons">token</span>
                                                            <h6>Type Ticket : ${ticket.qr_code_info.type}</h6>
                                                        </div>
                                                        <div class="date-validite qr-modal">
                                                            <span class="material-icons">hourglass_bottom</span>
                                                            <h6>Date d'expiration : ${ticket.qr_code_info.validite}</h6>
                                                        </div>
                                                        <div class="date-validite qr-modal">
                                                            <span class="material-icons">history</span>
                                                            <h6>Etat du ticket : ${ticket.qr_code_info.etat}</h6>
                                                        </div>
                                                        <div class="date-validite qr-modal">
                                                            <span class="material-icons">functions</span>
                                                            <h6>Nombre de scannes : ${ticket.qr_code_info.nb_scannes}</h6>
                                                        </div>
                                                    </div>
                    
                                                    <p>
                                                        N : Jamais utilisé
                                                        <br>
                                                        P : Périmé
                                                        <br>
                                                        V : En voyage
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            tbody.append(row);
                            $('body').append(modal_qrcode);
                        });
                    }else {
                        
                    }
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                var errorMessage = 'Erreur inconnue';
            
                // Vérifie si la réponse contient un code de statut et un message d'erreur personnalisé
                if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
                    switch (xhr.status) {
                        case 403:
                        case 405:
                        case 500:
                            errorMessage = xhr.responseJSON.error;
                        break;
                        default:
                            errorMessage = "Erreur HTTP " + xhr.status + ": " + xhr.responseJSON.error;
                    }
                } else if (textStatus !== 'error') {
                    errorMessage = textStatus;
                } else if (errorThrown) {
                    errorMessage = errorThrown;
                }
                console.log(errorMessage);
                showToastMessage(errorMessage, 'text-danger');
            },
            complete: function() {
                stopLoadingAnimation();
            }
        });
    } 

    getAllTicketsUser();

    // Écoute l'événement de clic sur le bouton "Choisir" en utilisant la délégation d'événements
    $(document).on('click', '.btn[data-ticket-choice]', function() {
        console.log('bouton cliqué');
        // Récupérez l'ID du ticket depuis l'attribut "data-ticket-choice"
        var ticketId = $(this).data('ticket-choice');

        // Mettez cet ID dans l'input
        inputElement.val(ticketId);

        // Vérifiez à nouveau la longueur du texte
        if (inputElement.val().length >= 20) {
            // Si la longueur est suffisante, activez le bouton
            submitButton.prop('disabled', false);
        } else {
            // Sinon, désactivez le bouton
            submitButton.prop('disabled', true);
        }
    });
});