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
            that.children(sDesc).toggle();
            that.children(sAsc).toggle();
            $(that.next()[0]).toggle(); //.css(sDisplayValue, 'none');

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