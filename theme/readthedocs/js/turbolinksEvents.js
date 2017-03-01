$(function () {
    var oDoc = $(document),
        sTocTree = ".toctree-l4",
        sClickEvent = "click",
        sTurboLinks = "turbolinks:";

    function myFunc() {
        var that = $(this),
            sDivClass = 'hidden_toctree-l4-incl',
            sDesc = '.fa-angle-down',
            sAsc = '.fa-angle-up';

        if (that.next() && that.next()[0].id == sDivClass) {
            if ($(that.next()[0]).is(':visible')) {
                $(that).children(sDesc).show();
                $(that).children(sAsc).hide();
                $(that.next()[0]).hide(); //.css(sDisplayValue, 'none');

            } else {
                $(that).children(sDesc).hide();
                $(that).children(sAsc).show();
                $(that.next()[0]).show(); //.css(sDisplayValue, 'block');
            }
        }
    }

    oDoc.on(sTurboLinks + "before-visit", function() {
        oDoc.off(sClickEvent, sTocTree, myFunc);
    });

    oDoc.on(sTurboLinks + "visit", function() {
        oDoc.on(sClickEvent, sTocTree, myFunc);
    });

    //oDoc.on(sTurboLinks + "click", function() {
    //    //Turbolinks.clearCache();
    //    oDoc.off(sClickEvent, sTocTree, myFunc);
    //});
    //
    //oDoc.on(sTurboLinks + "visit", function() {
    //    oDoc.on(sClickEvent, sTocTree, myFunc);
    //});

    oDoc.on(sClickEvent, sTocTree, myFunc);
});