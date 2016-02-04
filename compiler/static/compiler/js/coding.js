
$(document).ready(function() {
    var editor = ace.edit("coding");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
  $('[data-toggle="popover"]').popover({
    trigger:"hover"
  });
  // setTimeout(function() {
  //       var placeholder = 'Try coding and debugging by yourselves! \nYou have two options: \n1. TYPE your code here, \n2. or click on [Attach File] to UPLOAD a local file. \nNote: the existing code will be replaced by the content uploaded! ';
  //       $('textarea').on('focus', function(event) {
  //           $(this).html('').removeClass('placeholder');
  //       }).on('blur', function(event) {
  //             if ($(this).val().replace(/\s/g, '').length==0) {
  //                 // $('#coding textarea').html(placeholder);
  //                 // $(this).html('').addClass('placeholder');
  //                 alert("what")
  //             };
  //       });
  // }, 100);

  $('#changeTheme a').click(function(event) {
     $('.container').attr('class', $(this).attr('data-theme')+' container');
    editor.setTheme("ace/theme/"+$(this).attr('data-theme'));
    $('[name="theme"]').val($(this).attr('data-theme'));
    $('#changeTheme .glyphicon').remove();
    $(' <span class="glyphicon glyphicon-ok"></span>').appendTo($(this));
  });
  $('[data-action="visualization"]').click(function(event) {
    var jsav = new JSAV("v");
    var arr = [1, 2, 3, 4, 5, 6, 7, 8];
    jsav.label("Normal Array");
    var arr1 = jsav.ds.array(arr);
    arr1.highlight(2);
    arr1.css(4, {
      "background-color": "aqua",
      "color": "rgb(150, 55, 50)"
    });
    arr1.layout();
    jsav.label("Bar Array");
    var arr2 = jsav.ds.array(arr, {
      layout: "bar"
    });
    arr2.highlight(2);
    arr2.css(4, {
      "background-color": "aqua",
      "color": "rgb(150, 55, 50)"
    });
    arr2.layout();
  });


});




