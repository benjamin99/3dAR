function postMessage() {
    
    $.post(
        '/post',
        { content: encodeURI($("#text_box").val())},
        function() {
            updatePostWall();
            $('#text_box').val("");	
        }
    );

}


function updatePostWall() {
}
