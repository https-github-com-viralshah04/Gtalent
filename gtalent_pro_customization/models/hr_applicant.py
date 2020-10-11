from odoo import api,models,fields, tools, _
import logging
import base64

AVAILABLE_RATINGS = [
    ('1', 'Poor'),
    ('2', 'Poor'),
    ('3', 'Normal'),
    ('4', 'Normal'),
    ('5', 'Normal'),
    ('6', 'Good'),
    ('7', 'Good'),
    ('8', 'Excellent'),
    ('9', 'Excellent'),
    ('10', 'Excellent'),
]

_logger = logging.getLogger(__name__)
class InheritHrApplicant(models.Model):
    _inherit = 'hr.applicant'
    
    
    progress_rate = fields.Integer(string='Sample Rate')
    maximum_rate = fields.Integer(string='Maximum Rate')
#     Adding custom fields
    is_alumni = fields.Boolean('Is an Alumni?')
    
    ai_interview_status = fields.Selection([('yet_to_start','Yet to Start'),
                                            ('scheduled','Scheduled'),
                                            ('completed','Completed')],
                                            copy=False,
                                            string = 'AI Interview Status',
                                            help= "Applicant's AI Interview Status")

    prelive_interview_status = fields.Selection([('yet_to_start','Yet to Start'),
                                            ('scheduled','Scheduled'),
                                            ('completed','Completed')],
                                            copy=False,
                                            string='PreLive Interview Status',
                                            help= "Applicant's Prelive Interview Status")

    app_gender = fields.Selection([('male','Male'),('female','Female')],
                             copy = False,
                             string = 'Gender',
                             help = 'Gender of the applicant')
    nationality = fields.Char("Nationality",
                             copy = False,
                             help='Nationality of the applicant')
    language = fields.Char('Language',
                         copy = False, 
                         help = 'Language of the applicant')
    category = fields.Char('Category',
                         copy = False,
                         help = 'Category of the applicant')
    aadhar_number = fields.Char('Aadhar Number',
                             copy =  False,
                             help = 'Aadhar number of the applicant')
    source = fields.Char('Source',
                         copy = False,
                         help ='Soucrce of the applicant')
    uploaded_by  = fields.Char('Uploaded By',
                             copy = False,
                             help ='Uploaded By')
    candidate_type = fields.Selection([('fresh','Fresh'),('lateral','Lateral'),('contractor','Contractor')],
                                string='Candidate Type',
                                copy = False,
                                help='Type of the applicant')
    candidate_exp = fields.Char('Candidate Experience',
                                 copy = False,
                                 help = 'Experience of the applicant')
    candidate_birth_date = fields.Date('Birth Date',
                                 copy = False,
                                 help = 'Candidate Birth Date')
    visa_info = fields.Char('Visa Information',
                             copy = False,
                             help = 'Visa Information'
                             )
    blood_group = fields.Char('Blood Group',
                               copy = False,
                               help = 'Blood Group of the candidate')
    emergency_contact_number = fields.Integer('Emergency Contact Number',
                                               copy=False,
                                               help='Emergency Contact Number of the applicant')
     
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
        ], string='Address Type',
        default='contact',
        help="Used by Sales and Purchase Apps to select the relevant address depending on the context.")
    
    recruitment_industry_id = fields.Many2one('hr.recruitment.industry', 'Industry')
    
    applicant_college = fields.Many2one('res.partner',string = 'College')
    current_designation = fields.Char(string = 'Current Designation',
                                      copy  =  False,
                                      help = 'Current Designation of the applicant')
    app_yrs_of_exp = fields.Integer(string = 'Years of Experience',
                                    copy = False,
                                    help = "Applicant's Years of Experience")
    
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    
    #Social Media Related fields
    social_twitter_acc = fields.Char('Twitter Account')
    social_facebook_acc = fields.Char('Facebook Account')
    social_github_acc = fields.Char('GitHub Account')
    social_linkedin_acc = fields.Char('LinkedIn Account')
    social_youtube_acc = fields.Char('Youtube Account')
    social_googleplus_acc = fields.Char('Google+ Account')
    social_instagram_acc = fields.Char('Instagram Account')

    
    #Educational Related Fields
    educational_type_id = fields.One2many('applicant.college.list','applicant_id',string='Educational Details')
    skills_rating  = fields.Selection(AVAILABLE_RATINGS, "Ratings", default='1')
    notice_availability = fields.Selection([('immediate','Immediate'),
                                              ('30_days','30 Days'),
                                              ('60_days','60 Days'),
                                              ('90_days','90 Days')
                                              ],copy = False)
    #Employment Related fields
    employment_type_id = fields.Many2many('applicant.employment',string='Employment Details')
    hobbies_id = fields.One2many('hr.recruitment.hobbies','applicant_id',string='Hobbies')
    shared_applicant_info_ids = fields.One2many('share.applicant.data','applicant_id')
    experience_summary_ids = fields.One2many('experience.summary','applicant_id')
    college_name = fields.Char('College Name',
                               copy = False,
                               help = 'Please specify the college name from where the degree was completed')
    applicant_image = fields.Binary("Applicant's Image",
                                    copy = False,
                                    help='Image of the Applicant')
    image_128 = fields.Image("Image")

    #Assessment Page Related Details
    #Relational fields
    assesment_type_id = fields.Many2many('hr.recruitment.assessment',string= "Assessment")
    sequence = fields.Integer(index=True, help="Gives the sequence order when displaying a list of bank statement lines.", default=1)
    
    experience_summary_info = fields.Html("Summary",help = 'Notes of experience summary',
                                          copy = False)

    #Smart Link Related Fields
    education_count = fields.Integer('# Education',compute = '_compute_degree_count')
    experience_count = fields.Integer('# Experience',compute = '_compute_experience_count')
    skills_count = fields.Integer('# Skills',compute = '_compute_skills_count')
    assessment_count = fields.Integer('# Assessment',compute = '_compute_assessment_count')
    projects_count = fields.Integer('# Projects',compute = '_compute_project_count')
    total_count = fields.Integer("#Total",compute = '_compute_course_cert_awards_count')
    course_count = fields.Integer("#Courses",compute = '_compute_course_cert_awards_count')
    certification_count = fields.Integer('# Certification',compute = '_compute_certificate_count')
    awards_count = fields.Integer("#Awards",compute = '_compute_awards_count')
    
    #Project Related fields
    project_id = fields.Many2many('applicant.project',string='Projects')
    
    #Certificates and Awards Related fields
    course_id = fields.One2many('applicant.courses','applicant_id',string='Course Details')
    certificate_id = fields.One2many('applicant.certificate','applicant_id',string='Certificate Details')
    awards_id = fields.One2many('applicant.awards','applicant_id',string='Award Details')
    
    #Skill Related Fields
    applicant_skill_ids = fields.One2many('hr.employee.skill', 'applicant_id', string="Skills")

    # @api.model
    # def create(self, vals):
    #     print("VALS :---------------1------------>>>>>>>>>>>>> ",vals)
    #     res = super(InheritHrApplicant, self).create(vals)
    #     print("VALS :-----------------1---------->>>>>>>>>>>>> ",vals,res,res.attachment_ids)
    #
    #     return res



            
    def create_hr_applicant(
        self, email, username, partner_mobile,
        candidate_birth_date, current_designation,
        app_yrs_of_exp, app_gender, nationality,
        aadhar_number, street, street2, city, zipcode, country_id, state_id):
        applicants = self.create({
                'name': username,
                'partner_name': username,
                'email_from': email,
                'partner_mobile': partner_mobile,
                'candidate_birth_date': candidate_birth_date,
                'current_designation': current_designation,
                'app_yrs_of_exp': app_yrs_of_exp,
                'app_gender': app_gender,
                'nationality': nationality,
                'aadhar_number': aadhar_number,
                'street': street,
                'street2': street2,
                'city': city,
                'zip': zipcode,
                'country_id': country_id,
                'state_id': state_id
            }
        )
        return applicants

    #Over-riding default method of creation of employee from applicant
    def create_employee_from_applicant(self):
        _logger.info("EMPLOYEE--APPLICANT METHOD CALLED")
        employee_vals = {}
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                #Preparing employee dictionary to be sent for employee creation
                employee_vals =  {
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id or False,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                            and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.phone or False,
                    }
                #Optional fields
                if applicant.ai_interview_status : 
                    employee_vals['emp_ai_interview_status'] = applicant.ai_interview_status 
                    
                if applicant.prelive_interview_status : 
                    employee_vals['emp_prelive_interview_status'] = applicant.prelive_interview_status 
                            
                if applicant.visa_info : 
                    employee_vals ['emp_visa_info']  = applicant.visa_info or False,
                    
                if applicant.category : 
                    employee_vals['emp_category']  = applicant.category or False,
                    
                if applicant.source : 
                    employee_vals['emp_source'] =  applicant.source or False,
                
                if applicant.uploaded_by :
                    employee_vals['emp_uploaded_by'] = applicant.uploaded_by or False,
                
                if applicant.candidate_type :
                    employee_vals['emp_candidate_type'] = applicant.candidate_type or False,
                
                if applicant.social_twitter_acc : 
                    employee_vals['emp_social_twitter_acc'] =  applicant.social_twitter_acc or False,
                    
                if applicant.social_facebook_acc : 
                    employee_vals['emp_social_facebook_acc'] =  applicant.social_facebook_acc or False,
                    
                if applicant.social_github_acc : 
                    employee_vals['emp_social_github_acc'] =  applicant.social_github_acc or False,
                    
                if applicant.social_linkedin_acc : 
                    employee_vals['emp_social_linkedin_acc'] =  applicant.social_linkedin_acc or False,
                    
                if applicant.social_youtube_acc : 
                    employee_vals['emp_social_youtube_acc']  = applicant.social_youtube_acc or False,
                    
                if applicant.social_googleplus_acc : 
                    employee_vals['emp_social_googleplus_acc'] = applicant.social_googleplus_acc or False
                    
                if applicant.social_instagram_acc : 
                    employee_vals['emp_social_instagram_acc'] = applicant.social_instagram_acc or False
                    
                if applicant.app_gender : 
                    employee_vals['gender'] = applicant.app_gender or False
                    
                if applicant.nationality :
                    employee_vals['emp_nationality'] = applicant.nationality or False
                    
                if applicant.blood_group  :
                    employee_vals['emp_blood_group'] = applicant.blood_group or False
                    
                if applicant.language  :
                    employee_vals['emp_language'] =  applicant.language or False
                    
                if applicant.aadhar_number : 
                    employee_vals['emp_aadhar_number'] = applicant.aadhar_number or False
                    
                if applicant.emergency_contact_number : 
                    employee_vals['emergency_contact'] = applicant.emergency_contact_number or False
                    
                if applicant.candidate_exp  :
                    employee_vals['emp_candidate_exp'] = applicant.candidate_exp or False
                    
                if applicant.candidate_birth_date :
                    employee_vals['birthday'] = applicant.candidate_birth_date or False
                    
                if applicant.recruitment_industry_id.id:
                    employee_vals['employee_industry_id'] = applicant.recruitment_industry_id.id or False
                
                if applicant.applicant_skill_ids.ids :
                    employee_vals['employee_skill_ids'] = applicant.applicant_skill_ids.ids or False
                    
                if applicant.educational_type_id.ids : 
                    employee_vals['employee_degree_type_id'] = applicant.educational_type_id.ids or False
                    
                if applicant.employment_type_id.ids : 
                    employee_vals['employee_employment_type_id'] = applicant.employment_type_id.ids or False
                    
                if  applicant.assesment_type_id.ids :
                    employee_vals['employee_assessment_id'] =  applicant.assesment_type_id.ids or False
                    
                if applicant.course_certificate_id.ids  :
                    employee_vals['employee_applicant_certificate_id'] = applicant.course_certificate_id.ids or False
                
                if applicant.project_id.ids  :
                    employee_vals['employee_project_id'] = applicant.project_id.ids or False
                    
                if applicant.hobbies_id.ids : 
                    employee_vals['employee_recruitment_hobbies_id'] =  applicant.hobbies_id.ids or False
                
                
                
                employee = self.env['hr.employee'].create(employee_vals)
                applicant.write({'emp_id': employee.id})
                if applicant.job_id:
                    applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                    applicant.job_id.message_post(
                        body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                        subtype="hr_recruitment.mt_job_applicant_hired")
                applicant.message_post_with_view(
                    'hr_recruitment.applicant_hired_template',
                    values={'applicant': applicant},
                    subtype_id=self.env.ref("hr_recruitment.mt_applicant_hired").id)

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window
    
    @api.model
    def default_get(self, fields):
        res = super(InheritHrApplicant, self).default_get(fields)
        _logger.info("CONTEXT  of HR APPLICANT IS -!!!!!!!!!!!!!!!!!!!!!!--> {}".format(self._context))
        return res
    
    def _compute_assessment_count(self):
        '''This method will compute total number of
        assessments against the applicant'''
        _logger.info("Attempting Assessment Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.assesment_type_id : 
                _logger.info("Assessment Length is ---> {}".format(len(rec.assesment_type_id)))
                self.assessment_count =  len(rec.assesment_type_id)
            else:
                _logger.info("Assessment Data not field")
                self.assessment_count = 0
                
                
    def _compute_degree_count(self):
        '''This method will compute total number of
        degrees against the applicant'''
        _logger.info("Attempting Degrees Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.educational_type_id : 
                _logger.info("Degree Length is ---> {}".format(len(rec.educational_type_id)))
                self.education_count =  len(rec.educational_type_id)
            else:
                _logger.info("Degree Data not field")
                self.education_count = 0

                 
    def _compute_project_count(self):
        '''This method will compute total number of
        project against the applicant'''
        _logger.info("Attempting Project Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.project_id : 
                _logger.info("Project Length is ---> {}".format(len(rec.project_id)))
                self.projects_count =  len(rec.project_id)
            else:
                _logger.info("Project Data not field")
                self.projects_count = 0
    def _compute_course_cert_awards_count(self):
        '''
        This method will give the total number of count of courses,certificates
        and awards against an applicant
        '''
        _logger.info("Attempting to fetch Course,Certificates and Awards Count")
        count_all = []
        for rec in self : 
            if rec.course_id : 
                course_number = self._compute_course_count()
                count_all.append(course_number)
            if rec.certificate_id : 
                certificate_number = self._compute_certificate_count()
                count_all.append(certificate_number)
            if rec.awards_id :
                award_number = self._compute_awards_count()
                count_all.append(award_number)
            _logger.info("LIST IS ---> {}".format(count_all))
            _logger.info("COUNTS IS ---> {}".format(sum(count_all)))
            self.total_count = sum(count_all)
            
            
            
    def _compute_certificate_count(self):
        '''
        This method will list the number of
        certificates against the applicant
        '''
        _logger.info("Attempting Certificate Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.certificate_id : 
                _logger.info("Certificate Length is ---> {}".format(len(rec.certificate_id)))
                self.certification_count =  len(rec.certificate_id)
                return self.certification_count
            else:
                _logger.info("Certificate Data not filled")
                self.certification_count = 0
                return self.certification_count
                
                
    def _compute_course_count(self):
        '''
        This method will list the number of
        courses against the applicant
        '''
        _logger.info("Attempting Courses Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.course_id : 
                _logger.info("Course Length is ---> {}".format(len(rec.course_id)))
                self.course_count =  len(rec.course_id)
                return self.course_count
            else:
                _logger.info("Course Data not filled")
                self.course_count = 0
                return self.course_count
 
   
    def _compute_awards_count(self):
        '''
        This method will list the number of
        awards against the applicant
        '''
        _logger.info("Attempting Awards Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.awards_id : 
                _logger.info("Award Length is ---> {}".format(len(rec.awards_id)))
                self.awards_count =  len(rec.awards_id)
                return self.awards_count
            else:
                _logger.info("Awards Data not filled")
                self.awards_count = 0
                return self.awards_count
        
        
    def _compute_experience_count(self):
        '''
        This method will list the number of 
        experience count against the applicant
        '''
        _logger.info("Attempting Experience Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.employment_type_id : 
                _logger.info("Experience Length is ---> {}".format(len(rec.employment_type_id)))
                self.experience_count =  len(rec.employment_type_id )
            else:
                _logger.info("Experience Data not filled")
                self.experience_count = 0
                
                
    def _compute_skills_count(self):
        '''
        This method will list the number of 
        skills count against the applicant
        '''
        _logger.info("Attempting Skills Count")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            if rec.applicant_skill_ids : 
                _logger.info("Applicant Skill ID's ---> {}".format(len(rec.applicant_skill_ids)))
                self.skills_count = len(rec.applicant_skill_ids)
            else : 
                _logger.info("Skills Data not filled")
                self.skills_count = 0
                
                
    def test_share(self):
        #print("sddfdggfg")
        wizard_action = {
                'name': 'Share',
                'view_mode': 'form',
                'res_model': 'applicants.share.wizard',
                'views': [(self.env.ref('gtalent_pro_customization.applicants_share_wizard_view').id, 'form')],
                'type': 'ir.actions.act_window',
            }
        #print("sd",wizard_action)
        
    @api.model
    def action_applicants_share(self):
        _logger.info("Attempting to share Applicants to the company Requested")
        
        context = self._context or {}
        return {
            'name': 'SHare',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('gtalent_pro_customization.applicants_share_wizard_view').id,
            'res_model': 'applicants.share.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }
#         applicants_data = {}
#         wizard_action = {
#                 'name': 'Share',
#                 'view_mode': 'form',
#                 'res_model': 'applicants.share.wizard',
#                 'target' : 'new',
#                 'views': [(self.env.ref('gtalent_pro_customization.applicants_share_wizard_view').id, 'form')],
#                 'type': 'ir.actions.act_window',
#             }
#         print("sd",wizard_action)
#         return wizard_action
        #Make All the selected talents visible to the Recruitment Company
#         template = self.env.ref('gtalent_pro_customization.applicants_share_wizard_view')
#         print("assssssssssssssssssssss",template)
#         return {
#             'name': 'Share Applicants',
#             'type': 'ir.actions.act_window',
#             'res_model': 'applicants.share.wizard',
# #             'views': [(template.id, 'tree')],
# #             'view_mode' : 'tree,form',
#         }
# #             applicants_data = {
#                 'applicant_id' : rec.id,
#                 'college': rec.applicant_college.id
#                 }
#             share_data = self.env['hr.talents'].sudo().create(applicants_data)
#             _logger.info("Shared Data is --> {}".format(share_data))

    def send_application_acknowledgement(self):
        for applicant in self:
            template_id = self.env.ref(
                'gtalent_pro_customization.mail_template_application_acknowledgement')
            if template_id:
                template_id.sudo().with_context(email_to=','.join(
                    [str(applicant.user_id.partner_id.email)])).send_mail(self.id, force_send=True)


class InheritHREmployeeSkills(models.Model):
    _inherit = 'hr.employee.skill'
        
    employee_id = fields.Many2one('hr.employee',required = False)
    applicant_id = fields.Many2one('hr.applicant')
    partner_id = fields.Many2one('res.partner')
    primary_skill = fields.Char(string='Primary Skills')
    secondary_skill = fields.Char(string='Secondary Skills')

    @api.constrains('skill_type_id', 'skill_level_id')
    def _check_skill_level(self):
        return True


class InheritRecruitmentDegree(models.Model):
    _inherit = "hr.recruitment.degree"
   
    
        
        