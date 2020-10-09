from odoo import api,models,fields
import logging


class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    #Adding Custom Fields
    emp_is_alumni = fields.Boolean('Is an Alumni?')
    
    emp_ai_interview_status = fields.Selection([('yet_to_start','Yet to Start'),
                                            ('scheduled','Scheduled'),
                                            ('completed','Completed')],
                                            copy=False,
                                            string = 'AI Interview Status',
                                            help= "Applicant's AI Interview Status")

    emp_prelive_interview_status = fields.Selection([('yet_to_start','Yet to Start'),
                                            ('scheduled','Scheduled'),
                                            ('completed','Completed')],
                                            copy=False,
                                            string='PreLive Interview Status',
                                            help= "Applicant's Prelive Interview Status")
    
    emp_gender = fields.Selection([('male','Male'),('female','Female')],
                             copy = False,
                             help = 'Gender of the applicant')
    emp_nationality = fields.Char("Nationality",
                             copy = False,
                             help='Nationality of the applicant')
    emp_language = fields.Char('Language',
                         copy = False, 
                         help = 'Language of the applicant')
    emp_category = fields.Char('Category',
                         copy = False,
                         help = 'Category of the applicant')
    emp_aadhar_number = fields.Char('Aadhar Number',
                             copy =  False,
                             help = 'Aadhar number of the applicant')
    emp_source = fields.Char('Source',
                         copy = False,
                         help ='Source of the applicant')
    emp_uploaded_by  = fields.Char('Uploaded By',
                             copy = False,
                             help ='Uploaded By')
    emp_candidate_type = fields.Selection([('fresh','Fresh'),('lateral','Lateral'),('contractor','Contractor')],
                                string='Candidate Type',
                                copy = False,
                                help='Type of the applicant')
    emp_candidate_exp = fields.Char('Candidate Experience',
                                 copy = False,
                                 help = 'Experience of the applicant')
    emp_candidate_birth_date = fields.Date('Birth Date',
                                 copy = False,
                                 help = 'Candidate Birth Date')
    emp_visa_info = fields.Char('Visa Information',
                             copy = False,
                             help = 'Visa Information'
                             )
    emp_blood_group = fields.Char('Blood Group',
                               copy = False,
                               help = 'Blood Group of the candidate')
    emp_emergency_contact_number = fields.Integer('Emergency Contact Number',
                                               copy=False,
                                               help='Emergency Contact Number of the applicant')
    
    
    employee_industry_id = fields.Many2one('hr.recruitment.industry', 'Industry')

    employee_degree_type_id =fields.Many2many('hr.recruitment.degree',string='Degree')
    employee_employment_type_id =fields.Many2many('applicant.employment',string='Details')
    employee_assessment_id =fields.Many2many('hr.recruitment.assessment',string='Assessment')
    employee_applicant_certificate_id =fields.Many2many('applicant.certificate',string='Certificate')
    employee_project_id =fields.Many2many('applicant.project',string='Project')
    employee_recruitment_hobbies_id =fields.Many2many('hr.recruitment.hobbies',string='Hobbies')

    #Social Media Related fields
    emp_social_twitter_acc = fields.Char('Twitter Account')
    emp_social_facebook_acc = fields.Char('Facebook Account')
    emp_social_github_acc = fields.Char('GitHub Account')
    emp_social_linkedin_acc = fields.Char('LinkedIn Account')
    emp_social_youtube_acc = fields.Char('Youtube Account')
    emp_social_googleplus_acc = fields.Char('Google+ Account')
    emp_social_instagram_acc = fields.Char('Instagram Account')
    
    
