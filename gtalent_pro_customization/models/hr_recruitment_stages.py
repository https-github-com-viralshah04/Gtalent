from odoo import api,fields,models


class InheritHRStage(models.Model):
    _inherit = 'hr.recruitment.stage'
    
    applicant_email_notification = fields.Boolean("Send Email Notification to Applicant",
                                                  copy = False,
                                                  help ='If set,will send email notification to applicant.')
    
    applicant_whatsapp_notification = fields.Boolean("Send Whats App Notification to Applicant",
                                                     copy = False,
                                                     help = 'If set,will send Whats App notification to applicant.')