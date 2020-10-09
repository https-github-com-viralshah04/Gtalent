from odoo import api,models,fields
from datetime import datetime
import logging



_logger = logging.getLogger(__name__)
class ApplicantsShareWizard(models.TransientModel):
    _name = 'applicants.share.wizard'
    _rec_name = 'companies'
    
    applicants_share_date = fields.Date("Date", default=datetime.today())
    companies = fields.Char('Company')
    college = fields.Char('College Name')
    industry_request = fields.Char('Industry')
    candidate = fields.Selection([('fresher','Fresher'),
                                       ('experienced','Experienced')
                                       ],copy =  False)
    college_specialization = fields.Char(' Specialization')
    applicant_request = fields.Char("Number of Applicants to be Requested",
                                            copy = False,
                                            help = 'Number of applicant to be requested')
    applicant_share = fields.Integer("Applicants Share",
                                  copy = False,
                                  help = 'Number of Applicants Shared')
    candidates= fields.Many2many('hr.applicant')

      
    @api.model
    def default_get(self, fields):
        res = super(ApplicantsShareWizard, self).default_get(fields)
        _logger.info("CONTEXT IS ---> {}".format(self._context))
        company_request_id  = self._context.get('company_request_id')
        company_request_obj = self.env['companies.requests'].search([('id','=',company_request_id)])
        if company_request_obj.exists() :
            _logger.info("COMPANY FOUND ---> {}".format(company_request_obj))
        res.update({
            'companies' : company_request_obj.company_ref.name,
            'college': company_request_obj.college_ref.name,
            'applicant_request' : company_request_obj.no_of_applicants_requested,
            'industry_request' : company_request_obj.industry_name,
            'candidate' : company_request_obj.candidate_type,
            'college_specialization' : company_request_obj.specialization
        })
        _logger.info("RES IS ---> {}".format(res))
        return res


    @api.onchange('candidates')
    def on_change_candidates(self):
        _logger.info("Attempting to check the number of candidates")
        self.applicant_share = len(self.candidates)
        
        
    def share_applicants(self):
        _logger.info("Attempting to share applicants with requested company")
        _logger.info("CONTEXT FOR SHARE APPLICANTS IS ---> {}".format(self._context))
        company_requested = self._context.get('company_request_id')
        _logger.info('Company Requested is ---> {}'.format(company_requested))
        applicant_dict = {}
        for rec in self.candidates:
            applicant_dict = {
                'name'  : rec.name,
                'applicant_college' : rec.applicant_college.id,
                'app_gender' : rec.app_gender,
                'nationality' : rec.nationality,
                'aadhar_number' : rec.aadhar_number,
                'city' : rec.city,
                'source' : rec.source
                }
            _logger.info("Applicant Dictionary Is ---> {}".format(applicant_dict))
            talent_obj = self.env['hr.applicant'].sudo().create(applicant_dict)
            _logger.info("Talent Object is ---> {}".format(talent_obj))
            _logger.info("COLLEGE IS ---> {}".format(rec.applicant_college.id))
            college_partner = self.env['res.partner'].search([('id','=',rec.applicant_college.id)])
            company_request = self.env['companies.requests'].search([('id','=',company_requested)])
            _logger.info("College and Company is ---> {} {}".format(college_partner,company_request))
            if college_partner : 
                #Change the status to Approved
                college_partner.write({'request_state' : 'request_approved'})
            if company_request : 
                company_request.write({'request_status' : 'approved'})
            _logger.info("Process successful!")












