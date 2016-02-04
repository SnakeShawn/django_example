$(document).ready(function() {
	$('code').addClass('prettyprint linenums');
            prettyPrint();
             $('#changeTheme a').click(function(event) {
                $('#coding-coding').attr('class', $(this).attr('data-theme'));
                $('[name="theme"]').val($(this).attr('data-theme'));
                $('#changeTheme .glyphicon').remove();
                $(' <span class="glyphicon glyphicon-ok"></span>').appendTo($(this));
              });
               $('[data-toggle="popover"]').popover({
                trigger:"hover"
              });
              $("table").colResizable();
             var jsav = new JSAV("v");
                var arr = [1, 2, 3, 4, 5, 6, 7, 8];
                jsav.label("Normal Array");
                var arr1 = jsav.ds.array(arr);
                arr1.highlight(2);
                arr1.css(4, {"background-color": "aqua", "color": "rgb(150, 55, 50)"});
                arr1.layout();
                jsav.label("Bar Array");
                var arr2 = jsav.ds.array(arr, {layout: "bar"});
                arr2.highlight(2);
                arr2.css(4, {"background-color": "aqua", "color": "rgb(150, 55, 50)"});
                arr2.layout();
});	