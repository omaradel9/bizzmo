from odoo import fields, models, api


class MailActivity(models.Model):
    _inherit = "mail.activity"

    lead_id = fields.Many2one('crm.lead', "Opportunity", readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(MailActivity, self).default_get(fields)

        lead_id = self.env['ir.config_parameter'].sudo().get_param('crm_custom.crm_lead_id')

        if lead_id:
            res['lead_id'] = int(lead_id)
            res['res_model_id'] = self.env['ir.model']._get_id('crm.lead')
            res['res_id'] = res['lead_id']   

        return res

 