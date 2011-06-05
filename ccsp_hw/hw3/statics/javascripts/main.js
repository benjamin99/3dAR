ids = [];
var tagsObj = new Object();
var imgsObj = new Object(); 

window.onload = function() {
    var url = '/me/photos';
    fetchTagsFromFb( url );
}

// Onload methods:
function fetchTagsFromFb(url) {
    FB.api( url, function(response) {
	if(response.paging) {
	    picArray = response.data;
	    $.each( picArray, function(index, pic){
                //Handle sources and pictures:
		var tmpObj = new Object();
                tmpObj['source'] = pic.source;
		tmpObj['thumb'] = pic.picture;
		imgsObj[ pic.id ] = tmpObj;

		//Handle tags:
                tagArray = pic.tags.data;
		var pid = pic.id;
		$.each( tagArray, function(index, tag){
		    if(tag.id != '')
                        appendTag( tag.id, tag.name, pid );
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
		message.push('<li class="arrow">');
		message.push('<a href="#" onclick="return appendAndGotoFriendPage(');
	        message.push( tag.id + ');">');
		message.push( tag.name );
		message.push('<br>');
		message.push( tag.count);
		message.push( '<img src="https://graph.facebook.com/' + tag.id + '/picture">');
		message.push('<a>');
		message.push('</li>');
            });
	    if(message) {
                $('#start').append( message.join("") );	        
	    }
	}
    });
}

function appendTag( id, name, pid ) {
    if( tagsObj[id] ) {
        tagsObj[id]['count'] = tagsObj[id]['count'] + 1;
        tagsObj[id]['pics'].push( pid ); 
    }
    else {
	tagsObj[id] = new Object();
	tagsObj[id]['id'] = id;
        tagsObj[id]['name'] = name;
	tagsObj[id]['count'] = 1;
	tagsObj[id]['pics'] = [ pid ];
	ids.push(id);
    }
}

function sortTagList( a, b ) {
    return b['count'] - a['count'];
}

// Friend page methods:
function appendAndGotoFriendPage( fid ) {
    
    if( $('#fid_' + fid ).length == 0 ) {
        var newdiv = [];
        newdiv.push('<div id="fid_');
        newdiv.push( fid );
        newdiv.push('">');
        newdiv.push('<div class="toolbar">');
        newdiv.push('    <h1> Friend </h1>');
        newdiv.push('    <a class="button back" href="#main">Back</a>');
        newdiv.push('</div>');
	newdiv.push('<ul class="rounded" id="photos">');
	
	var photoList = tagsObj[fid]['pics'];
	if(photoList.length > 0) {
	    $.each( photoList, function( index, pid ){  
	        newdiv.push('<li class="arrow">');
		var from = '#fid_' + fid;
		newdiv.push('<a href="#" onclick="return appendAndGotoPhotoPage('+ pid +', \'' + from + '\');">');
                newdiv.push('<img src="' + imgsObj[pid]['thumb'] + '">'); 
		newdiv.push('</a>');
	        newdiv.push( '</li>');
	    });
	}

	newdiv.push('</ul>');
        newdiv.push('</div>'); 
        $('body').append( newdiv.join("") );

    }
    jQT.goTo( '#fid_' + fid, 'flip');
}

// Photo page methods:
function appendAndGotoPhotoPage( pid, from ) {
    if( $( '#pid_' + pid ).length == 0) {
        var newdiv = [];
        newdiv.push('<div id="pid_');
        newdiv.push( pid );
        newdiv.push('">');
        newdiv.push('<div class="toolbar">');
        newdiv.push('    <h1> Photo </h1>');
        newdiv.push('    <a class="button back" href="'+ from + '">Back</a>');
        newdiv.push('</div>');
        newdiv.push('<ul class="rounded">');
	newdiv.push('<li> <img src="'+ imgsObj[pid]['source'] + '"> </li>');
	newdiv.push('</ul>');
        $('body').append( newdiv.join("") );
    
    }
    jQT.goTo( '#pid_' + pid, 'flip' );
}


// Sharing methods:
function shareOnFb() {
    FB.ui(
   {
     method: 'feed',
     name: 'Facebook Dialogs',
     display: 'popup',
     caption: 'MyFriendsTags is amazing!',
     message: 'Try this one!'
   },
   function(response) {
     if (response && response.post_id) {
       //alert('Post was published.');
     } else {
       //alert('Post was not published.');
     }
   }
 );
}
