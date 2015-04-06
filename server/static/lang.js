(function(){
    var page_lang = document.getElementsByTagName('html')[0].attributes["lang"].value;

    var menu = document.getElementsByClassName("lang");
    for (var i = 0; i < menu.length; i++){
        for (var j = 0; j < menu[i].classList.length; j++){
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
})();