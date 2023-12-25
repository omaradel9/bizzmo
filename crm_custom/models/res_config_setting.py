from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crm_lead_id = fields.Many2one(
        string='Lead Name',
        comodel_name='crm.lead',
        store=True
    )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('crm_custom.crm_lead_id', self.crm_lead_id.id)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        Icpsudo = self.env['ir.config_parameter'].sudo()
        crm_lead_id = Icpsudo.get_param('crm_custom.crm_lead_id')
        if crm_lead_id:
            res.update(
                crm_lead_id=int(crm_lead_id)
            )
        return res
        
   

   
   
