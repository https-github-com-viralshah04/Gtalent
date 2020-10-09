from odoo import api,models,fields
from odoo.exceptions import ValidationError


class ApplicantCourses(models.Model):
    _name = 'applicant.courses'
    _description = "Applicant's Courses"

    partner_id = fields.Many2one('res.partner', string='Partner')
    applicant_id = fields.Many2one('hr.applicant')

    #Course Related Fields
    course_vendor = fields.Char('Vendor',copy = False)
    course = fields.Char(string = 'Course',
                         copy=False,
                         help = 'Course')
    course_name = fields.Char(string = 'Name',
                              copy = False)
    course_technology = fields.Char('Technology',
                                    copy = False,
                                    help = 'Course Technology')
    course_status = fields.Char('Status')
    course_duration = fields.Char('Duration',
                                  copy=False,
                                  help='Month/Year of Course Start')
    course_start = fields.Date('Start Date',
                               copy = False,
                               help = 'Start Date')
    course_end = fields.Date('End Date',
                            copy=False,
                            help='Month/Year of Course Completion')
    
    course_documents_filename = fields.Char('Details')
    course_documents = fields.Binary('Documents',
                                    copy = False,
                                    help = 'Documents')
    
class ApplicantCertificates(models.Model):
    _name = 'applicant.certificate'
    _description = "Applicant's Certificate List"
    
    _sql_constraints = [
        ('name_uniq', 'CHECK(1=1)', 'The name of the Certificate must be unique!')
    ]
        
    applicant_id = fields.Many2one('hr.applicant')
    partner_id = fields.Many2one('res.partner', string='Partner')

    #Certificate Related Fields
    certificate_vendor = fields.Char('Vendor',copy = False)
    
   
    certificate_name = fields.Char(string = 'Name',
                              copy = False)
    
    certificate_id = fields.Char('Certification ID',
                                   copy = False,
                                   help='Certification ID')
    certificate_level = fields.Selection([('entry_level','Entry Level'),
                                          ('intermediate','Intermediate'),
                                          ('advance','Advance')])
    
    certificate_technology = fields.Char('Technology',
                                    copy = False,
                                    help = 'Course Technology')
   
    
    certificate_documents_filename = fields.Char('Details')
    certificate_documents = fields.Binary('Documents',
                                    copy = False,
                                    help = 'Documents')
    
    

    
class ApplicantAwards(models.Model):
    _name = 'applicant.awards'
    _description = "Applicant's Awards List"
    _order = "award_name"
       
    applicant_id = fields.Many2one('hr.applicant')
    partner_id = fields.Many2one('res.partner', string='Partner')

    #Award Related fields
    award_name = fields.Char('Award Name',
                             copy = False,
                             help='Award Name')
    present_by = fields.Char('Present By',
                             copy = False,
                             help='Present By')
    award_year = fields.Integer('Award Year',
                             copy = False,
                             size =4,
                             help = 'Award Year')
    
    @api.constrains('award_year')
    def _check_award_year(self):
        for record in self:
            awd_year = str(record.award_year)
            if (len(awd_year)) != 4:
                raise ValidationError('Please Enter Valid Award Year upto 4 digits')
            
