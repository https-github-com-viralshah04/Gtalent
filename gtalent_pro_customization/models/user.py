from odoo import api,models,fields


class UserAccess(models.Model):
    _name = 'user.access'
    
    
    user_id = fields.Many2one('User', required=True)
    sale = fields.Char('Sales')
    accounting = fields.Char('Accounting')
    purchase = fields.Char('Purchase')
    inventory = fields.Char('Inventory')
    project = fields.Char('Project')