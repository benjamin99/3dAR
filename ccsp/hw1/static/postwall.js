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

function deleteMessage(tar_id) {
    $.get(
    	'/del',
        { id: tar_id },
        function() {
            //TODO: delete the elements on the wall:
            $('#'+ tar_id ).remove();
        }
    );
}

function updatePostWall() {
    $.ajax({
        type: "GET",
        url: "/fetch",
        data: {id: g_id },
        dataType: "xml",
        timeout: 3000,
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
                    var postID = $("postID", message).text();
                    info += "<div id=" + postID + ">" +
                            "<b>" + $("author", message).text() +
                            "</b> @ " + $("time", message).text() +
                            " -- " + $("rcount", message).text() + 
                            ":<blockquote><pre>" + content + "</pre></blockquote>" +
                            "</b><input type='submit' id='del_msg' value='delete' onclick='deleteMessage("+ postID +");'></input>" +
                            "</div>";

                });
            }
            if(info) {
                $('#info').prepend(info);
            }
            updatePostWall();
        }
    });
}

function updateWeather(cityTag) {
    $.ajax({
        type: 'GET',
        url:  '/weather',
        data: {city: cityTag},
        dataType: 'xml',
        timeout: 3000,
        error: function() { updateWeather(cityTag); },
        success: function(xml) {
           //TODO: update the weather on the postWall.
           var cityName = $("cityname", xml).text();
           var temperature = $("temperature", xml).text();
           var rainChance  = $("rainchance", xml).text();
           
           info = cityName + " 溫度:" + temperature + " 降雨機率:" + rainChance;
           $('#weather').text(info);
        }
    });

}
