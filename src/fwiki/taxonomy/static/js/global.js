//Constants => have this come from the server side conf instead
var BASE = "http://localhost:8080"
var API_BASE = "http://localhost:6888"
var APP_ID = "139274172804886"


// Load FB library
$(function() {
    window.fbAsyncInit = function() {
        
        FB.init({appId: APP_ID, status: true, cookie: true, xfbml: true,  oauth  : true});
        FB.Event.subscribe('auth.authResponseChange', FWIKI.fbSessionChange);

    };

    $('body').append('<div id="fb-root"></div>');
    $.getScript(document.location.protocol + '//connect.facebook.net/en_US/all.js');
})


// After DOM is loaded
$(window).load(function () {
    console.log('window load');

    FWIKI.init();
    
});


var FWIKI = {

	init : function() {
			
	} ,
	
	loginSetup : function() {
		
		$('#fb_login').click(function(){
			window.location ="http://www.facebook.com/dialog/oauth/?scope=email,read_stream,offline_access,friends_likes,friends_checkins,user_checkins,user_photos,friends_photos,friends_location,friends_photo_video_tags,friends_hometown&client_id=139274172804886&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Ffb_login&response_type=code"
		} );
		
//		$('#fb_login').click(function(){
//			FB.getLoginStatus(function(response) {
//		        aResp = response.authResponse;
//		        if (aResp == null) {
//		        	window.location ="http://www.facebook.com/dialog/oauth/?scope=email,read_stream,offline_access,friends_likes,friends_checkins,user_checkins,user_photos,friends_photos,friends_location,friends_photo_video_tags,friends_hometown&client_id=139274172804886&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Ffb_login&response_type=code"
//		        } else {
//		        	//means this is an existing user,
//		        	//FWIKI.setState(response.authResponse);
//		        }
//			});
			
//		});
		
	},
	
	setState : function(aResponse) {
		console.log(aResponse);
		 $.ajax({
			   url: "/_xhr/setup_user",
			   cache: false,
			   data: aResponse,
			   success: function(json){
			     console.log(json)
			   }
			 });
	},
	
	reelSetup : function() {
		src_reel = []
	    
	    for(i =0 ; i < reel_pics.length ; i++) {
	    	src_reel[i] = { src : reel_pics[i] };
	    }
	    
	    console.log(src_reel);
	    
	    $('#reel').crossSlide({
	    		sleep: 2,
	    		fade: 1
	    	}, 
	    	src_reel
	    );
	},

	
	searchSetup : function() {
		
		$("#querybox").keyup(function(event){
	        if(event.keyCode == 13){
	          // Require login, then redirect upon query
	          fbRequiresSession(function(session) {
	              query = $("#querybox").val();
	              window.location = BASE + "/q/" + query;
	          });
	        }
	    });    
		
	} ,
	
	fbRequiresSession: function(cb) {
		FB.getLoginStatus(function(response) {
	        console.log(response.session)
	        session = response.session
	        if (!session) {
	            this.fbLogin(cb);
	        }
	        else {
	            cb(response);
	        }
	    });
	},
	
	// Facebook abstraction call
	fbLogin : function (success_callback) {
	    FB.login(function(response) {
	      if (response.session) {
	        if (response.perms) {
	          success_callback();
	          // user is logged in and granted some permissions.
	          // perms is a comma separated list of granted permissions
	        } else {
	          // user is logged in, but did not grant any permissions
	        }
	      } else {
	        // user is not logged in
	      }
	    }, {perms:'read_stream,offline_access,friends_likes,friends_checkins,user_checkins,user_photos,friends_photos,friends_location,friends_photo_video_tags,friends_hometown'});
	},
	
	fbSessionChange : function () {
	    console.log('session change');
	    // Post-load means that we don't have the ability to determine user session server-side & user not authenticated
	    if (window.location.hash.length == 1) {
	    	var accessToken = window.location.hash.substring(1);
	    	
	    	console.log(accessToken);
	    	
	    	
	    }
	}

	
	
	
	
}


function fbLogout() {
    FB.logout(function(response) {
        
    });
}
// Callback on session change to change data

