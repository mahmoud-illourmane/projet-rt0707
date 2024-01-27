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
                    
                    if (tickets.length > 0) {
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
                                    <th scope="row">${ticket.type}</th>
                                    <th scope="row">${ticket.etat}</th>
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
                        // Ligne pour indiquer aucun ticket
                        var row = `
                            <tr>
                                <th scope="row" class="text-center" colspan="7">Aucun Ticket</th>
                            </tr>
                        `;
                        var tbody = $('.table tbody');
                        tbody.append(row);
                    }
                }
            },
            error: function(xhr, textStatus, errorThrown) {
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
                stopLoadingAnimation();
            }
        });
    } 

    getAllTicketsUser();

    // Écoute l'événement de clic sur le bouton "Choisir" en utilisant la délégation d'événements
    $(document).on('click', '.btn[data-ticket-choice]', function() {
        // Récupérez l'ID du ticket depuis l'attribut "data-ticket-choice"
        var ticketId = $(this).data('ticket-choice');

        scannerTicket(ticketId);

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

    function toggleClassesDoor() {
        $('.led').toggleClass('green green-light');
    }

    function scannerTicket(ticketId) {
        var ticket = {
            ticket_id: ticketId,
        };
        
        $.ajax({
            url: '/api/scanne/ticket',
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(ticket),
            success: function(response) {
                if(response.status == 200) {
                    showToastMessage(response.message, 'text-success');
                    $('.led').removeClass('red').addClass('green');

                    // Démarre le clignotement de la porte
                    const clignotement = setInterval(toggleClassesDoor, 500); // Alterne toutes les 500 millisecondes (0.5 seconde)
                    // Arrête le clignotement après 2 secondes
                    setTimeout(() => {
                        clearInterval(clignotement); // Arrête le clignotement
                        $('.led').removeClass('green green-light').addClass('red'); // Revenir à la classe "red"
                        showToastMessage("Porte fermée.", 'text-danger');
                    }, 3000);

                }else {
                    showToastMessage(response.error, 'text-danger');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
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
                // Afficher le message d'erreur dans l'interface utilisateur, par exemple via une alerte ou un toast
                // alert(errorMessage); // Exemple simple
                showToastMessage(errorMessage, 'text-danger'); // Supposons que c'est une fonction personnalisée pour afficher des messages
            },
            complete: function() {
                getAllTicketsUser();
            }
        });
    }
});