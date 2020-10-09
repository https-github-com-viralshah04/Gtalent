from odoo import api,fields,models


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    #Adding custom fields
    is_college = fields.Boolean("Is A College ?",copy = False,
                                help = 'If set,will identify the user as College Entity')
    college_type = fields.Char("College Type",
                               copy = False,
                               help = 'Type of college')
    university_name = fields.Char("University Name", translate=True)
    university_type = fields.Char("University Type",
                                  copy = False,
                                  help = 'Type of University')
    college_email = fields.Char("Email",translate=True)
    college_contact =fields.Char("Contact",copy = False,
                                 help = 'Contact Number of College')
    college_founded_in = fields.Char('College Founded In',
                                     copy = False,
                                     help = 'College Founded In')
    number_of_students = fields.Char("Number of Students",
                                     copy = False,
                                     help = 'Number of Students')
    placement_ratio = fields.Char("Placement Ratio",
                                  copy = False,
                                  help = 'College Placement Ratio')
    college_website = fields.Char("College Website",
                                  copy = False,
                                  help = 'College Website')
    college_management = fields.Char('Management',
                                     copy = False,
                                     help = 'College Management')
    college_year_establishment = fields.Date("Year of Establishment",
                                             copy = False,
                                             help = 'Year of Establishment')
    college_specialization = fields.Char("College Specialization",
                                         copy = False,
                                         help = 'College Specialization')
    college_location = fields.Char("Location",
                                   copy = False,
                                   help = 'Location of the college')
    
    placement_officer_name = fields.Char("Placement Officer Name",
                                         copy = False,
                                         help = 'Placement Officer Name')
    placement_officer_contact = fields.Char("Placement Officer Contact Number",
                                            copy = False,
                                            help = 'Placement Officer Contact Number')
    placement_officer_email = fields.Char("Placement Officer Email",
                                          copy = False,
                                          help = 'Email id of Placement Officer')
    
    
    #Recruitment Related Fields
    
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
        ], string='Address Type',
        default='contact',
        help="Used by Sales and Purchase Apps to select the relevant address depending on the context.")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    
    
    #Social Media Related fields
    social_twitter_acc = fields.Char('Twitter Account')
    social_facebook_acc = fields.Char('Facebook Account')
    social_github_acc = fields.Char('GitHub Account')
    social_linkedin_acc = fields.Char('LinkedIn Account')
    social_youtube_acc = fields.Char('Youtube Account')
    social_googleplus_acc = fields.Char('Google+ Account')
    social_instagram_acc = fields.Char('Instagram Account')
    
    
    is_recruitment_company = fields.Boolean('Is A Recruitment Company?',
                                       copy = False,
                                       help = 'If set,will identify the record as Corporate Company')