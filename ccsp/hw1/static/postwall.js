var g_id = 0;

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
    $.ajax({
        type: "GET",
        url: "/fetch",
        data: {id: g_id },
        dataType: "xml",
        timeout: 5000,
        error: function() { updatePostWall();},
        success: function(xml) {
	    var info = "";
            var id = parseInt($("id",xml).text());
            if( id > g_id ) {
                g_id = id;
                $("message", xml).each( function(i){
		    var message = $("message", xml).get(i);
                    var content = decodeURI($("content", message).text()).replace(/</g, "&lt;").replace(/>/g, "&gt;");
                    /*if (($.browser.mozilla || $.browser.opera) && content.length > LENGTH) {
                        var str = "";
                        while (content.length > LENGTH) {
                           str += content.substr(0, LENGTH) + "<br />";
                           content = content.substr(LENGTH, content.length);
                        }
                        content = str + content;
                    }*/
                    info += "<b>" + $("author", message).text() +
                            "</b> @ " + $("time", message).text() + ":<blockquote><pre>" +
                            content + "</pre></blockquote>";

                });
            }
            if(info) {
                $('#info').prepend(info);
            }
            updatePostWall();
        }
    });
}
