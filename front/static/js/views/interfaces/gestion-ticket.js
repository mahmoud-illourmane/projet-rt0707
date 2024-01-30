$(document).ready(function() {

    function getAllTicketsUser() {    
        $.ajax({
            url: '/api/get/tickets-user', 
            method: 'GET',
            dataType: 'json',                           
            success: function(response) {
                if(response.status == 200) {

                    // Affichage des tickets
                    $('#total-tickets').text(response.ticket_count);
                    var tickets = response.tickets;
                    if (tickets && response.ticket_count != 0) {
                        // Sélectionne le 'tbody' dans ton tableau
                        var tbody = $('.table-tickets tbody');
                        var body = $('.table-responsive');

                        // Vide le 'tbody' pour s'assurer qu'il n'y a pas de lignes précédentes
                        tbody.empty();

                        // Remplit le 'tbody' avec de nouvelles lignes pour chaque ticket
                        $.each(tickets, function(index, ticket) {
                            // Une nouvelle ligne pour chaque ticket
                            var row = `
                                <tr>
                                    <th scope="row">${ticket._id}</th>
                                    <td>${ticket.type}</td>
                                    <td>${ticket.etat}</td>
                                    <td>${ticket.date_achat}</td>
                                    <td>${ticket.validite}</td>
                                    <td>${ticket.nb_scannes}</td>
                                    <td>
                                        <button type="button" class="btn btn-sm btn-success btn-rounded" data-bs-toggle="modal" data-bs-target="#ticketModal${ticket._id}">
                                            Afficher
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
                                                        <div class="date-validite qr-modal">
                                                            <span class="material-icons">hourglass_bottom</span>
                                                            <h6>Date d'expiration : ${ticket.qr_code_info.validite}</h6>
                                                        </div>
                                                        <div class="type-ticket-badge qr-modal">
                                                            <span class="material-icons">token</span>
                                                            <h6>Type Ticket : ${ticket.qr_code_info.type}</h6>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            tbody.append(row);
                            body.append(modal_qrcode);
                        });
                    }else {
                        // Ligne pour indiquer aucun ticket
                        var row = `
                            <tr>
                                <th scope="row" class="text-center" colspan="7">Aucun Ticket</th>
                            </tr>
                        `;
                        var tbody = $('.table-tickets tbody');
                        tbody.append(row);
                    }

                    // Total badges achetés
                    $('#total-badges').text(response.badge_count);
                    var badges = response.badges;
                    if (badges && response.badge_count != 0) {
                        // Sélectionnez le 'tbody' dans votre tableau
                        var tbody = $('.table-badges tbody');
                        var body = $('.table-responsive');

                        // Videz le 'tbody' pour vous assurer qu'il n'y a pas de lignes précédentes
                        tbody.empty();
                    
                        // Remplissez le 'tbody' avec de nouvelles lignes pour chaque badge
                        $.each(badges, function(index, badge) {
                            // Une nouvelle ligne pour chaque badge
                            var row = `
                                <tr>
                                    <th scope="row">${badge._id}</th>
                                    <td>${badge.type}</td>
                                    <td>${badge.etat}</td>
                                    <td>${badge.date_achat}</td>
                                    <td>${badge.validite}</td>
                                    <td>${badge.nb_scannes}</td>
                                    <td>
                                        <button type="button" class="btn btn-sm btn-success btn-rounded" data-bs-toggle="modal" data-bs-target="#badgeModal${badge._id}">
                                            Afficher
                                        </button>
                                    </td>
                                </tr>
                            `;
                            // Le modal qui permet d'afficher le QR code pour chaque badge
                            var modal_qrcode = `
                                <div class="modal fade" id="badgeModal${badge._id}" tabindex="-1" aria-labelledby="badgeModalLabel${badge._id}" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-scrollable">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="badgeModalLabel">Détails du Badge</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <div class="modal-qrcode">
                                                    <div class="modal-qrcode-image">
                                                        <img src="data:image/png;base64,${badge.qr_code}" width="200"/>
                                                    </div>
                    
                                                    <div class="modal-qrcode-content">
                                                        <div class="qr-code-id qr-modal">
                                                            <span class="material-icons">widgets</span>
                                                            <h6>Identification : ${badge.qr_code_info.id}</h6>
                                                        </div>
                                                        <div class="date-creation qr-modal">
                                                            <span class="material-icons">calendar_month</span>
                                                            <h6>Date de création : ${badge.qr_code_info.date_achat}</h6>
                                                        </div>
                                                        <div class="date-validite qr-modal">
                                                            <span class="material-icons">hourglass_bottom</span>
                                                            <h6>Date d'expiration : ${badge.qr_code_info.validite}</h6>
                                                        </div>
                                                        <div class="type-ticket-badge qr-modal">
                                                            <span class="material-icons">token</span>
                                                            <h6>Type Badge : ${badge.qr_code_info.type}</h6>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            tbody.append(row);
                            body.append(modal_qrcode);
                        });
                    } else {
                        // Ligne pour indiquer aucun badge
                        var row = `
                            <tr>
                                <th scope="row" class="text-center" colspan="7">Aucun Badge</th>
                            </tr>
                        `;
                        var tbody = $('.table-badges tbody');
                        tbody.append(row);
                    }
                }
                else {
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
                showToastMessage(errorMessage, 'text-danger');
            },
            complete: function() {
                stopLoadingAnimation();
            }
        });
    } 

    getAllTicketsUser();
});