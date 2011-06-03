ids = [];
var tagsObj = new Object();

function fetchTagsFromFb(url) {
    FB.api( url, function(response) {
	if(response.paging) {
	    picArray = response.data;
	    $.each( picArray, function(index, pic){
                tagArray = pic.tags.data;
		$.each( tagArray, function(index, tag){
		    if(tag.id != '')
                        appendTag( tag.id, tag.name );
		});
            });

            fetchTagsFromFb( response.paging.next );
	}
	else { //Sort the tags by count and display them:
	    tags = [];
            for( i=0; i<ids.length; i++) {
	        tags.push( tagsObj[ids[i]] );
	    }
	    tags.sort(sortTagList);

	    var message = [];
	    $.each( tags, function(index, tag) {
		message.push('<li>');
		message.push('<a href="#">');
		message.push( tag.name );
		message.push('<br>');
		message.push( tag.count);
		message.push( '<img src="https://graph.facebook.com/');
		message.push( tag.id );
		message.push( '/picture"');
		message.push('>');
		message.push('<a>');
		message.push('</li>');
            });
	    if(message) {
                $('#start').append( message.join("") );	        
	    }
	}
    });
}

function appendTag( id, name ) {
    if( tagsObj[id] ) 
        tagsObj[id]['count'] = tagsObj[id]['count'] + 1;
    else {
	tagsObj[id] = new Object();
	tagsObj[id]['id'] = id;
        tagsObj[id]['name'] = name;
	tagsObj[id]['count'] = 1;
	ids.push(id);
    }
}

function sortTagList( a, b ) {
    return b['count'] - a['count'];
}
