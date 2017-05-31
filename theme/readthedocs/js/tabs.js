$(document).ready(function(){
    var oBlock = $(".c-tabs"),
        liClass = 'c-tabs__item',
        sLiClassItem = '.c-tabs .c-tabs__item',
        sBtnElem = 'copyButton',
        sTooltip = 'tooltip',
        sClickAction = 'click',
        sTabsContentClass = 'c-tabs__content',
        oButton;

    var sTemplate = "<li class=" + liClass + ">" +
            "<div class=" + sTabsContentClass + ">" +
            "</div>" +
            "</li>";

    oButton = $('<button/>', {
        "class": sBtnElem,
        "id": sBtnElem,
        "rel": sTooltip,
        "title": "Copied!",
        "container": '.' + sBtnElem,
        "data-toggle": sTooltip,
        "data-trigger": sClickAction,
        "data-placement": "bottom"
    });

    oBlock.children().each(function(i, item) {
        var oItem;

        $(this).wrap(sTemplate);
        oItem = $(sLiClassItem);
        oItem.last().prepend("<span class='c-tabs__link'>" + $(item).children('code').attr('class').toUpperCase() + " </span>");
    });

    oButton.append("<img class='clippy' src='/img/clippy.svg'>");

    oBlock.each(function(i, item) {
        item.appendChild(oButton.first().clone()[0]);
    });

    $('.' + sBtnElem).each(function(i, item) {
        item.addEventListener(sClickAction, function() {
            var aPrevCodeEls = $(this).prevAll('.' + liClass);

            copyToClipboard($(this).prevAll('.' + liClass).find('.' + sTabsContentClass + '.is-open code:not(.hljs-line-numbers)'), this);
        })
    });

    function setTooltip(btn) {
        $(btn).tooltip('show');
        setTimeout(function() {
            $(btn).tooltip('hide');
        }, 1000);
    }

    function removeRanges() {
        window.getSelection().removeAllRanges();
    }

    function copyToClipboard(elem, btn) {
        var range,
            succeed;

        removeRanges();
        range = document.createRange();

        range.selectNode(elem[0]);
        window.getSelection().addRange(range);

        try {
            succeed = document.execCommand("copy");
            setTooltip(btn);
        } catch(e) {
            succeed = false;
        }
        if (succeed) {
            removeRanges();
        }
    }
});