from odoo import api,models,fields
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)
class ApplicantCollegeList(models.Model):
    _name = 'applicant.college.list'
    _description = "Applicant's College List"
    _sql_constraints = [
        ('college_uniq', 'CHECK(1=1)', 'The name of the College must be unique!')
    ]
    
    degree_type = fields.Many2one('hr.recruitment.degree',string='Degree')
    degree_type_id = fields.Many2one('hr.recruitment.degree.type',string = 'Type')
    degree_score = fields.Integer('Score',copy = False)
    degree_start_year = fields.Char('Start Year',
                                    copy = False,
                                    limit = 4,
                                    help = 'Start year of the degree')
    degree_end_year = fields.Char('End Year',
                                    limit = 4,
                                     copy = False,
                                     help = 'End year of the degree')
    degree_percentage = fields.Float('Percentage (%)',
                                    copy = False,
                                    help = 'Percentage scored')
    
    degree_class = fields.Selection([('first_class_with_distinction','First Class with Distinction'),
                                     ('first_class','First Class'),
                                     ('second_class','Second Class'),
                                     ('third_class','Third Class'),
        ],string ='Class')
    upload_certifcate = fields.Binary('Documents',copy = False,help = 'Certificate to be uploaded')
    upload_certificate_filename = fields.Char("Image Filename")
    applicant_id = fields.Many2one('hr.applicant')
    name = fields.Many2one('res.partner',string = 'College')
    partner_id = fields.Many2one('res.partner',string = 'Partner')
    institute = fields.Many2one('res.partner',string = 'Institute')
    sequence = fields.Integer("Sequence", default=1, help="Gives the sequence order when displaying a list of colleges.")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    
    @api.constrains('degree_start_year','degree_end_year')
    def _check_degree_start_year(self):
        for record in self:
            start = str(record.degree_start_year)
            end = str(record.degree_end_year)
            if (len(start)) != 4:
                raise ValidationError('Please Enter Start  year upto 4 digits')
            if (len(end)) != 4 :
                raise ValidationError('Please Enter End Year upto 4 digits')
            if start > end :
                raise ValidationError("Please check the Years Entered")
            
    @api.onchange('name')
    def onchange_name(self):
        if not self.name:
                return
        
        else :
            self.street = self.name.street
            self.street2 = self.name.street2
            self.zip = self.name.zip
            self.city = self.name.city
            self.state_id = self.name.state_id
            self.country_id = self.name.country_id
            
