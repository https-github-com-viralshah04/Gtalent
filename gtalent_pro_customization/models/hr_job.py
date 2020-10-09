from odoo import api, models, fields


class Job(models.Model):
    _inherit = "hr.job"

    job_role = fields.Char(string='Job Role')
    company_id = fields.Many2one('res.company', string='Company Name')
    industry_type_id = fields.Many2one(
        'hr.recruitment.industry', string="Industry Type")
    experience_year = fields.Char(string='Years of Experience')
    experience_month = fields.Char(string='Month of Experience')
    work_location = fields.Char(string='Work Location')
    candidate = fields.Char(string='Candidate')
    # job_description = fields.Char(string='Job Description')
    job_type = fields.Selection(
        [('permanent', 'Permanent'), ('contract', 'Contract'), ('intern', 'Intern')], string='Job Type')
    candidate_type = fields.Selection([('experience', 'Experience'), (
        'fresher', 'Fresher'), ('contractor', 'Contractor')], string='Candidate Type')

    company_website = fields.Char(string='Company Website')
    min_salary_range = fields.Char(string='Min Salary Range')
    max_salary_range = fields.Char(string='Max Salary Range')
    functional_area = fields.Char(string='Functional Area')
    company_profile = fields.Text(string='Company Profile')
    description = fields.Text(string='Job Description')
    company_benefits = fields.Text(string='Company Benefits')
    instructions = fields.Text(string='Instructions')
    roles_responsibility = fields.Text(string='Roles and Responsibility')
    education = fields.Selection(
        [('graduate', 'Graduate'), ('postgraduate', 'Post Graduate')], string='Education')
    Key_skills = fields.Char(string='Key Skills')
    s_key_skill = fields.Char(string='Secondary Key Skills')
    image = fields.Image("Image")
    specialization = fields.Char(string='Specialization')
    degree_id = fields.Many2one('hr.recruitment.degree', string='Degree')
