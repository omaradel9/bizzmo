/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Message } from '@mail/components/message/message';
import { PartnerImStatusIcon } from '@mail/components/partner_im_status_icon/partner_im_status_icon';
var ajax = require('web.ajax')
const { useState } = require('web.core');



  patch(PartnerImStatusIcon.prototype, "odoo_marketplace.message_restriction", {
    _onClick(ev) {
      return false
      var self = this;
      const _super = this._super;
      ajax
        .jsonRpc("/wk/check/mp/seller", "call", {})
        .then(function (is_seller) {
          if (!is_seller) {
            _super.apply(self, arguments);
          }
        });
    },
  });

  patch(Message.prototype, "odoo_marketplace.message_restriction", {
    _constructor() {
      var self = this;
      this._super(...arguments);
      this.is_seller = false;
      ajax
        .jsonRpc("/wk/check/mp/seller", "call", {})
        .then(function (is_seller) {
          self.is_seller = is_seller;
          $('.o_mail_systray_item').hide()
        });
        $(function(){
          $('a[data-oe-model="res.partner"]').on("mouseover", function(){
              $(this).attr('href', '#');
          });
        });


    },

    _onClickAuthorAvatar(ev) {
      if (!this.is_seller) {
        this._super.apply(this, arguments);
      }
    },

    _onClickAuthorName(ev) {
      if (!this.is_seller) {
        this._super.apply(this, arguments);
      }
    },

    _onClick(ev) {
      ev.preventDefault();      
      const anchor = ev.target.closest("a");  
      if (!anchor) return;                       
      anchor.getAttribute('href');
      anchor.setAttribute("href","#")
      if (!this.is_seller) {
        this._super.apply(this, arguments);
      }
    },
  });
