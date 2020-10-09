from odoo import api,models,fields
import logging 


_logger = logging.getLogger(__name__)
class HRTalents(models.Model):
    _name = 'hr.talents'
    _rec_name = 'applicant_id'
    
    #Adding custom fields
    applicant_id = fields.Many2one('hr.applicant',string = 'Talent')
    college = fields.Many2one('res.partner',string = 'College')
    companies = fields.Many2many('res.partner',string = 'Companies')
    
    
