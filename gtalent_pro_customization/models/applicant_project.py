from odoo import api,models,fields


class ApplicantDesignation(models.Model):
    _name = 'applicant.project'
    _description = "Applicant's Projects List"
    _order = "name"
    
    _sql_constraints = [
        ('project_uniq', 'CHECK(1=1)', 'The name of the Projects must be unique!')
    ]

    name = fields.Char(string = ' Project Name', translate=True)
    
    recruitment_industry_id = fields.Many2one('hr.recruitment.industry', 'Industry')
    
    project_for = fields.Selection([('college','College'),('corporate','Corporate'),
                                    ('freelancer','Freelancer'),('capstone','Capstone')],
                                    copy = False,
                                    help = 'Project For')
    project_link = fields.Char('Project Link',
                               copy = False,
                               help = 'Project Link')
    
    technology = fields.Char(string = 'Technology',
                             copy = False)
    
    team_size =  fields.Integer(string = 'Team Size',
                             copy = False,
                             help='Team size of the Project')
    
    project_start_date = fields.Date('Project Start Date',
                                     copy = False,
                                     help= 'Start Date of the Project')
    
    project_end_date = fields.Date('Project End Date',
                                     copy = False,
                                     help= 'End Date of the Project')
    
    project_duration = fields.Char('Project Duration',
                                   copy =False,
                                   help = 'Duration of the project')
    
    impact = fields.Char('Impact',
                         copy = False,
                         help = 'Impact of the project')
    
    guided_by  = fields.Char('Guided By',
                             copy = False,
                             help = 'Guidance in the project')
    project_summary  = fields.Html('Project Summary',
                                   copy = False,
                                   help = 'Summary of the project')
    
    project_accomplishments = fields.Html('Project Accomplishments',
                                          copy = False,
                                          help = 'Accomplishents made by the project')

    partner_id = fields.Many2one('res.partner')
