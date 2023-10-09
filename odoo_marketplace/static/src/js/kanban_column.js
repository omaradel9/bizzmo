odoo.define('odoo_marketplace.kanban_column',function(require){
"use strict";
    var ajax = require('web.ajax');

    var KanbanColumn = require('web.KanbanColumn');
    var KanbanRenderer = require('web.KanbanRenderer');

    KanbanColumn.include({

        init: function (parent, data, options, recordOptions) {
            this._super(parent, data, options, recordOptions);
            if(data.context.no_archive == 1){
                this.has_active_field = false;
            }
        },
    });

    KanbanRenderer.include({

        _setState: function (state) {
          ajax.jsonRpc("/wk/check/mp/seller", 'call', {})
            .then(function (is_seller) {
              if (is_seller) {
                $('.o_mail_systray_item').hide()
              }
            });
            this._super.apply(this, arguments);
            var arch = this.arch;
            var drag_drop = true;
            if (arch.attrs.disable_draggable) {
                if (arch.attrs.disable_draggable == 'true') {
                    this.columnOptions.draggable = false;
                }
            }
        },

    });

});
