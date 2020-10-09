from odoo import api,fields,models


class ResUsers(models.Model):
    _inherit = 'res.company'
    
    gstn = fields.Char('GSTN')