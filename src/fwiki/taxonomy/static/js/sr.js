var SearchResult = {

    render: function(data) {

        switch(data.type) {

            case "status":
                if (data.fbdata["to"]) {
                    this.renderTargetedStatus(data);
                }
                else {
                    this.renderStatus(data);
                }

                break;

            case "link":
                this.renderLink(data);
                break;

            case "photo":
                this.renderPhoto(data);
                break;
        }

    },

    renderStatus: function(data) {

        var tmpldata = {
            'name':     data.fbdata['from']['name'],
            'userid':   data.fbdata['from']['id'],
            'postid':   data.fbdata['id'],
            'message' : data.fbdata['message'],
            'datetime': jQuery.timeago(data.fbdata['created_time'])};

        this.postRender(data, "#sr_status_tmpl", tmpldata);
    },

    renderTargetedStatus: function(data) {
        var tmpldata = {
            'fromname':     data.fbdata['from']['name'],
            'fromuserid':   data.fbdata['from']['id'],
            'toname':       data.fbdata['to']['data'][0]['name'],
            'touserid':     data.fbdata['to']['data'][0]['id'],
            'postid':       data.fbdata['id'],
            'message' :     data.fbdata['message'],
            'datetime':     jQuery.timeago(data.fbdata['created_time'])};

        this.postRender(data, "#sr_targetedstatus_tmpl", tmpldata);
    },


    renderLink: function(data) {
        var tmpldata = {
            'name':         data.fbdata['from']['name'],
            'userid':       data.fbdata['from']['id'],
            'postid':       data.fbdata['id'],
            'message' :     data.fbdata['message'],
            'link_url' :    data.fbdata['link'],
            'link_name' :   data.fbdata['name'],
            'link_caption': data.fbdata['caption'],
            'link_image':   data.fbdata['picture'],
            'link_description':   data.fbdata['description'],
            'datetime': jQuery.timeago(data.fbdata['created_time'])};

        this.postRender(data, "#sr_link_tmpl", tmpldata);
    },


    renderComments: function(data) {
        domid = "sr_" + data.fbdata['id'];

        // Append sr_comments template
        $("#sr_comments_tmpl").tmpl().appendTo("#"+domid+" .commentsholder");

        // iterate through and append each comment
        for (i=0; i<data.fbdata.comments.data.length; i++) {
            comment = data.fbdata.comments.data[i]
            tmpldata = {
                'id' : comment['id'],
                'userid': comment.from.id,
                'name': comment.from.name,
                'message': comment.message,
                'datetime': jQuery.timeago(comment.created_time)
           }

            $("#sr_comment_tmpl").tmpl(tmpldata).appendTo("#"+domid+" .sr_comments");
        }

    },

    renderPhoto: function(data) {
        var tmpldata = {
            'photourl':     data.item['src_big'],
            'caption':      data.item['caption'],
            'pid':          data.item['pid'],
            'owner' :       data.item['owner']
        };

        // Temp, need to fix this server side
        data['id'] = data.item['pid'];

        this.postRender(data, "#sr_photo_tmpl", tmpldata);
    },

    postRender: function(data, template, tmpldata) {
        

        // Add temlate!
        $(template).tmpl(tmpldata).appendTo("#results");

        domid = "sr_" + data['id'];

        // Render commetns?
        //if (data.fbdata.comments) this.renderComments(data)

        // Now need to render XFBML
        FB.XFBML.parse(document.getElementById(domid));

        // Highlight searched term
        //$('#'+domid).highlight(Query.search_term);
    }


}