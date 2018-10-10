$( document ).ready(function() {
    var SHIFT_CLASS = "shift";

    // Shift nav in mobile when clicking the menu.
    $(document).on('click', "[data-toggle='wy-nav-top']", function() {
      $("[data-toggle='wy-nav-shift']").toggleClass(SHIFT_CLASS);
      $("[data-toggle='rst-versions']").toggleClass(SHIFT_CLASS);
    });
    // Close menu when you click a link.
    $(document).on('click', ".wy-menu-vertical .current ul li a", function() {
      $("[data-toggle='wy-nav-shift']").removeClass(SHIFT_CLASS);
      $("[data-toggle='rst-versions']").toggleClass(SHIFT_CLASS);
    });
    $(document).on('click', "[data-toggle='rst-current-version']", function() {
        var SHIFT_UP_CLASS = "shift-up";

        $("[data-toggle='rst-versions']").toggleClass(SHIFT_UP_CLASS);
        $("[data-toggle='rst-other-versions']").toggleClass(SHIFT_UP_CLASS);
    if ($(".fa-caret-down").length > 0)
        $(".fa-caret-down").attr('class', 'fa fa-caret-up');
    else
        $(".fa-caret-up").attr('class', 'fa fa-caret-down');
    });
    // Make tables responsive
    $("table.docutils:not(.field-list)").wrap("<div class='wy-table-responsive'></div>");

    hljs.initHighlightingOnLoad();

    $('table').addClass('docutils');
});

window.SphinxRtdTheme = (function (jquery) {
    var stickyNav = (function () {
        var navBar,
            win,
            stickyNavCssClass = 'stickynav',
            applyStickNav = function () {
                if (navBar.height() <= win.height()) {
                    navBar.addClass(stickyNavCssClass);
                } else {
                    navBar.removeClass(stickyNavCssClass);
                }
            },
            enable = function () {
                applyStickNav();
                win.on('resize', applyStickNav);
            },
            init = function () {
                navBar = jquery('nav.wy-nav-side:first');
                win    = jquery(window);
            };
        jquery(init);
        return {
            enable : enable
        };
    }());
    return {
        StickyNav : stickyNav
    };
}($));
