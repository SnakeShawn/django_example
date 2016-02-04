 $(document).ready(function() {
             $('#changeTheme a').click(function(event) {
                $('.container').attr('class', $(this).attr('data-theme')+' container');
                $('[name="theme"]').val($(this).attr('data-theme'));
                $('#changeTheme .glyphicon').remove();
                $(' <span class="glyphicon glyphicon-ok"></span>').appendTo($(this));
              });
            $('#demoList .label').click(function(event) {
                $(this).parent().find('.label').removeClass('label-pick');
                $(this).addClass('label-pick');
                $('#demoListForm input').val($(this).text());
            });
            $('code').addClass('prettyprint linenums');
            prettyPrint();
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

function getDemoData () {
       var demo=[{
            theme:"monokai",
            step:{

            }
       },{

       },{

       }]
}   

//for demo only, this function should be the visualization function

function visualization (data) {
    switch(data){
        case 1:
            break;
        case 2:
            break;
        case 3:
            break;
    }
}