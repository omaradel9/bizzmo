/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */
if (!odoo.defineCalled) {
odoo.define('odoo_marketplace/static/src/js/activity_icon_hide.js', function (require) {
  "use strict";
  var ajax = require('web.ajax');
  $(document).ready(function () {
    ajax.jsonRpc("/wk/check/mp/seller", 'call', {})
      .then(function (is_seller) {
        if (is_seller) {
          $('.o_mail_systray_item').hide()
        }
      });

  });
})
odoo.defineCalled = true;
}
