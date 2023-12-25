from odoo import fields, models, tools


class ActivityReport(models.Model):
    """ CRM Lead Analysis """

    _inherit = "crm.activity.report"


    def action_edit_activity(self):
        
    
        return {
            'type': 'ir.actions.act_window',
            'name': 'Activity Report',
            'res_model': 'activity.report.wizard',
            'view_mode': 'form',
            'target': 'new',
        }




    
  





