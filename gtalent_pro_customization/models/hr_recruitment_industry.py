from odoo import api,models,fields


class HrRecruitmentIndustry(models.Model):
    _description = 'Industry'
    _name = "hr.recruitment.industry"
    _order = "name"

    name = fields.Char('Name', translate=True)
    full_name = fields.Char('Full Name', translate=True)
    active = fields.Boolean('Active', default=True)