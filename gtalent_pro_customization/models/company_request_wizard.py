from odoo import api,models,fields
from datetime import datetime
import logging



_logger = logging.getLogger(__name__)
class CompanyRequestWizard(models.TransientModel):
    _name = 'company.request.wizard'
    
    company_request_date = fields.Date("Date", default=datetime.today())
    company_name = fields.Char('Company Name')
    college_name = fields.Char('College Name')
    industry_name = fields.Many2one('hr.recruitment.industry')
    candidate_type = fields.Selection([('fresher','Fresher'),
                                       ('experienced','Experienced')
                                       ],copy =  False)
    college_specialization = fields.Char(' Specialization')
    company_applicant_request = fields.Char("Number of Applicants to be Requested",
                                            copy = False,
                                            help = 'Number of applicant to be requested')
    
    @api.model
    def default_get(self, fields):
        res = super(CompanyRequestWizard, self).default_get(fields)
        _logger.info("CONTEXT IS ---> {}".format(self._context))
        rec_obj = self.env['res.partner'].browse(self.env.context['active_id'])
        _logger.info("Record is ---> {}".format(rec_obj))
        company_obj = self.env['res.users'].search([('id','=',self.env.uid)])
        _logger.info("LOGGED IN USER IS --->".format(company_obj.name))
        res.update({
            'company_name': company_obj.name,
            'college_name': rec_obj.name,
        })
        _logger.info("RES IS ---> {}".format(res))
        if rec_obj.college_specialization : 
            res['college_specialization'] =  rec_obj.college_specialization
        _logger.info("RES IS ---> {}".format(res))
        return res

    
    def send_company_request(self):
        '''
        Send applicant request from company to colleges
        '''
        _logger.info("Attempting to send applicants request to colleges")
        rec_obj = self.env['res.partner'].browse(self.env.context['active_id'])
        company_obj = self.env['res.users'].search([('id','=',self.env.uid)])
        _logger.info("LOGGED IN USER IS ---> {}".format(company_obj.name))
        #print("comp id",company_obj.partner_id,self.id)
        _logger.info("Record is ---> {}".format(rec_obj))
        dict_vals = {
                    'request_date' : self.company_request_date,
                    'company_ref'  : company_obj.partner_id.id,
                    'college_ref' : rec_obj.id,
#                     'company_request' : self.company_name,
#                     'request_to' : self.college_name,
                    'industry_name': self.industry_name.name,
                    'candidate_type': self.candidate_type,
                    'specialization' : self.college_specialization,
                    'no_of_applicants_requested': self.company_applicant_request
                    
                }
        _logger.info("Dictionary values getting sent for creation are as follows ---> {}".format(dict_vals))
        request_send = self.env['companies.requests'].create(dict_vals)
        if request_send : 
            request_success = rec_obj.sudo().update({'request_state' :'request_pending' })
            _logger.info("Request Sent Successfully ---> {}".format(request_success))
            
        else : 
            _logger.info("Sorry,the request was not sent")