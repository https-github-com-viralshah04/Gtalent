from odoo import api,models,fields


class CrmLead(models.Model):
    _inherit = "crm.lead"

    category = fields.Many2one('crm.lead.category',string='Category')

class CrmLeadCategory(models.Model):
    _name = "crm.lead.category"

    name = fields.Char('Name')