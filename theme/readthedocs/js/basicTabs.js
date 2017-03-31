(function( $ ) {
  $.fn.basicTabs = function(options){
    var settings = $.extend({
      active_class: "is-active",
      open_class: "is-open",
      list_class: "c-tabs",
      starting_tab: 1
    }, options );

    $("." + settings.list_class).each(function() {
      $(this).children('li:nth-child(' + settings.starting_tab + ')' ).children('span').addClass(settings.active_class).next().addClass(settings.open_class).show();
    });    
    $("." + settings.list_class).on('click', 'li > span.c-tabs__link', function(event) {
      if (!$(this).hasClass(settings.active_class)) {
        event.preventDefault();
        var tabs = $(this).closest("." + settings.list_class);
        tabs.find("." + settings.open_class).removeClass(settings.open_class).hide();

        $(this).next().toggleClass(settings.open_class).toggle();
        tabs.find("." + settings.active_class).removeClass(settings.active_class);
        $(this).addClass(settings.active_class);
      } else {
        event.preventDefault();
      }
    });
  };
}( jQuery ));


