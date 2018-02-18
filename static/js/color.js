var initial_color = tinycolor.random().toHexString();

$('#color-pick').colorpicker({
  'color': initial_color,
});

var make_text_readable = function(color) {
  var dark_secondary_light = ["#212531", "#6c757d", "#f8f9fa"];
  var best = tinycolor.mostReadable(color, dark_secondary_light).toHexString();
  $('body').css({'color': best});
};

var set_background_color = function(color) {
  $('body').css({'background-color': color});
  make_text_readable(color);
};

set_background_color(initial_color);

$('body').on('colorpickerChange', function(e) {
  var selected_color = e.color.toRgbString();
  set_background_color(selected_color);
});
