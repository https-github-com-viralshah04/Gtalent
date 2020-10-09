from odoo import api,models,fields


class HrRecruitmentAssessment(models.Model):
    _name = 'hr.recruitment.assessment'
    _description = "Applicant Assessment"
    
    _sql_constraints = [
        ('assesment_uniq', 'CHECK(1=1)', 'The name of the Assessment must be unique!')
    ]

    name = fields.Char("Assessment", required=True, translate=True)
    assessment_scores = fields.Char('Scores')
    assessment_description = fields.Many2many('hr.applicant.category',string = 'Description')
    assessment_date = fields.Date(string = 'Date',
                                  copy = False,
                                  help = 'Date when assessment was taken')
    sequence = fields.Integer("Sequence", default=1, help="Gives the sequence order when displaying a list of degrees.")
    link = fields.Char('Link',
                       copy = False,
                       help = 'Assessment Link')
    vendor = fields.Char('Vendor',
                         copy = False,
                         help = 'Vendor')
    partner_id = fields.Many2one('res.partner')
    
    
    
 