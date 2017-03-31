$(document).ready(function(){
    var oBlock = $(".c-tabs"),
        liClass = 'c-tabs__item';

    var sTemplate = "<li class=" + liClass +">" +
            "<div class='c-tabs__content'>" +
            "</div>" +
            "</li>";

    oBlock.children().each(function(i, item) {
        $(this).wrap(sTemplate);
        $('.c-tabs .c-tabs__item').last().prepend("<span class='c-tabs__link'>" + $(item).children('code').attr('class').toUpperCase() + " </span>")
    });
});