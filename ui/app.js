(function($) {

  var app = $.sammy('#app', function() {
    this.get('#/', function(context) {
      context.app.swap('');
      context.render('views/index.html', {})
               .appendTo(context.$element());
      });
      this.get('#/add-employee', function(context) {
        context.app.swap('');
        context.render('views/add-employee.html', {})
                 .appendTo(context.$element());
        });
      this.get('#/view-employees', function(context) {
        context.app.swap('');
        context.render('views/view-employees.html', {})
                 .appendTo(context.$element());
        });
    });

  $(function() {
            app.run('#/');
  });
})(jQuery);
