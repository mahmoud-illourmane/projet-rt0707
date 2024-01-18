/**
 | 
 |  This file containt all JS code for the UI/UX personnalisation.
 |  AUTHOR: MAHMOUD ILLOURMANE
 |  DATE: 01-18-24 US DATE
 | 
*/

function topFunction() {
    $('body,html').animate({scrollTop: 0}, 800);
    return false;
}

/**
 * Cette méthode permet d'arrêter l'animation de préchargement de la page.
 */
function stopLoadingAnimation() {
    $('#loading-animation').fadeOut(200);
    $('.body').fadeIn(200);
}

/*== Toast message ==*/
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

    /**
     * Ferme le toast de message de la part du serveur.
     */
    function closeToastServerMsg() {
        // Utilise la méthode 'toast' pour masquer le toast de message de la part du serveur
        liveToastMsgServer.toast('hide');
    }
/*== END/Toast message ==*/

/*== Mode swticher ==*/
    /**
     * Cette fonction met à jour l'affichage des icônes en fonction du thème spécifié.
     *
     * @param {string} theme - Le thème actuel, généralement une classe CSS.
     */
    function updateIcons(theme) {
        // Vérifie si le thème contient la classe 'dark-mode'
        if (theme.includes('dark-mode')) {
            // Si le thème est en mode sombre, affiche les icônes sombres et masque les icônes claires
            $('.dark-mode-icon').show();
            $('.light-mode-icon').hide();
        } else {
            // Si le thème n'est pas en mode sombre, affiche les icônes claires et masque les icônes sombres
            $('.light-mode-icon').show();
            $('.dark-mode-icon').hide();
        }
    }     

    /**
     * Cette fonction crée un cookie avec le nom, la valeur et une durée d'expiration spécifiés.
     *
     * @param {string} name - Le nom du cookie à créer.
     * @param {string} value - La valeur à associer au cookie.
     * @param {number} days - Le nombre de jours avant que le cookie n'expire (0 pour session).
     */
    function createCookie(name, value, days) {
        // Chaîne pour stocker l'expiration du cookie
        var expires = "";

        // Si des jours sont spécifiés, calcule la date d'expiration
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }

        // Crée le cookie en utilisant le nom, la valeur, l'expiration et le chemin "/"
        document.cookie = name + "=" + value + expires + "; path=/";
    }       
        
    /**
     * Cette fonction récupère la valeur d'un cookie en fonction de son nom.
     *
     * @param {string} name - Le nom du cookie que je souhaite récupérer.
     * @returns {string|null} La valeur du cookie ou null si le cookie n'existe pas.
     */
    function getCookie(name) {
        // Récupère la valeur de tous les cookies
        var dc = document.cookie;

        // Préfixe du cookie à rechercher
        var prefix = name + "=";

        // Recherche du cookie dans la chaîne de cookies
        var begin = dc.indexOf("; " + prefix);

        // Si le cookie n'a pas été trouvé avec "; " comme préfixe, je recherche le début sans "; "
        if (begin == -1) {
            begin = dc.indexOf(prefix);

            // Si le cookie n'a pas été trouvé du tout, renvoye null
            if (begin != 0) return null;
        } else {
            // Si le cookie a été trouvé avec "; " comme préfixe, ajuste le point de départ
            begin += 2;

            // Recherche de la fin du cookie
            var end = document.cookie.indexOf(";", begin);

            // Si la fin du cookie n'est pas trouvée, prendre la fin de la chaîne de cookies
            if (end == -1) {
                end = dc.length;
            }
        }

        // Récupère la valeur du cookie, la décode et la renvoie
        return decodeURI(dc.substring(begin + prefix.length, end));
    }
/*== END/Mode swticher ==*/

$(document).on("DOMContentLoaded", function() {       
    $("#return_back").click(function() {
        history.back();
    });
    
    /*== Bootstrap validation forms ==*/
        // TODO
    /*== END/Bootstrap validation forms ==*/

    /*== Switch Modes DARK/LIGHT ==*/
        // Variables
        var savedTheme = getCookie("theme");
        var cssBasePath = '/static/css/ux-ui/';

        $('.dark-mode-icon').hide();

        $('#mode-switcher').click(function() {
            var currentTheme = $('#theme-style').attr('href');
            var newTheme = currentTheme.includes('dark-mode') ? 'light-mode/style.css' : 'dark-mode/style.css';
            $('#theme-style').attr('href', cssBasePath + newTheme);

            updateIcons(currentTheme);
            createCookie("theme", newTheme, 365);
        });        
        
        // Load theme from cookie
        if (savedTheme) {
            $('#theme-style').attr('href', cssBasePath + savedTheme);
            updateIcons(savedTheme);
        }     
    /*== END/Mode Switch ==*/
});