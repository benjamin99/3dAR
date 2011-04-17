function postMessage() {
    
    $.post(
        '/post',
        { content: encodeURI($("#text_box").val())
        },
        function() {
            updatePostWall();
            $('#text_box').val("");	
        }
    );

}


function updatePostWall() {
    $.ajax(
        type: "GET",
        url: "/fetch",
        data: {id: g_id },
        dataType: "xml",
        timeout: 5000,
        error: function() { updatePostWall();},
        success: function(xml) {
	    var message = "";
            var id = parseInt($("id",xml).text());
            if( id > g_id ) {
                g_id = id;
            }
        }
    );
}
