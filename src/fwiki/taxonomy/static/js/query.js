var Query = {

    search_term: '',
    facebook_id : '',
    access_token : '',
    friends: [],
    media_types: [],


    initQuery: function() {

        console.log("init query");

        // Get from facebook and save to object
    	fbRequiresSession(function(response) {

            console.log(response);

            session = response.session

            Query.facebook_id = session['uid'];
            Query.access_token = session['access_token'];
            Query.search_term = $("#querybox").val();

            // First clear results
            //$("#results").html('');

            // Show loading indicator 

            // Show left column query context
            Query.updateContextUI();

            // Show summary UI (x albums, x photos etc)
            $("#query_summary_tmpl").tmpl().appendTo("#results");

            // Pull server
            Query.pullServer(0);
    	});
    },

    pullServer: function(cursor) {
        url = API_BASE+ "/q";
        data = {'search':  Query.search_term, 'cursor' : cursor, 'facebook_id' : Query.facebook_id, 'access_token' : Query.access_token}
        console.log(data);
        $.ajax({
          url: url,
          dataType: 'json',
          data: data,
          success: Query.processResults
        });

    },


    processResults: function(ret) {
    	console.log(ret);

    	//return val will look like :
//    	{
//    		data : {
//	            'cursor' : <cursor val>,
//	            'items' : [
//	                       	{'type' : <type>, 'item' : { 'caption' : "" , ... }}
//	                       ],
//	            'done' : 0/1
//    		}
//
//
//
//    	}
	   // Iterate through and show
    	data = ret.data;
        console.log('items = ' + data.items);
        for (var i = 0; i < data.items.length; i++) {
            item = data.items[i];

            // Log to console and debugger
            console.log(item)
            $("#debug").append("<br>" + JSON.stringify(item.item) + "</br>");

            // Append to Query properties
            friend_id = item.item['owner']; // this needs to cleaned up, abstracted to work with all media types
            Query.friends.push(friend_id);

            // Render search result
            SearchResult.render(item);
        }

        // Update summary
        Query.updateSummaryUI();

        // Call back to get more if cursor provided
        if (data.done == 0) {
            Query.pullServer(data.cursor);
        }


    },

    complete: function() {
        // Turn off any animation
        
    },

    updateContextUI: function() {
        $("#query_context_tmpl").tmpl().appendTo("#col_left");
    },

    // Will need some work topdare this
    updateSummaryUI: function() {
        
        // Update friend count
        unique_friends = jQuery.unique(Query.friends);
        $("#query_summary_friend_count").html(unique_friends.length);

        // Add new friend photos
        for (var i=0; i < unique_friends.length; i++) {
  
            dom_id = "summary_image_"+unique_friends[i];
            if ($("#"+dom_id).length == 0) {
                var tmpldata = {'userid':    unique_friends[i] };
                $("#query_summary_pic_tmpl").tmpl(tmpldata).appendTo("#summary_images");
            }
        }
        
        // Now need to render new XFBML
        FB.XFBML.parse(document.getElementById("summary_images"));
    }
    
/*
    updateTerms: function(data) {

        //$("#terms").html('')
        Query.terms = data.terms

        // Iterate through and show the terms
        for (var i=0; i<data.terms.length; i++) {
            $("#terms").append(data.terms[i])
        }
    }
    
    updateContext: function(context) {
        Query.context = data.context

        var tmpldata = {
            'abstract':     context['abstract'],
            'image':        context['image'],
        };

        $("#context_tmpl").tmpl(tmpldata).appendTo("#context");
    }
    */
   
}