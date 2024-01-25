$(document).ready(function() {

    function generalsInfosUser() {    
        $.ajax({
            url: 'api/get/generals-infos-user', 
            method: 'GET',
            dataType: 'json',                           
            success: function(response) {
                if(response.status == 200) {
                    $('#total-achat').text(response.ticket_count);
                    var lastTicket = response.last_ticket_qrcode;
                    if (lastTicket) {
                        var qrCodeBase64 = response.last_ticket_qrcode.qr_code_base64;
                        var ticketInfo = lastTicket.ticket_info;
                        
                        let elementHtml = `
                            <div class="modal-qrcode">
                                <div class="modal-qrcode-image">
                                    <img src="data:image/png;base64,${qrCodeBase64}" width="200"/>
                                </div>
                        
                                <div class="modal-qrcode-content">
                                    <div class="qr-code-id qr-modal">
                                        <span class="material-icons">widgets</span>
                                        <h6>Identification : ${ticketInfo.id}</h6>
                                    </div>
                                    <div class="date-creation qr-modal">
                                        <span class="material-icons">calendar_month</span>
                                        <h6>Date de création : ${ticketInfo.date_achat}</h6>
                                    </div>
                                    <div class="type-ticket-badge qr-modal">
                                        <span class="material-icons">token</span>
                                        <h6>Type Ticket : ${ticketInfo.type}</h6>
                                    </div>
                                    <div class="date-validite qr-modal">
                                        <span class="material-icons">hourglass_bottom</span>
                                        <h6>Date d'expiration : ${ticketInfo.validite}</h6>
                                    </div>
                                    <div class="date-validite qr-modal">
                                        <span class="material-icons">history</span>
                                        <h6>Etat du ticket : ${ticketInfo.etat}</h6>
                                    </div>
                                    <div class="date-validite qr-modal">
                                        <span class="material-icons">functions</span>
                                        <h6>Nombre de scannes : ${ticketInfo.nb_scannes}</h6>
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
                        `;
                        $('.qr-code-modal-index').append(elementHtml);
                    }
                    else {
                        $('.qr-code-modal-index').append(`<span class="color_7">AUCUN QRCODE DISPONIBLE.</span>`);
                    }
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                var errorMessage = 'Erreur inconnue';
            
                // Vérifier si la réponse contient un code de statut et un message d'erreur personnalisé
                if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
                    switch (xhr.status) {
                        case 400:
                        case 401:
                        case 403:
                        case 404:
                        case 500:
                            // Utilise le message d'erreur personnalisé du serveur
                            errorMessage = xhr.responseJSON.error;
                            break;
                        default:
                            errorMessage = "Erreur HTTP " + xhr.status + ": " + xhr.responseJSON.error;
                    }
                } else if (textStatus !== 'error') {
                    // Erreur avec un texte d'état fourni par jQuery (par exemple, "timeout", "abort", etc.)
                    errorMessage = textStatus;
                } else if (errorThrown) {
                    // Message d'erreur par défaut fourni par le navigateur
                    errorMessage = errorThrown;
                }
                
                console.log(errorMessage);
                showToastMessage(errorMessage, 'text-danger');
            },
            complete: function() {
                console.log('Requête complétée');
            }
        });
    } 

    generalsInfosUser();
});