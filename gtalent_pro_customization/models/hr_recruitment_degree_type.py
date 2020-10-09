from odoo import api,models,fields


class HrRecruitmentDegreeType(models.Model):
    _name = 'hr.recruitment.degree.type'
    _rec_name = 'name'
    _description = "Applicant Degree Type"
    
    _sql_constraints = [
        ('degree_uniq', 'CHECK(1=1)', 'The name of the Degree of Recruitment must be unique!')
    ]
    
    name = fields.Char(string = 'Degree Type',
                       copy = False,
                       help = 'Type of the Degree')
    
    sequence = fields.Integer("Sequence", default=1, help="Gives the sequence order when displaying a list of degrees.")
