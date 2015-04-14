(function(){

    /* GENERAL */
    var i, j;
    var page_lang = document.getElementsByTagName('html')[0].attributes["lang"].value;

    /* LANG */
    var menu = document.getElementsByClassName("lang");
    for (i = 0; i < menu.length; i++){
        for (j = 0; j < menu[i].classList.length; j++){
            if (menu[i].classList[j].substr(0, 5) == "lang-"){
                var current_lang = menu[i].classList[j].substr(5);
                if (current_lang == page_lang){
                    menu[i].classList.add("lang-active");
                }
                menu[i].onclick = function(lang){
                    return function(){
                        if (lang) {
                            var url = document.location.pathname;
                            url = (url.indexOf("/", 1) == -1) ? "" : url.substr(url.indexOf("/", 1));
                            document.location.pathname = "/" + lang + url;
                        }
                        return false;
                    }
                }(current_lang);
                break;
            }
        }
    }

    /* FORM */
    var forms = document.getElementsByClassName("form_summoner_search");
    for (i = 0; i < forms.length; i++) {
        forms[i].onsubmit = function(form){
            return function() {
                var select = form.querySelector("[name=summoner_region]");
                var region = select.options[select.selectedIndex].value;
                var name = encodeURIComponent(form.querySelector("[name=summoner_name]").value);
                if (name.trim().length > 0)
                    window.location.href = "/" + page_lang + "/game/" + region + "/" + name;
                return false;
            }
        }(forms[i]);
    }

    /* Description for given tips */
    var descriptions = document.getElementsByClassName("description");
     for (i = 0; i < descriptions.length; i++) {
        var title = descriptions[i].previousElementSibling;
        title.onclick = function(elem){
            return function() {
                if (elem.className === 'description')
                    elem.className = 'description hide';
                else
                    elem.className = 'description';
            }
        }(descriptions[i]);
    }

})();