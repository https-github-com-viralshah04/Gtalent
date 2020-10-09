from odoo import api,models,fields


class RecruitCompanyUsers(models.Model):
    _name = 'recruitment.company.users'
    _description ='Recruitment Company Users'
    
    
    user_id = fields.Many2one('res.users', string= 'Recruitment Companies')
        
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
        ], string='Address Type',
        related = 'user_id.type',
        default='contact',
        help="Used by Sales and Purchase Apps to select the relevant address depending on the context.")
    street = fields.Char(related = 'user_id.street')
    street2 = fields.Char(related = 'user_id.street2')
    zip = fields.Char(change_default=True,
                      related = 'user_id.zip')
    city = fields.Char(related = 'user_id.city')
    state_id = fields.Many2one("res.country.state",
                                related = 'user_id.state_id',
                                string='State',
                                ondelete='restrict', 
                                domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country',
                                related = 'user_id.country_id',
                                string='Country',
                                ondelete='restrict')
    
    #Social Media Related fields
    social_twitter_acc = fields.Char('Twitter Account',
                                    related = 'user_id.social_twitter_acc')
    social_facebook_acc = fields.Char('Facebook Account',
                                    related = 'user_id.social_facebook_acc')
    social_github_acc = fields.Char('GitHub Account',
                                    related = 'user_id.social_github_acc')
    social_linkedin_acc = fields.Char('LinkedIn Account',
                                    related = 'user_id.social_linkedin_acc')
    social_youtube_acc = fields.Char('Youtube Account',
                                    related = 'user_id.social_youtube_acc')
    social_googleplus_acc = fields.Char('Google+ Account',
                                    related = 'user_id.social_googleplus_acc')
    social_instagram_acc = fields.Char('Instagram Account',
                                    related = 'user_id.social_instagram_acc')
    
    
    
    
    
    
    
    
    
    
  