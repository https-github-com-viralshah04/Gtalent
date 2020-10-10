from odoo import api,models,fields
from datetime import datetime
import logging


_logger = logging.getLogger(__name__)
class CompaniesRequests(models.Model):
    _name = 'companies.requests'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'company_ref'
    
    
    company_request = fields.Char(copy = False)
    request_to = fields.Char('Request To',copy = False)
    college_ref = fields.Many2one('res.partner')
    company_ref = fields.Many2one('res.partner')
    industry_name = fields.Char('Industry')
    candidate_type = fields.Char('Candidate Type')
    specialization = fields.Char('Specialization')
    no_of_applicants_requested  = fields.Char('Number of Applicants Requested',
                                            copy =  False,
                                            help = 'Number of Applicants Requested')
    request_date = fields.Date('Request Date',
                       copy = False,
                       help = 'Company Requested Date')
    applicant_specialization = fields.Many2one('hr.recruitment.industry', "Applicant's Specialization")
    request_status = fields.Selection([('pending','Pending'),
                                       ('approved','Approved')],
                                       default = 'pending')

    def approve_company_request(self):
        '''
        This function will approve the company request and share the details of the applicants requested.
        '''
        _logger.info("Approval of Company Requests")
        #Make request as Approved against the company
#         company_id = self.partner_id
#         update_approved_state = company_id.sudo().update({'request_state'  :'request_approved'})

        #Open List View of Applicants
        #print("CONTEXT IS --->",self)
        ctx = self._context.copy()
        #print("sds",ctx)
        ctx['company_request_id'] = self.id
        self.ensure_one()
        #print("APPROVE ##############################CONTEXT ",ctx)
        template = self.env.ref('gtalent_pro_customization.applicants_share_wizard_view')
        return {
            'name': 'Share Applicants',
            'type': 'ir.actions.act_window',
            'res_model': 'applicants.share.wizard',
            'view_mode' : 'form',
            'views': [(template.id, 'form')],
            'context' : ctx
        }
        
#         return {
#             'name': 'SHare',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'view_id': self.env.ref('gtalent_pro_customization.applicants_share_wizard_view').id,
#             'res_model': 'applicants.share.wizard',
#             'type': 'ir.actions.act_window',
#             'target': 'new',
#             'context': context
#         }
        
        
        
