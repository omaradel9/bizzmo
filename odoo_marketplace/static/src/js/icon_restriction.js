/** @odoo-module **/
    import { patch } from "@web/core/utils/patch";
    import { MessagingMenu } from '@mail/components/messaging_menu/messaging_menu';
    const { useState } = owl;

    var ajax = require('web.ajax');
       patch(MessagingMenu.prototype,'odoo_marketplace.icon_restriction',{

        _constructor() {
            this._super(...arguments);
            this.marketplace_states = useState({
                is_seller: false
            });
            var self = this;
            ajax.jsonRpc("/wk/check/mp/seller", 'call',{})
            .then(function (is_seller) {
                self.marketplace_states.is_seller = is_seller;
            });
        },
    });
