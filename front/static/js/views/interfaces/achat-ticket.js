$(document).ready(function() {

    /**
     * Gestionnaire d'événements pour le formulaire d'achat de tickets.
     */
    $('#purchase-form').submit(function(event) {
        event.preventDefault(); // Empêche la soumission standard du formulaire

        var selectType = {
            'selectType': $('[name="selectType"]').val()
        };

        $.ajax({
            url: '/api/purchase',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(selectType),
            dataType: 'json',
            success: function(response) {
                if(response.status == 201) {
                    showToastMessage(response.message, 'text-success');
                    
                    // Création de la balise img avec la source basée sur la chaîne base64 de la réponse
                    var element = `
                        <div class="qr-code-img">
                            <img src="data:image/png;base64,${response.qr_code_base64}" width="200"/>
                        </div>
                
                        <div class="qr-code-infos">
                            <div class="qr-code-id">
                                <span class="material-icons">widgets</span>
                                <h6>Identification : ${response.id}</h6>
                            </div>
                            <div class="date-creation">
                                <span class="material-icons">calendar_month</span>
                                <h6>Date de création : ${response.date_achat}</h6>
                            </div>
                            <div class="type-ticket-badge">
                                <span class="material-icons">token</span>
                                <h6>Type Ticket : ${response.type}</h6>
                            </div>
                            <div class="date-validite">
                                <span class="material-icons">hourglass_bottom</span>
                                <h6>Date d'expiration : ${response.validite}</h6>
                            </div>
                        </div>
                        
                    `;
                    // Ajout de l'élément img à la balise avec la classe "qr-code"
                    $('.qr-code').append(element);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                var errorMessage = 'Erreur inconnue';
            
                // Vérifie si la réponse contient un code de statut et un message d'erreur personnalisé
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
            
                showToastMessage(errorMessage, 'text-danger');
            },                      
            complete: function() {
                $('#purchase-form').trigger('reset');
                console.log('Requête complétée');
            }
        });
        
    });
});
