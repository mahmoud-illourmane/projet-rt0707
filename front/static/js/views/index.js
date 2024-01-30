$(document).ready(function() {

    function generalsInfosUser() {    
        $.ajax({
            url: 'api/get/generals-infos-user', 
            method: 'GET',
            dataType: 'json',                           
            success: function(response) {
                if(response.status == 200) {
                    // Total tickets achetés
                    $('#total-achat').text(response.ticket_count);

                    // Afficher le QRCODE du dernier Ticket Acheté
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
                                    <div class="date-validite qr-modal">
                                        <span class="material-icons">hourglass_bottom</span>
                                        <h6>Date d'expiration : ${ticketInfo.validite}</h6>
                                    </div>
                                    <div class="type-ticket-badge qr-modal">
                                        <span class="material-icons">token</span>
                                        <h6>Type Ticket : ${ticketInfo.type}</h6>
                                    </div>
                                </div>
                            </div>
                        `;
                        $('.qr-code-modal-index').append(elementHtml);
                    }else {
                        $('.qr-code-modal-index').append(`<span class="color_7">AUCUN QRCODE DISPONIBLE.</span>`);
                    }
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
});