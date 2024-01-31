$(document).ready(function() {
    getAllTicketsUser();

    /*== Fonctions utilitaiers ==*/
        /**
        * Méthode qui affiche la petite animation de la porte
        */
        function toggleClassesDoor() {
            $('.led').toggleClass('green green-light');
        }

        /**
        * Fonction pour vérifier la longueur de l'input et activer/désactiver le bouton de soumission
        */
        function checkInputLengthAndToggleSubmitButton() {
            if (inputElement.val().length >= 20) {
                // Si la longueur est suffisante, activez le bouton
                submitButton.prop('disabled', false);
            } else {
                // Sinon, désactivez le bouton
                submitButton.prop('disabled', true);
            }
        }
    /*== END/Fonctions utilitaiers ==*/

    /*== Gestion de l'input id d'un qrcode ==*/
        // Cible l'élément d'entrée (input)
        var inputElement = $('.form-control');
        // Cible le bouton "Soumettre"
        var submitButton = $('#button-addon2');
        // Désactive le bouton au chargement de la page
        submitButton.prop('disabled', true);
        // Écoute l'événement de saisie dans le champ texte
        inputElement.on('input', function() {
            // Vérifie si la longueur du texte est d'au moins 20 caractères
            if ($(this).val().length >= 20) {
                // Si oui, active le bouton
                submitButton.prop('disabled', false);
            } else {
                // Sinon, désactive le bouton
                submitButton.prop('disabled', true);
            }
        });
    /*== END/Gestion de l'input d'id d'un qrcode ==*/

    /**
     * Cette méthode effectue une requête Ajax pour récupérer tous les tickets et badges
     * d'un utilisateur.
     * Elle remplit le tableau de manière dynamique.
     */
    function getAllTicketsUser() {    
        $.ajax({
            url: '/api/get/tickets-user', 
            method: 'GET',
            dataType: 'json',                           
            success: function(response) {
                if(response.status == 200) {
                    // Affichage des tickets sur le tableau des tickets
                    $('#total-tickets').text(response.ticket_count);
                    var tickets = response.tickets;
                    if (tickets.length > 0) {
                        // Sélectionne le 'tbody' dans ton tableau
                        var tbody = $('.table-tickets tbody');
                        // Vide le 'tbody' pour s'assurer qu'il n'y a pas de lignes précédentes
                        tbody.empty();
                        // Remplit le 'tbody' avec de nouvelles lignes pour chaque ticket
                        $.each(tickets, function(index, ticket) {
                            // Une nouvelle ligne pour chaque ticket
                            var rowClass = ticket.etat === "P" ? "table-danger" : ""; // Ajoute la classe 'table-danger' si l'état est "P"
                            var row = `
                                <tr class="${rowClass}">
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
                        
                                        <button type="button" class="btn btn-sm btn-primary btn-rounded btn-scan" data-choice-type=${ticket.type} data-titre-qrcode=${ticket.qr_code} data-ticket-choice=${ticket._id}>
                                            Scanner
                                        </button>
                                    </td>
                                </tr>
                            `;
                        
                            // Le modal qui permet d'afficher le qrcode pour chaque badge
                            var modal_qrcode = `
                                <div class="modal fade" id="ticketModal${ticket._id}" tabindex="-1" aria-labelledby="ticketModal${ticket._id}" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-scrollable">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="ticketModal">Détails du Badge</h5>
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
                                                        <div class="type-ticket qr-modal">
                                                            <span class="material-icons color_8">token</span>
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
                            $('body').append(modal_qrcode);
                        });
                        
                    }else {
                        var tbody = $('.table-tickets tbody');
                        tbody.empty();

                        // Ligne pour indiquer aucun ticket
                        var row = `
                            <tr>
                                <th scope="row" class="text-center" colspan="7">Aucun Ticket</th>
                            </tr>
                        `;
                        tbody.append(row);
                    }

                    // Affichage des badges sur le tableau des tickets
                    $('#total-badges').text(response.badge_count);
                    var badges = response.badges;
                    if (badges.length > 0) {
                        // Sélectionne le 'tbody' dans ton tableau
                        var tbody = $('.table-badges tbody');
                        // Vide le 'tbody' pour s'assurer qu'il n'y a pas de lignes précédentes
                        tbody.empty();
                        // Remplit le 'tbody' avec de nouvelles lignes pour chaque badge
                        $.each(badges, function(index, badge) {
                            // Une nouvelle ligne pour chaque badge
                            var rowClass = badge.etat === "P" ? "table-danger" : ""; // Ajoute la classe 'table-danger' si l'état est "P"
                            var row = `
                                <tr class="${rowClass}">
                                    <th scope="row">${badge._id}</th>
                                    <th scope="row">${badge.type}</th>
                                    <th scope="row">${badge.etat}</th>
                                    <td>${badge.date_achat}</td>
                                    <td>${badge.validite}</td>
                                    <td>${badge.nb_scannes}</td>
                                    <td>
                                        <button type="button" class="btn btn-sm btn-success btn-rounded" data-bs-toggle="modal" data-bs-target="#badgeModal${badge._id}">
                                            Afficher
                                        </button>

                                        <button type="button" class="btn btn-sm btn-primary btn-rounded btn-scan" data-choice-type=${badge.type} data-titre-qrCode=${badge.qr_code} data-badge-choice=${badge._id}>
                                            Scanner
                                        </button>
                                    </td>
                                </tr>
                            `;

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
                            $('body').append(modal_qrcode);
                        });
                    } else {
                        var tbody = $('.table-badges tbody');
                        tbody.empty();

                        // Ligne pour indiquer aucun badge
                        var row = `
                            <tr>
                                <th scope="row" class="text-center" colspan="7">Aucun Badge</th>
                            </tr>
                        `;
                        
                        tbody.append(row);
                    }
                }
                else {
                    showToastMessage(response.error, 'text-danger');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                var errorMessage = 'Erreur inconnue';
                // Vérifie si la réponse contient un code de statut et un message d'erreur personnalisé
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

    // Écoute l'événement de clic sur le bouton "Choisir" en utilisant la délégation d'événements
    $(document).on('click', '.btn[data-choice-type]', function() {
        // Désactive les boutons "scanner"
        $('.btn-scan').prop('disabled', true);
        // Récupère le QROCDE
        var qrCode = $(this).data('titre-qrcode');
        scannerPorte(qrCode);
    });
    
    /**
     * Fonction qui effectue une requête Ajax pour ouvrir une porte.
     *
     * @param {string} qrCodeBase64 - L'image du QRCode.
     */
    function scannerPorte(qrCodeBase64) {    
        // Données à envoyer dans la requête PUT
        var donnees = {
            qrCodeBase64: qrCodeBase64,
        };
            
        // Envoi de la requête AJAX avec les données préparées
        $.ajax({
            url: '/api/send/request/open/door',
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(donnees),
            dataType: 'json',
            success: function(response) {
                if(response.status == 200) {
                    showToastMessage(response.message, 'text-success');
                    $('.led').removeClass('red').addClass('green');

                    const clignotement = setInterval(toggleClassesDoor, 500); 

                    setTimeout(() => {
                        clearInterval(clignotement);
                        $('.led').removeClass('green green-light').addClass('red'); 
                        showToastMessage("Porte fermée.", 'text-danger');
                    }, 3000);
                }else {
                    showToastMessage(response.error, 'text-danger');
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
                getAllTicketsUser();
                console.log('Requête complétée');
                $('.btn-scan').prop('disabled', false);
            }
        });
    }

    /**
     * Fonction qui effectue une requête Ajax pour ouvrir une porte, lorsque il s'agit d'un ticket.
     *
     * @param {string} ticketId - L'identifiant du ticket.
     */
    // function scannerTicket(ticketId) {
    //     var ticket = {
    //         ticket_id: ticketId,
    //     };
        
    //     $.ajax({
    //         url: '/api/scanne/ticket',
    //         type: 'PUT',
    //         contentType: 'application/json',
    //         data: JSON.stringify(ticket),
    //         success: function(response) {
    //             if(response.status == 200) {
    //                 showToastMessage(response.message, 'text-success');
    //                 $('.led').removeClass('red').addClass('green');

    //                 // Démarre le clignotement de la porte
    //                 const clignotement = setInterval(toggleClassesDoor, 500); // Alterne toutes les 500 millisecondes (0.5 seconde)
    //                 // Arrête le clignotement après 3 secondes
    //                 setTimeout(() => {
    //                     clearInterval(clignotement); // Arrête le clignotement
    //                     $('.led').removeClass('green green-light').addClass('red'); // Revenir à la classe "red"
    //                     showToastMessage("Porte fermée.", 'text-danger');
    //                 }, 3000);

    //             }else {
    //                 showToastMessage(response.error, 'text-danger');
    //             }
    //         },
    //         error: function(xhr, textStatus, errorThrown) {
    //             var errorMessage = 'Erreur inconnue';
    //             if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
    //                 errorMessage = xhr.responseJSON.error;
    //             } else if (textStatus !== 'error') {
    //                 errorMessage = 'Erreur AJAX: ' + textStatus;
    //             } else if (errorThrown) {
    //                 errorMessage = 'Erreur exceptionnelle: ' + errorThrown;
    //             }
    //             console.log(errorMessage);
    //             showToastMessage(errorMessage, 'text-danger');
    //         },
    //         complete: function() {
    //             getAllTicketsUser();
    //         }
    //     });
    // }

    /**
     * Fonction qui effectue une requête Ajax pour ouvrir une porte, lorsque il s'agit d'un badge.
     *
     * @param {string} ticketId - L'identifiant du ticket.
     */
    // function scannerBadge(badgeId) {
    //     var badge = {
    //         badge_id: badgeId,
    //     };
        
    //     $.ajax({
    //         url: '/api/scanne/badge',
    //         type: 'PUT',
    //         contentType: 'application/json',
    //         data: JSON.stringify(badge),
    //         success: function(response) {
    //             if(response.status == 200) {
    //                 showToastMessage(response.message, 'text-success');
    //                 $('.led').removeClass('red').addClass('green');

    //                 const clignotement = setInterval(toggleClassesDoor, 500); 

    //                 setTimeout(() => {
    //                     clearInterval(clignotement);
    //                     $('.led').removeClass('green green-light').addClass('red'); 
    //                     showToastMessage("Porte fermée.", 'text-danger');
    //                 }, 3000);

    //             }else {
    //                 showToastMessage(response.error, 'text-danger');
    //             }
    //         },
    //         error: function(xhr, textStatus, errorThrown) {
    //             var errorMessage = 'Erreur inconnue';
    //             if (xhr.status && xhr.responseJSON && xhr.responseJSON.error) {
    //                 errorMessage = xhr.responseJSON.error;
    //             } else if (textStatus !== 'error') {
    //                 errorMessage = 'Erreur AJAX: ' + textStatus;
    //             } else if (errorThrown) {
    //                 errorMessage = 'Erreur exceptionnelle: ' + errorThrown;
    //             }
    //             console.log(errorMessage);
    //             showToastMessage(errorMessage, 'text-danger'); 
    //         },
    //         complete: function() {
    //             getAllTicketsUser();
    //         }
    //     });
    // }
});

