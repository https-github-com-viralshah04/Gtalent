from odoo import api,models,fields


class CollegeUsers(models.Model):
    _name = 'college.users'
    _description =' College Details'
    
    
    user_id = fields.Many2one('res.users', string= 'Colleges')
    
    college_type = fields.Char("College Type",
                               related = 'user_id.college_type',
                               copy = False,
                               help = 'Type of college')
    university_name = fields.Char("University Name", 
                                related = 'user_id.university_name',
                                  translate=True)
    university_type = fields.Char("University Type",
                                  related = 'user_id.university_type',
                                  copy = False,
                                  help = 'Type of University')
    college_email = fields.Char("Email",
                                related = 'user_id.college_email',
                                translate=True)
    college_contact =fields.Char("Contact",copy = False,
                                related = 'user_id.college_contact',
                                 help = 'Contact Number of College')
    college_founded_in = fields.Char('College Founded In',
                                    related = 'user_id.college_founded_in',

                                     copy = False,
                                     help = 'College Founded In')
    number_of_students = fields.Char("Number of Students",
                                    related = 'user_id.number_of_students',

                                     copy = False,
                                     help = 'Number of Students')
    placement_ratio = fields.Char("Placement Ratio",
                                  related = 'user_id.placement_ratio',
                                  copy = False,
                                  help = 'College Placement Ratio')
    college_website = fields.Char("College Website",
                                  related = 'user_id.college_website',
                                  copy = False,
                                  help = 'College Website')
    college_management = fields.Char('Management',
                                    related = 'user_id.college_management',
                                     copy = False,
                                     help = 'College Management')
    college_year_establishment = fields.Date("Year of Establishment",
                                        related = 'user_id.college_year_establishment',
                                         copy = False,
                                         help = 'Year of Establishment')
    college_specialization = fields.Char("College Specialization",
                                         copy = False,
                                        related = 'user_id.college_specialization',
                                         help = 'College Specialization')
    college_location = fields.Char("Location",
                                    related = 'user_id.college_location',
                                   copy = False,
                                   help = 'Location of the college')
    
    placement_officer_name = fields.Char("Placement Officer Name",
                                         related = 'user_id.placement_officer_name',
                                         copy = False,
                                         help = 'Placement Officer Name')
    placement_officer_contact = fields.Char("Placement Officer Contact Number",
                                            related = 'user_id.placement_officer_contact',
                                            copy = False,
                                            help = 'Placement Officer Contact Number')
    placement_officer_email = fields.Char("Placement Officer Email",
                                          related = 'user_id.placement_officer_email',
                                          copy = False,
                                          help = 'Email id of Placement Officer')
    
    
    
    
    
    
    