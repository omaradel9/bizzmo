from odoo import models, fields, api


class ActivityReportWizard(models.TransientModel):
    _name = 'activity.report.wizard'
    _description = 'Activity Report Wizard'


    name = fields.Char(related='lead_id.name')
    date = fields.Datetime('Completion Date')
    lead_create_date = fields.Datetime('Creation Date')
    date_conversion = fields.Datetime('Conversion Date')
    date_deadline = fields.Date('Expected Closing')
    date_closed = fields.Datetime('Closed Date')
    author_id = fields.Many2one('res.partner', 'Assigned To')
    user_id = fields.Many2one('res.users', 'Salesperson')
    team_id = fields.Many2one('crm.team', 'Sales Team')
    lead_id = fields.Many2one('crm.lead', "Opportunity")
    body = fields.Html('Activity Description')
    subtype_id = fields.Many2one('mail.message.subtype', 'Subtype')
    mail_activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type')
    country_id = fields.Many2one('res.country', 'Country')
    company_id = fields.Many2one('res.company', 'Company')
    stage_id = fields.Many2one('crm.stage', 'Stage')
    partner_id = fields.Many2one('res.partner', 'Customer')
    lead_type = fields.Selection(
        string='Type',
        selection=[('lead', 'Lead'), ('opportunity', 'Opportunity')],
        help="Type is used to separate Leads and Opportunities")
    active = fields.Boolean('Active')




    @api.model
    def default_get(self, fields):
        res = super(ActivityReportWizard, self).default_get(fields)
        record_id= self._context.get('active_id')
        if record_id:
            record_data = self.env['crm.activity.report'].browse(record_id)

            res['date'] = record_data['date']
            res['lead_create_date'] = record_data['lead_create_date']
            res['date_conversion'] = record_data['date_conversion']
            res['date_deadline'] = record_data['date_deadline']
            res['date_closed'] = record_data['date_closed']
            res['author_id'] = record_data['author_id']
            res['user_id'] = record_data['user_id']
            res['team_id'] = record_data['team_id']
            res['lead_id'] = record_data['lead_id']
            res['name'] = record_data['lead_id'].name
            res['body'] = record_data['body']
            res['subtype_id'] = record_data['subtype_id']
            res['mail_activity_type_id'] = record_data['mail_activity_type_id']
            res['country_id'] = record_data['country_id']
            res['company_id'] = record_data['company_id']
            res['stage_id'] = record_data['stage_id']
            res['partner_id'] = record_data['partner_id']
            res['lead_type'] = record_data['lead_type']
            res['active'] = record_data['active']
        
     
        
    
        return res




    def action_create_lead_and_mailmessage(self):
        query_lead = """
            UPDATE crm_lead
            SET name = %s,
                create_date = %s,
                date_conversion = %s,
                date_closed = %s,
                date_deadline = %s,
                user_id = %s,
                team_id = %s,
                country_id = %s,
                company_id = %s,
                stage_id = %s,
                partner_id = %s,
                email_from = %s,
                phone = %s,
                city = %s,
                zip = %s,
                street = %s,
                partner_name = %s,
                contact_name = %s,
                function = %s,
                type = %s,
                active = %s
            WHERE id = %s
        """
        params_lead = (
            self.name,
            self.lead_create_date,
            self.date_conversion,
            self.date_closed,
            self.date_deadline,
            self.user_id.id,
            self.team_id.id,
            self.partner_id.country_id.id,
            self.company_id.id,
            self.stage_id.id,
            self.partner_id.id,
            self.partner_id.email,
            self.partner_id.phone,
            self.partner_id.city,
            self.partner_id.zip,
            self.partner_id.street,
            self.partner_id.name,
            self.partner_id.name,
            self.partner_id.function,
            self.lead_type,
            self.active,
            self.lead_id.id
        )
        self.env.cr.execute(query_lead, params_lead)




        message_query = """
            UPDATE mail_message
            SET subtype_id = %s,
                author_id = %s,
                date = %s,
                body = %s
            WHERE res_id = %s
        """
        message_params = (
            self.subtype_id.id,
            self.author_id.id,
            self.date,
            self.body,
            self.lead_id.id
        )
        self.env.cr.execute(message_query, message_params)


       






  

       

    




  

    

        

       