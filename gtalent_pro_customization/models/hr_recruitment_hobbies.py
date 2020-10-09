from odoo import api,models,fields


class HrRecruitmentHobbies(models.Model):
    _name = 'hr.recruitment.hobbies'
    _description = "Applicant Hobbies"
    
    _sql_constraints = [
        ('hobbies_uniq', 'CHECK(1=1)', 'The name of the Hobby of Applicant must be unique!')
    ]

    applicant_id = fields.Many2one('hr.applicant')
    name = fields.Char("Hobbies", required=True, translate=True)
    sequence = fields.Integer("Sequence", default=1, help="Gives the sequence order when displaying a list of degrees.")
    hobbies_comments = fields.Char('Comments')
    hobbies_achievements = fields.Char('Any Achievements')
    partner_id = fields.Many2one('res.partner', string='Partner')
    
    
    
 