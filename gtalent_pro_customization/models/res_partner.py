from odoo import api,models,fields
import logging
import uuid


_logger = logging.getLogger(__name__)
class InheritResPartner(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'name'
    
    #Adding custom fields
    gtalent_users = fields.Selection([('candidate','Candidate'),
                                      ('campus','Campus'),
                                      ('employer','Employer'),
                                      ('recruitment_vendor','Recruitment Vendor')
                                      ],
                                      default = 'candidate',
                                      copy = False)
    is_connect = fields.Boolean('Connect',copy = False)
    college_type = fields.Char("College Type",
                               copy = False,
                               help = 'Type of college')
    university_name = fields.Char("University Name", translate=True)
    university_type = fields.Char("University Type",
                                  copy = False,
                                  help = 'Type of University')
    college_email = fields.Char("Email",translate=True)
    college_contact =fields.Char("Contact",copy = False,
                                 help = 'Contact Number of College')
    college_founded_in = fields.Char('College Founded In',
                                     copy = False,
                                     help = 'College Founded In')
    number_of_students = fields.Char("Number of Students",
                                     copy = False,
                                     help = 'Number of Students')
    placement_ratio = fields.Char("Placement Ratio",
                                  copy = False,
                                  help = 'College Placement Ratio')
    college_website = fields.Char("College Website",
                                  copy = False,
                                  help = 'College Website')
    college_management = fields.Char('Management',
                                     copy = False,
                                     help = 'College Management')
    college_year_establishment = fields.Date("Year of Establishment",
                                             copy = False,
                                             help = 'Year of Establishment')
    college_specialization = fields.Char("College Specialization",
                                         copy = False,
                                         help = 'College Specialization')
    college_location = fields.Char("Location",
                                   copy = False,
                                   help = 'Location of the college')
    
    request_state = fields.Selection([('open','Open'),
                                      ('connect_email_sent','Connect'),
                                      ('request_pending','Request Pending'),
                                      ('request_approved','Request Approved')
                                      ],default = 'open')
     

    placement_details_id = fields.One2many('campus.placement.details','campus_id',string='Placement Details')

     
     
    is_recruitment_company = fields.Boolean('Is A Recruitment Company?',
                                       copy = False,
                                       help = 'If set,will identify the record as Corporate Company')
    
    
    is_an_employer = fields.Boolean("Is an Employer?",
                                    copy = False,
                                    help = 'If set,will identify the record as an Employer')
    
    
    employer_about_company = fields.Text('About Company',placeholder = 'About Company',copy = False)

    company_vision = fields.Text('Company Vision',placeholder = 'Vision and Mission,Statement and Value',copy = False)
    company_offerings = fields.Text('Offerings and Services',placeholder = 'Offerings and Services',copy = False)
    company_registration = fields.Char(copy = False)
    number_of_employees = fields.Integer(copy = False)
    yearly_business = fields.Integer(copy = False)
    achievements = fields.Text(copy = False)
    
    total_applicants = fields.Integer("#Applicants",compute = '_compute_applicants_count')

    app_gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                                  copy=False,
                                  string='Gender',
                                  help='Gender of the applicant')

    nationality = fields.Char("Nationality",
                              copy=False,
                              help='Nationality of the applicant')
    language = fields.Char('Language',
                           copy=False,
                           help='Language of the applicant')
    aadhar_number = fields.Char('Aadhar Number',
                                copy=False,
                                help='Aadhar number of the applicant')
    blood_group = fields.Char('Blood Group',
                              copy=False,
                              help='Blood Group of the candidate')

    # Social Media Related fields
    social_twitter_acc = fields.Char('Twitter Account')
    social_facebook_acc = fields.Char('Facebook Account')
    social_github_acc = fields.Char('GitHub Account')
    social_linkedin_acc = fields.Char('LinkedIn Account')
    social_youtube_acc = fields.Char('Youtube Account')
    social_googleplus_acc = fields.Char('Google+ Account')
    social_instagram_acc = fields.Char('Instagram Account')

    # Applicant fields
    date_of_birth = fields.Date('Date of Birth')
    registered_id = fields.Char('Registration ID',copy = False)
    gstn_id = fields.Char('Company GSTN',copy = False)
    affiliation_id = fields.Char('Affiliation ID',copy = False)
    years_of_exp = fields.Char('Years of Experience',copy = False)
    voter_id = fields.Char('Voter Id',copy=False)
    qualification  = fields.Char('Highest Qualification',copy = False)
    industry = fields.Many2one('hr.recruitment.industry', 'Industry')
    partner_skill_ids = fields.One2many('hr.employee.skill', 'partner_id', string="Skills")
    candidate_type = fields.Selection([('fresh', 'Fresh'), ('lateral', 'Lateral'), ('contractor', 'Contractor')],
                                      string='Candidate Type',
                                      copy=False,
                                      help='Type of the applicant')
    educational_type_id = fields.One2many('applicant.college.list', 'partner_id', string='Educational Details')
    employment_type_id = fields.Many2many('applicant.employment', string='Employment Details')
    hobbies_id = fields.One2many('hr.recruitment.hobbies', 'partner_id', string='Hobbies')
    shared_applicant_info_ids = fields.One2many('share.applicant.data', 'partner_id')
    experience_summary_ids = fields.One2many('experience.summary','partner_id')
    assesment_type_id = fields.Many2many('hr.recruitment.assessment',string= "Assessment")
    course_id = fields.One2many('applicant.courses','partner_id',string='Course Details')
    certificate_id = fields.One2many('applicant.certificate','partner_id',string='Certificate Details')
    awards_id = fields.One2many('applicant.awards','partner_id',string='Award Details')
    applicant_skill_ids = fields.One2many('hr.employee.skill', 'partner_id', string="Skills")
    project_id = fields.Many2many('applicant.project',string='Projects')
    experience_summary_info = fields.Html("Summary", help='Notes of experience summary',
                                          copy=False)
    applicant_id = fields.Many2one('hr.applicant',string='Related Applicant')
    visa_info = fields.Char('Visa Information',
                            copy=False,
                            help='Visa Information'
                            )
    category = fields.Char('Category',
                           copy=False,
                           help='Category of the applicant')
    source = fields.Char('Source',
                         copy=False,
                         help='Soucrce of the applicant')

    uploaded_by = fields.Char('Uploaded By',
                              copy=False,
                              help='Uploaded By')

    def view_applicants(self):
        '''
        This method will redirect to applicants 
        with all applicants shown of specific college
        '''
        _logger.info("View Applicants Method called")
        applicant_action = {
                'name': 'Applicants',
                'view_mode': 'tree,kanban',
                'res_model': 'hr.applicant',
                'views': [(self.env.ref('hr_recruitment.crm_case_tree_view_job').id, 'tree'), (self.env.ref('hr_recruitment.hr_kanban_view_applicant').id, 'kanban')],
                'type': 'ir.actions.act_window',
                'domain' : [('applicant_college','=',self.id)]
            }
        return applicant_action
    
    
    def view_campus_requests(self):
        '''
        This method will redirect to applicants 
        with all applicants shown of specific college
        '''
        _logger.info("View Campus Requests Method called")
        applicant_action = {
                'name': 'Campus Requests',
                'view_mode': 'tree,form',
                'res_model': 'companies.requests',
                'views': [(self.env.ref('gtalent_pro_customization.companies_applicants_requests_tree_view').id, 'tree'), (self.env.ref('gtalent_pro_customization.companies_requests_applicants_form_view').id, 'form')],
                'type': 'ir.actions.act_window',
            }
        return applicant_action
    
    
    def _compute_applicants_count(self):
        _logger.info("Applicants count called")
        for rec in self : 
            _logger.info("REC IS ---> {}".format(rec))
            total_app_count = self.env['hr.applicant'].search_count([('applicant_college','=',rec.id)])
            _logger.info("TOTAL APP COUNT ---> {}".format(total_app_count))
            if total_app_count : 
                rec.total_applicants = total_app_count
            else : 
                rec.total_applicants = 0
                
                
    def action_request_applicant(self):
        self.ensure_one()
        template = self.env.ref('gtalent_pro_customization.applicants_connect_request_template')
        _logger.info("TEMPLATE IS ---> {}".format(template))
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = dict(
            default_model='res.partner',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_light",
            force_email=True
        )
        return {
            'name': 'Connect',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
        
        
    def generate_unique_code(self):
        _logger.info("Attempting to generate unique code")
        uid = uuid.uuid4()
        str_uuid = str(uid)
        formatted_uuid = ''.join([x for x in str(uid) if x.isdigit()][0:6])
        return formatted_uuid
    
    
class InheritMailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'
    
    def send_mail(self, auto_commit=False):
        _logger.info("Attempting to override Send Mail")
        _logger.info("CONTEXT IS ---> {}".format(self._context))
        if 'is_connect' in self._context : 
            _logger.info("Attempting to send mail")
            rec_ids = self._context.get('active_ids')
            for rec in rec_ids : 
                _logger.info("RECORD IS ---> {}".format(rec))
                connected_obj = self.env['res.partner'].browse(int(rec))
                if connected_obj.exists  :
                    connected_obj.write({'request_state' : 'connect_email_sent'})
                    _logger.info("CONNECTION SUCCESSFULL VIA SERVER ACTION")
                else : 
                    _logger.info("Some Issue Ocurred via server action!")
        return super(InheritMailComposeMessage,self.with_context(mail_post_autofollow = True)).send_mail()
            
            

class CampusPlacementDetails(models.Model):
    _name = 'campus.placement.details'
    _description = "Campus Placement Details"
    
    campus_id = fields.Many2one('res.partner')
    
    
    placement_officer_name = fields.Char("Name",
                                         copy = False,
                                         help = 'Placement Officer Name')
    placement_officer_contact = fields.Char("Contact Number",
                                            copy = False,
                                            help = 'Placement Officer Contact Number')
    placement_officer_email = fields.Char("Email",
                                          copy = False,
                                          help = 'Email id of Placement Officer')
    placement_officer_position = fields.Selection([('placement_officer','Placement Officer'),
                                                   ('placement_head','Placement Head')],
                                                   string= 'Position',
                                                  copy = False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     