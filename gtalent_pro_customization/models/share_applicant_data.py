from odoo import api,models,fields
import logging


_logger = logging.getLogger(__name__)
class ShareApplicantData(models.Model):
    _name = 'share.applicant.data'
    
    applicant_id = fields.Many2one('applicant_id')
    partner_id = fields.Many2one('res.partner', string='Partner')
    shared_company = fields.Many2one('res.partner')
    stage_status = fields.Many2one('hr.recruitment.stage')
    shared_date = fields.Date('Shared Date',copy = False)

class experience_summary(models.Model):
    _name = 'experience.summary'

    # applicant_id = fields.Many2one('applicant_id')
    partner_id = fields.Many2one('res.partner', string='Partner')
    summary_detail = fields.Text('Summary')
    applicant_id = fields.Many2one('hr.applicant')
