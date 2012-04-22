document.addEvent('domready', function() {
    var ajax_properties = {
        load_button_id: 'load_button',
        item_class: 'single_comics_box',
        pages_class: 'comics_pages',
        count: 5,
        load_url: '/ajax_comics_loader/'
    };

    var AjaxLoader = new Class({
        Implements: Options,

        options: ajax_properties,

        initialize: function(options) {
            this.setOptions(options);
    		$(this.options.load_button_id).addEvent('click', this.start_request.bind(this));
        },

        start_request: function(e) {
            e.stop();
    		new Request({
    		    url: this.options.load_url,
    		    onSuccess: function(r) {
    		        this.parse_result(r);
    		    }.bind(this),
    		}).post({
    		    last_item_id: $$('.'+this.options.item_class).getLast().id,
    		    count: this.options.count,
    		});
        },
	
    	parse_result: function(server_response) {
    		if (server_response.trim() == 'no_new_items') {
    		    $(this.options.load_button_id).getChildren().addClass('disabled');
    		    return
    		};
    		var last_page_id = $$('.'+this.options.pages_class).getLast().id;
    		var last_page = $(last_page_id);
    		/* new_page_id is prefix + number + 1;*/
    		var new_page_id = last_page_id.slice(0, -1) + (last_page_id.split('_')[1].toInt() + 1);
    		var ajax_comics_page = new Element('div', {
                styles: {
                	//opacity: '0',
                 },
    			class: this.options.pages_class,
                id: new_page_id,
    	    });
			ajax_comics_page.set('html', server_response);
			ajax_comics_page.inject(last_page, 'after');
			/* without links property SmoothScroll is not smooth. don't know why. */
			var win_scroller = new Fx.SmoothScroll({links: 'comics_pages'}, window);
			win_scroller.toElement(new_page_id);
    	},
    
    });

    var AL = new AjaxLoader();
});
