from odoo import api,models,fields
from datetime import date
from dateutil.relativedelta import relativedelta




class ApplicantEmployment(models.Model):
    _name = 'applicant.employment'
    _description = "Applicant's Employee List"

    #Adding Employment Related field
    upload_employment_attachment =  fields.Binary(string = 'Documents',
                                                  copy = False,
                                                  help = 'Attach Documents related to Employment Details')
    employment_attachment_filename = fields.Char('Details')
    applicant_id = fields.Many2one('hr.applicant')
    partner_id = fields.Many2one('res.partner')
    designation_type_id = fields.Char(string = 'Designation')
    department_type_id = fields.Char(string='Department')
    deliverables = fields.Html(string = 'Deliverables')
    job_summary = fields.Html(string='Job Summary')
    company_name = fields.Many2one('res.partner')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    employment_start_date = fields.Date('Start Date',
                                        copy = False,
                                        help = 'Employment Start Date')
    employment_end_date = fields.Date('End Date',
                                        copy = False,
                                        help = 'Employment End Date')
    job_accomplishments = fields.Html(string = 'Job Accomplishments',
                                      copy = False)
    job_tenure = fields.Char('Job Tenure',
                             copy = False,
                             help = 'Job Tenure')
    emp_duration = fields.Float("Duration")
    
    
    @api.onchange('employment_start_date','employment_end_date')
    def calculate_duration(self):
        '''
        This method will calculate the duration between specified days
        '''
        if self.employment_end_date and self.employment_start_date:
            duration = self.employment_end_date - self.employment_start_date
    #         difference_in_years = relativedelta(self.employment_end_date, self.employment_start_date).months
    #         self.emp_duration = difference_in_years
            emp_duration = duration
        
    