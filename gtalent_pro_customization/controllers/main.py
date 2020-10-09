import json
import logging
import werkzeug
import base64

from odoo import http, _
from odoo.http import request
from datetime import datetime as dt
from odoo.addons.website.controllers.main import Website
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment
from odoo.addons.web.controllers.main import ensure_db
from odoo.exceptions import UserError
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)


class Website(Website):

    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(
            redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/'
            return http.redirect_with_hash(redirect)
        return response


class WebsiteForm(WebsiteForm):

    @http.route(['/contactus'], type='http', auth="public", website=True)
    def contact_us(self):
        categories = request.env['crm.lead.category'].sudo().search([])
        values = {
            'categories': categories
        }
        return request.render("gtalent_pro_customization.custom_contactus_form_v", values)

    def insert_record(self, request, model, values, custom, meta=None):
        if 'category' in custom:
            category = custom.split(':')
            if category and category[1]:
                values.update({'category': int(category[1])})
                custom = ''
        return super(WebsiteForm, self).insert_record(request, model, values, custom, None)


class WebsiteJobDescription(http.Controller):

    @http.route(['/website/profile'], type='http', auth="public", website=True)
    def website_profile(self, **post):
        values = {}
        applicant_id = False
        if 'applicant_id' in post and post.get('applicant_id'):
            applicant = request.env['hr.applicant'].sudo().browse(
                post.get('applicant_id'))
            partner = applicant
            applicant_id = True

            # model = 'hr.applicant'
            # attachment_id = request.env['ir.attachment'].sudo().search([('res_model', '=', model),('res_id', '=', applicant.id)],limit=1)
        else:
            partner = request.env.user.partner_id
            hr_applicant_obj = request.env['hr.applicant'].sudo().search(
                ['|', ('email_from', '=', partner.email), ('partner_id', '=', partner.id)], limit=1)
            if hr_applicant_obj:
                model = 'hr.applicant'
                # attachment_id = request.env['ir.attachment'].sudo().search(
                #     [('res_model', '=', model), ('res_id', '=', hr_applicant_obj.id)])
                values.update(
                    {'hr_applicant_obj': hr_applicant_obj.attachment_ids})
        values.update({
            'partner': partner,
            'applicant_id': applicant_id,
        })
        return request.render("gtalent_pro_customization.profile", values)

    @http.route(['/custom_job_description_form'], type='http', auth="public", website=True)
    def job_description(self):
        custom_job = request.env['hr.job'].sudo().search([])
        res_company_obj = request.env['res.company'].sudo().search([])
        industry_obj = request.env['hr.recruitment.industry'].sudo().search([])
        values = {
            'custom_job': custom_job,
            'res_company_obj': res_company_obj,
            'industry_obj': industry_obj,
        }
        return request.render("gtalent_pro_customization.custom_job_description_form_page", values)

    @http.route(['/check_login'], type='http', auth='public', website=True)
    def check_login(self, **post):
        result = {}
        if request.env.user._is_public():
            result = {'is_user_logged_in': False}
        else:
            result = {'is_user_logged_in': True}

        return json.dumps(result)

    @http.route(['/custom_job_description_detail_form'], type='http', auth="public", website=True)
    def job_description_detail_form(self, **kw):
        vals = {
            'name': kw.get('name'),
            'job_role': kw.get('role'),
            'company_id': kw.get('company'),
            'industry_type_id': kw.get('industry'),
            'experience_year': kw.get('experience_year'),
            'experience_month': kw.get('experience_month'),
            'work_location': kw.get('worklocation'),
            'candidate': kw.get('candidate'),
            'description': kw.get('jobdescription'),
            'job_type': kw.get('jobtype'),
            'candidate_type': kw.get("candidatetype"),
            'company_website': kw.get("companywebsite"),
            'min_salary_range': kw.get("minsalaryrange"),
            'max_salary_range': kw.get("maxsalaryrange"),
            'functional_area': kw.get("functionalarea"),
            'company_profile': kw.get("companyprofile"),
            'company_benefits': kw.get("companybenefits"),
            'instructions': kw.get("instructions"),
            'roles_responsibility': kw.get("rolesandresponsibility"),
            'education': kw.get("education"),
            'Key_skills': kw.get("Keyskills"),
            's_key_skill': kw.get("SecondaryKeyskills"),
            'no_of_recruitment': kw.get("NoofVacancies"),
            'specialization': kw.get("specialization"),
            'degree_id': int(kw.get("degree")),
        }
        hr_job_obj = request.env['hr.job'].sudo().create(vals)
        return request.render("gtalent_pro_customization.thanks_mail_send_massage_request")

    @http.route('/applicant/profile', type='http', auth='public', website=True)
    def applicant_profile(self, **kwargs):
        if request.env.user._is_public():
            return request.render("gtalent_pro_customization.logged_in_template")
        else:
            hr_recruitment_degree_id = http.request.env['hr.recruitment.degree'].search([
            ])
            # res_partner_id = http.request.env['res.partner'].sudo().search([('is_college', '=', True)])
            res_country_id = http.request.env['res.country'].sudo().search([])
            state_id = http.request.env['res.country.state'].sudo().search([])
            applicant_employment = http.request.env['applicant.employment'].sudo().search([
            ])
            countries = request.env['res.country'].sudo().search([])
            state = request.env['res.country.state'].sudo().search([])
            employment_info = request.env.user.partner_id.employment_type_id
            project_info = request.env.user.partner_id.project_id
            assessment_info = request.env.user.partner_id.assesment_type_id
            education_info = request.env.user.partner_id.educational_type_id
            course_info = request.env.user.partner_id.course_id
            certificate_info = request.env.user.partner_id.certificate_id
            award_info = request.env.user.partner_id.awards_id
            hobbies_info = request.env.user.partner_id.hobbies_id
            skill_info = request.env.user.partner_id.applicant_skill_ids
            shared_info = request.env.user.partner_id.shared_applicant_info_ids
            partner = request.env.user.partner_id
            applicant_college_list_id = http.request.env['res.partner'].sudo().search(
                [('gtalent_users', '=', 'campus')])
            companies = request.env['res.partner'].sudo().search(
                [('gtalent_users', '=', 'employer')])
            skill_types = request.env['hr.skill.type'].sudo().search([])
            skills = request.env['hr.skill'].sudo().search([])
            skill_level = request.env['hr.skill.level'].sudo().search([])
            shared_companies = request.env['res.partner'].sudo().search([])
            stage_status_ids = request.env['hr.recruitment.stage'].sudo().search([
            ])
            degree_type = request.env['hr.recruitment.degree.type'].sudo().search([
            ])
            industry_obj = request.env['hr.recruitment.industry'].sudo().search([
            ])

            values = {
                'hr_recruitment_degree_id': hr_recruitment_degree_id,
                'state_id': state_id,
                'res_country_id': res_country_id,
                'applicant_employment': applicant_employment,
                'countries': countries,
                'state': state,
                'states': state,
                'employment_info': employment_info,
                'assessment_info': assessment_info,
                'hobbies_info': hobbies_info,
                'project_info': project_info,
                'companies': companies,
                'education_info': education_info,
                'applicant_college_list_id': applicant_college_list_id,
                'skill_types': skill_types,
                'skills': skills,
                'skill_level': skill_level,
                'shared_companies': shared_companies,
                'stage_status_ids': stage_status_ids,
                'course_info': course_info,
                'certificate_info': certificate_info,
                'award_info': award_info,
                'shared_info': shared_info,
                'skill_info': skill_info,
                'partner': partner,
                'degree_type': degree_type,
                'industry_obj': industry_obj,
            }
        return request.render("gtalent_pro_customization.job_application_form_template", values)

    @http.route('/create_applicant_shared_details', type='http', auth='user', website=True, csrf=False)
    def create_applicant_shared_details(self, **post):
        vals = {}
        if post.get('shared_company'):
            vals['shared_company'] = int(post.get('shared_company'))
        if post.get('stage_status'):
            vals['stage_status'] = int(post.get('stage_status'))
        if post.get('shared_date'):
            vals['shared_date'] = dt.strptime(
                str(post.get('shared_date')), "%Y-%m-%d")

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            share_applicant_data = request.env['share.applicant.data'].sudo().create(
                vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_shared_details', type='http', auth='user', website=True, csrf=False)
    def update_applicant_shared_details(self, **post):
        vals = {}
        if post.get('shared_company'):
            vals['shared_company'] = int(post.get('shared_company'))
        if post.get('stage_status'):
            vals['stage_status'] = int(post.get('stage_status'))
        if post.get('shared_date'):
            vals['shared_date'] = dt.strptime(
                str(post.get('shared_date')), "%Y-%m-%d")

        if post.get('applicant_shared_details_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            shared_detail_id = request.env['share.applicant.data'].sudo().browse(
                int(post.get('applicant_shared_details_id')))
            share_applicant_data = shared_detail_id.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_employment', type='http', auth='user', website=True, csrf=False)
    def create_applicant_employment(self, **post):
        vals = {}
        if post.get('company_name'):
            vals['company_name'] = int(post.get('company_name'))
        if post.get('designation_type_id'):
            vals['designation_type_id'] = post.get('designation_type_id')
        if post.get('department_type_id'):
            vals['department_type_id'] = post.get('department_type_id')
        if post.get('employment_start_date'):
            vals['employment_start_date'] = dt.strptime(
                str(post.get('employment_start_date')), "%Y-%m-%d")
        if post.get('employment_end_date'):
            vals['employment_end_date'] = dt.strptime(
                str(post.get('employment_end_date')), "%Y-%m-%d")
        if post.get('deliverables'):
            vals['deliverables'] = post.get('deliverables')
        if post.get('job_summary'):
            vals['job_summary'] = post.get('job_summary')
        if post.get('job_accomplishments'):
            vals['job_accomplishments'] = post.get('job_accomplishments')

        if post.get('upload_employment_attachment'):
            # file_name =
            # attachment_id = request.env['ir.attachment'].create({
            #     'datas': base64.encodestring(post['upload_employment_attachment'].read()),
            #     'name': 'resume',
            #     'store_fname': 'resume'
            #     # 'res_id': application.id,
            # })
            # if attachment_id:
            vals['upload_employment_attachment'] = base64.encodestring(
                post['upload_employment_attachment'].read())

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            employment = request.env['applicant.employment'].sudo().create(
                vals)
            request.env.user.partner_id.employment_type_id = [
                (4, employment.id)]
            if request.env.user.partner_id.applicant_id:
                request.env.user.partner_id.applicant_id.employment_type_id = [
                    (4, employment.id)]
        return request.redirect("/applicant/profile")

    @http.route('/create_project_details', type='http', auth='user', website=True, csrf=False)
    def create_project_details(self, **post):
        vals = {}
        if post.get('project_name'):
            vals['name'] = post.get('project_name')
        if post.get('industry'):
            vals['recruitment_industry_id'] = int(post.get('industry'))
        if post.get('project_for'):
            vals['project_for'] = post.get('project_for')
        if post.get('project_start_date'):
            vals['project_start_date'] = dt.strptime(
                str(post.get('project_start_date')), "%Y-%m-%d")
        if post.get('project_end_date'):
            vals['project_end_date'] = dt.strptime(
                str(post.get('project_end_date')), "%Y-%m-%d")
        if post.get('technology'):
            vals['technology'] = post.get('technology')
        if post.get('impact'):
            vals['impact'] = post.get('impact')
        if post.get('guided_by'):
            vals['guided_by'] = post.get('guided_by')
        if post.get('project_summary'):
            vals['project_summary'] = post.get('project_summary')
        if post.get('project_accomplishments'):
            vals['project_accomplishments'] = post.get(
                'project_accomplishments')
        if post.get('team_size'):
            vals['team_size'] = int(post.get('team_size'))
        if post.get('project_duration'):
            vals['project_duration'] = post.get('project_duration')
        if post.get('project_link'):
            vals['project_link'] = post.get('project_link')

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id

            # if request.env.user.partner_id.applicant_id:
            #     vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            project = request.env['applicant.project'].sudo().create(vals)
            request.env.user.partner_id.project_id = [(4, project.id)]
            if request.env.user.partner_id.applicant_id:
                request.env.user.partner_id.applicant_id.project_id = [
                    (4, project.id)]

        return request.redirect("/applicant/profile")

    @http.route('/update_project_details', type='http', auth='user', website=True, csrf=False)
    def update_project_details(self, **post):
        vals = {}
        if post.get('project_name'):
            vals['name'] = post.get('project_name')
        if post.get('industry'):
            vals['recruitment_industry_id'] = int(post.get('industry'))
        if post.get('project_for'):
            vals['project_for'] = post.get('project_for')
        if post.get('project_start_date'):
            vals['project_start_date'] = dt.strptime(
                str(post.get('project_start_date')), "%Y-%m-%d")
        if post.get('project_end_date'):
            vals['project_end_date'] = dt.strptime(
                str(post.get('project_end_date')), "%Y-%m-%d")
        if post.get('technology'):
            vals['technology'] = post.get('technology')
        if post.get('impact'):
            vals['impact'] = post.get('impact')
        if post.get('guided_by'):
            vals['guided_by'] = post.get('guided_by')
        if post.get('project_summary'):
            vals['project_summary'] = post.get('project_summary')
        if post.get('project_accomplishments'):
            vals['project_accomplishments'] = post.get(
                'project_accomplishments')
        if post.get('team_size'):
            vals['team_size'] = int(post.get('team_size'))
        if post.get('project_duration'):
            vals['project_duration'] = post.get('project_duration')
        if post.get('project_link'):
            vals['project_link'] = post.get('project_link')

        if post.get('applicant_project_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id

            # if request.env.user.partner_id.applicant_id:
            #     vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            project = request.env['applicant.project'].sudo().browse(
                int(post.get('applicant_project_id')))
            project.sudo().write(vals)
            # request.env.user.partner_id.project_id = [(4, project.id)]
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_hobbies', type='http', auth='user', website=True, csrf=False)
    def create_applicant_hobbies(self, **post):
        vals = {}
        if post.get('hobby_name'):
            vals['name'] = post.get('hobby_name')
        if post.get('hobbies_comments'):
            vals['hobbies_comments'] = post.get('hobbies_comments')
        if post.get('hobbies_achievements'):
            vals['hobbies_achievements'] = post.get('hobbies_achievements')

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            project = request.env['hr.recruitment.hobbies'].sudo().create(vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_hobbies', type='http', auth='user', website=True, csrf=False)
    def update_applicant_hobbies(self, **post):
        vals = {}
        if post.get('hobby_name'):
            vals['name'] = post.get('hobby_name')
        if post.get('hobbies_comments'):
            vals['hobbies_comments'] = post.get('hobbies_comments')
        if post.get('hobbies_achievements'):
            vals['hobbies_achievements'] = post.get('hobbies_achievements')

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if post.get('applicant_hobbies_id'):
                hobbies = request.env['hr.recruitment.hobbies'].sudo().browse(
                    int(post.get('applicant_hobbies_id')))
                project = hobbies.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_skill', type='http', auth='user', website=True, csrf=False)
    def create_applicant_skill(self, **post):
        vals = {}
        if post.get('skill_type_id'):
            vals['skill_type_id'] = int(post.get('skill_type_id'))
        if post.get('skill_id'):
            vals['skill_id'] = int(post.get('skill_id'))
        if post.get('skill_level_id'):
            vals['skill_level_id'] = int(post.get('skill_level_id'))

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            skill = request.env['hr.employee.skill'].sudo().create(vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_employment', type='http', auth='user', website=True, csrf=False)
    def update_applicant_employment(self, **post):
        vals = {}
        if post.get('company_name'):
            vals['company_name'] = int(post.get('company_name'))
        if post.get('designation_type_id'):
            vals['designation_type_id'] = post.get('designation_type_id')
        if post.get('department_type_id'):
            vals['department_type_id'] = post.get('department_type_id')
        if post.get('employment_start_date'):
            vals['employment_start_date'] = dt.strptime(
                str(post.get('employment_start_date')), "%Y-%m-%d")
        if post.get('employment_end_date'):
            vals['employment_end_date'] = dt.strptime(
                str(post.get('employment_end_date')), "%Y-%m-%d")
        if post.get('deliverables'):
            vals['deliverables'] = post.get('deliverables')
        if post.get('job_summary'):
            vals['job_summary'] = post.get('job_summary')
        if post.get('job_accomplishments'):
            vals['job_accomplishments'] = post.get('job_accomplishments')

        if post.get('upload_employment_attachment'):
            # file_name =
            # attachment_id = request.env['ir.attachment'].create({
            #     'datas': base64.encodestring(post['upload_employment_attachment'].read()),
            #     'name': 'resume',
            #     'store_fname': 'resume'
            #     # 'res_id': application.id,
            # })
            # if attachment_id:
            vals['upload_employment_attachment'] = base64.encodestring(
                post['upload_employment_attachment'].read())

        if post.get('applicant_employment_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            applicant_employment_id = request.env['applicant.employment'].browse(
                int(post.get('applicant_employment_id')))
            employment = applicant_employment_id.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route(['/get_applicant_details'], type='http', auth='public', website=True)
    def get_applicant_details(self, **post):
        result = {}
        partner = request.env.user.partner_id
        if partner:
            result['gender'] = partner.app_gender
            result['nationality'] = partner.nationality
            result['candidate_type'] = partner.candidate_type
            result['blood_group'] = partner.blood_group
            # result['category'] = partner.category

            hr_applicant_obj = request.env['hr.applicant'].sudo().search(
                ['|', ('email_from', '=', partner.email), ('partner_id', '=', partner.id)], limit=1)
            if hr_applicant_obj:
                partner.applicant_id = hr_applicant_obj.id
        return json.dumps(result)

    @http.route(['/get_applicant_employment_details'], type='http', auth='public', website=True)
    def get_applicant_employment_details(self, **post):
        result = {}
        if post.get('employment_id'):
            employment_id = request.env['applicant.employment'].browse(
                int(post.get('employment_id')))
            if employment_id:
                if employment_id.company_name:
                    result['company_name'] = employment_id.company_name.id
                else:
                    result['company_name'] = ""
                result['designation_type_id'] = employment_id.designation_type_id
                result['department_type_id'] = employment_id.department_type_id
                result['employment_start_date'] = employment_id.employment_start_date
                result['employment_end_date'] = employment_id.employment_end_date
                result['deliverables'] = employment_id.deliverables
                result['job_summary'] = employment_id.job_summary
                result['job_accomplishments'] = employment_id.job_accomplishments
        return json.dumps(result, default=date_utils.json_default)

    @http.route(['/get_applicant_hobbies_details'], type='http', auth='public', website=True)
    def get_applicant_hobbies_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['hr.recruitment.hobbies'].browse(
                int(post.get('record_id')))
            if record_id:
                result['name'] = record_id.name
                result['hobbies_comments'] = record_id.hobbies_comments
                result['hobbies_achievements'] = record_id.hobbies_achievements
        return json.dumps(result)

    @http.route(['/get_applicant_award_details'], type='http', auth='public', website=True)
    def get_applicant_award_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.awards'].browse(
                int(post.get('record_id')))
            if record_id:
                result['award_name'] = record_id.award_name
                result['present_by'] = record_id.present_by
                result['award_year'] = record_id.award_year
        return json.dumps(result)

    @http.route(['/get_applicant_certificate_details'], type='http', auth='public', website=True)
    def get_applicant_certificate_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.certificate'].browse(
                int(post.get('record_id')))
            if record_id:
                result['certificate_name'] = record_id.certificate_name
                result['certificate_vendor'] = record_id.certificate_vendor
                result['certificate_id'] = record_id.certificate_id
                result['certificate_technology'] = record_id.certificate_technology
                result['certificate_level'] = record_id.certificate_level
        return json.dumps(result)

    @http.route(['/get_applicant_course_details'], type='http', auth='public', website=True)
    def get_applicant_course_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.courses'].browse(
                int(post.get('record_id')))
            if record_id:
                result['course'] = record_id.course
                result['course_vendor'] = record_id.course_vendor
                result['course_technology'] = record_id.course_technology
                result['course_status'] = record_id.course_status
                result['course_start'] = record_id.course_start
                result['course_end'] = record_id.course_end
        return json.dumps(result, default=date_utils.json_default)

    @http.route(['/get_applicant_education_details'], type='http', auth='public', website=True)
    def get_applicant_education_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.college.list'].browse(
                int(post.get('record_id')))
            if record_id:
                result['degree_type_id'] = record_id.degree_type_id.id
                result['degree_type'] = record_id.degree_type.id
                result['institute'] = record_id.name.id
                result['degree_class'] = record_id.degree_class
                result['country_id'] = record_id.country_id.id
                result['state_id'] = record_id.state_id.id
                result['degree_start_year'] = record_id.degree_start_year
                result['degree_end_year'] = record_id.degree_end_year
                result['degree_score'] = record_id.degree_score
                result['degree_percentage'] = record_id.degree_percentage
        return json.dumps(result, default=date_utils.json_default)

    @http.route(['/get_applicant_shared_details'], type='http', auth='public', website=True)
    def get_applicant_shared_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['share.applicant.data'].browse(
                int(post.get('record_id')))
            if record_id:
                result['shared_company'] = record_id.shared_company.id
                result['stage_status'] = record_id.stage_status.id
                result['shared_date'] = record_id.shared_date
        return json.dumps(result, default=date_utils.json_default)

    @http.route(['/get_applicant_project_details'], type='http', auth='public', website=True)
    def get_applicant_project_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.project'].browse(
                int(post.get('record_id')))
            if record_id:
                result['project_link'] = record_id.project_link
                result['project_accomplishments'] = record_id.project_accomplishments
                result['team_size'] = record_id.team_size
                result['project_start_date'] = record_id.project_start_date
                result['project_end_date'] = record_id.project_end_date
                result['project_duration'] = record_id.project_duration
                result['project_summary'] = record_id.project_summary
                result['guided_by'] = record_id.guided_by
                result['impact'] = record_id.impact
                result['project_for'] = record_id.project_for
                result['industry'] = record_id.recruitment_industry_id.id
                result['name'] = record_id.name
                result['technology'] = record_id.technology
        return json.dumps(result, default=date_utils.json_default)

    @http.route(['/get_applicant_assessment_details'], type='http', auth='public', website=True)
    def get_applicant_assessment_details(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['hr.recruitment.assessment'].browse(
                int(post.get('record_id')))
            if record_id:
                result['assessment_name'] = record_id.name
                result['assessment_description'] = record_id.assessment_description
                result['assessment_scores'] = record_id.assessment_scores
                result['vendor'] = record_id.vendor
                result['link'] = record_id.link
                result['assessment_date'] = record_id.assessment_date
        return json.dumps(result, default=date_utils.json_default)

    @http.route(['/delete_applicant_employment'], type='http', auth='public', website=True)
    def delete_applicant_employment(self, **post):
        result = {}
        if post.get('employment_id'):
            employment_id = request.env['applicant.employment'].browse(
                int(post.get('employment_id')))
            if employment_id:
                employment_id.sudo().unlink()
        return json.dumps(result)

    @http.route('/create_applicant_education', type='http', auth='user', website=True, csrf=False)
    def create_applicant_education(self, **post):
        vals = {}
        if post.get('degree_type_id'):
            vals['degree_type_id'] = int(post.get('degree_type_id'))
        if post.get('hr_recruitment_degree_id'):
            vals['degree_type'] = int(post.get('hr_recruitment_degree_id'))
        if post.get('institute'):
            vals['name'] = int(post.get('institute'))
        if post.get('country_id'):
            vals['country_id'] = int(post.get('country_id'))
        if post.get('state_id'):
            vals['state_id'] = int(post.get('state_id'))
        if post.get('degree_percentage'):
            vals['degree_percentage'] = float(post.get('degree_percentage'))
        if post.get('degree_score'):
            vals['degree_score'] = post.get('degree_score')
        if post.get('degree_start_year'):
            vals['degree_start_year'] = int(post.get('degree_start_year'))
        if post.get('degree_end_year'):
            vals['degree_end_year'] = int(post.get('degree_end_year'))
        if post.get('degree_class'):
            vals['degree_class'] = post.get('degree_class')
        if post.get('upload_certificate'):
            vals['upload_certifcate'] = base64.encodestring(
                post['upload_certificate'].read())
        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            employment = request.env['applicant.college.list'].sudo().create(
                vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_education', type='http', auth='user', website=True, csrf=False)
    def update_applicant_education(self, **post):
        vals = {}
        if post.get('degree_type_id'):
            vals['degree_type_id'] = int(post.get('degree_type_id'))
        if post.get('hr_recruitment_degree_id'):
            vals['degree_type'] = int(post.get('hr_recruitment_degree_id'))
        if post.get('institute'):
            vals['name'] = int(post.get('institute'))
        if post.get('country_id'):
            vals['country_id'] = int(post.get('country_id'))
        if post.get('state_id'):
            vals['state_id'] = int(post.get('state_id'))
        if post.get('degree_percentage'):
            vals['degree_percentage'] = float(post.get('degree_percentage'))
        if post.get('degree_score'):
            vals['degree_score'] = post.get('degree_score')
        if post.get('degree_start_year'):
            vals['degree_start_year'] = int(post.get('degree_start_year'))
        if post.get('degree_end_year'):
            vals['degree_end_year'] = int(post.get('degree_end_year'))
        if post.get('degree_class'):
            vals['degree_class'] = post.get('degree_class')
        if post.get('upload_certificate'):
            vals['upload_certifcate'] = base64.encodestring(
                post['upload_certificate'].read())
        if post.get('applicant_education_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            education = request.env['applicant.college.list'].sudo().browse(
                int(post.get('applicant_education_id')))
            result = education.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_course', type='http', auth='user', website=True, csrf=False)
    def create_applicant_course(self, **post):
        vals = {}
        if post.get('course'):
            vals['course'] = post.get('course')
        if post.get('course_vendor'):
            vals['course_vendor'] = post.get('course_vendor')
        if post.get('course_technology'):
            vals['course_technology'] = post.get('course_technology')
        if post.get('course_status'):
            vals['course_status'] = post.get('course_status')
        if post.get('course_start'):
            vals['course_start'] = dt.strptime(
                str(post.get('course_start')), "%Y-%m-%d")
        if post.get('course_end'):
            vals['course_end'] = dt.strptime(
                str(post.get('course_end')), "%Y-%m-%d")
        if post.get('course_documents'):
            vals['course_documents'] = base64.encodestring(
                post['course_documents'].read())

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            courses = request.env['applicant.courses'].sudo().create(vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_course', type='http', auth='user', website=True, csrf=False)
    def update_applicant_course(self, **post):
        vals = {}
        if post.get('course'):
            vals['course'] = post.get('course')
        if post.get('course_vendor'):
            vals['course_vendor'] = post.get('course_vendor')
        if post.get('course_technology'):
            vals['course_technology'] = post.get('course_technology')
        if post.get('course_status'):
            vals['course_status'] = post.get('course_status')
        if post.get('course_start'):
            vals['course_start'] = dt.strptime(
                str(post.get('course_start')), "%Y-%m-%d")
        if post.get('course_end'):
            vals['course_end'] = dt.strptime(
                str(post.get('course_end')), "%Y-%m-%d")
        if post.get('course_documents'):
            vals['course_documents'] = base64.encodestring(
                post['course_documents'].read())

        if post.get('applicant_course_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            courses = request.env['applicant.courses'].sudo().browse(
                int(post.get('applicant_course_id')))
            courses.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_certificate', type='http', auth='user', website=True, csrf=False)
    def create_applicant_certificate(self, **post):
        vals = {}
        if post.get('certificate_vendor'):
            vals['certificate_vendor'] = post.get('certificate_vendor')
        if post.get('certificate_name'):
            vals['certificate_name'] = post.get('certificate_name')
        if post.get('certificate_id'):
            vals['certificate_id'] = post.get('certificate_id')
        if post.get('certificate_technology'):
            vals['certificate_technology'] = post.get('certificate_technology')
        if post.get('certificate_level'):
            vals['certificate_level'] = post.get('certificate_level')
        if post.get('certificate_documents'):
            vals['certificate_documents'] = base64.encodestring(
                post['certificate_documents'].read())

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            courses = request.env['applicant.certificate'].sudo().create(vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_certificate', type='http', auth='user', website=True, csrf=False)
    def update_applicant_certificate(self, **post):
        vals = {}
        if post.get('certificate_vendor'):
            vals['certificate_vendor'] = post.get('certificate_vendor')
        if post.get('certificate_name'):
            vals['certificate_name'] = post.get('certificate_name')
        if post.get('certificate_id'):
            vals['certificate_id'] = post.get('certificate_id')
        if post.get('certificate_technology'):
            vals['certificate_technology'] = post.get('certificate_technology')
        if post.get('certificate_level'):
            vals['certificate_level'] = post.get('certificate_level')
        if post.get('certificate_documents'):
            vals['certificate_documents'] = base64.encodestring(
                post['certificate_documents'].read())

        if post.get('applicant_certificate_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            courses = request.env['applicant.certificate'].sudo().browse(
                int(post.get('applicant_certificate_id')))
            courses.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_award', type='http', auth='user', website=True, csrf=False)
    def create_applicant_award(self, **post):
        vals = {}
        if post.get('award_name'):
            vals['award_name'] = post.get('award_name')
        if post.get('present_by'):
            vals['present_by'] = post.get('present_by')
        if post.get('award_year'):
            vals['award_year'] = int(post.get('award_year'))

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.applicant_id:
                vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            courses = request.env['applicant.awards'].sudo().create(vals)
        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_award', type='http', auth='user', website=True, csrf=False)
    def update_applicant_award(self, **post):
        vals = {}
        if post.get('award_name'):
            vals['award_name'] = post.get('award_name')
        if post.get('present_by'):
            vals['present_by'] = post.get('present_by')
        if post.get('award_year'):
            vals['award_year'] = int(post.get('award_year'))

        if post.get('applicant_award_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            courses = request.env['applicant.awards'].sudo().browse(
                int(post.get('applicant_award_id')))
            courses.sudo().write(vals)
        return request.redirect("/applicant/profile")

    @http.route('/create_applicant_assessment', type='http', auth='user', website=True, csrf=False)
    def create_applicant_assessment(self, **post):
        vals = {}
        if post.get('assessment_name'):
            vals['name'] = post.get('assessment_name')
        # if post.get('assessment_description'):
        #     vals['assessment_description'] = post.get('assessment_description')
        if post.get('assessment_scores'):
            vals['assessment_scores'] = post.get('assessment_scores')
        if post.get('vendor'):
            vals['vendor'] = post.get('vendor')
        if post.get('link'):
            vals['link'] = post.get('link')
        if post.get('assessment_date'):
            vals['assessment_date'] = dt.strptime(
                str(post.get('assessment_date')), "%Y-%m-%d")

        if vals:
            vals['partner_id'] = request.env.user.partner_id.id
            # if request.env.user.partner_id.applicant_id:
            #     vals['applicant_id'] = request.env.user.partner_id.applicant_id.id
            assessment = request.env['hr.recruitment.assessment'].sudo().create(
                vals)
            request.env.user.partner_id.assesment_type_id = [
                (4, assessment.id)]
            if request.env.user.partner_id.applicant_id:
                request.env.user.partner_id.applicant_id.assesment_type_id = [
                    (4, assessment.id)]

        return request.redirect("/applicant/profile")

    @http.route('/update_applicant_assessment', type='http', auth='user', website=True, csrf=False)
    def update_applicant_assessment(self, **post):
        vals = {}
        if post.get('assessment_name'):
            vals['name'] = post.get('assessment_name')
        # if post.get('assessment_description'):
        #     vals['assessment_description'] = post.get('assessment_description')
        if post.get('assessment_scores'):
            vals['assessment_scores'] = post.get('assessment_scores')
        if post.get('vendor'):
            vals['vendor'] = post.get('vendor')
        if post.get('link'):
            vals['link'] = post.get('link')
        if post.get('assessment_date'):
            vals['assessment_date'] = dt.strptime(
                str(post.get('assessment_date')), "%Y-%m-%d")

        if post.get('applicant_assessment_id') and vals:
            vals['partner_id'] = request.env.user.partner_id.id
            assessment = request.env['hr.recruitment.assessment'].sudo().browse(
                int(post.get('applicant_assessment_id')))
            assessment.sudo().write(vals)
            # request.env.user.partner_id.assesment_type_id = [(4, assessment.id)]
        return request.redirect("/applicant/profile")

    # @http.route('/create_applicant_skill', type='http', auth='user', website=True, csrf=False)
    # def create_applicant_skill(self, **post):
    #     vals = {}
    #     if vals:
    #         vals['partner_id'] = request.env.user.partner_id.id
    #         employment = request.env['applicant.employment'].sudo().create(vals)
    #     return request.redirect("/applicant/profile")

    @http.route(['/delete_applicant_education'], type='http', auth='public', website=True)
    def delete_applicant_education(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.college.list'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_skill'], type='http', auth='public', website=True)
    def delete_applicant_skill(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['hr.employee.skill'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_assessment'], type='http', auth='public', website=True)
    def delete_applicant_assessment(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['hr.recruitment.assessment'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_hobbies'], type='http', auth='public', website=True)
    def delete_applicant_hobbies(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['hr.recruitment.hobbies'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_project'], type='http', auth='public', website=True)
    def delete_applicant_project(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.project'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_shared_doc'], type='http', auth='public', website=True)
    def delete_applicant_shared_doc(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['share.applicant.data'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_course'], type='http', auth='public', website=True)
    def delete_applicant_course(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.courses'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_certificate'], type='http', auth='public', website=True)
    def delete_applicant_certificate(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.certificate'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route(['/delete_applicant_award'], type='http', auth='public', website=True)
    def delete_applicant_award(self, **post):
        result = {}
        if post.get('record_id'):
            record_id = request.env['applicant.awards'].browse(
                int(post.get('record_id')))
            if record_id:
                record_id.sudo().unlink()
        return json.dumps(result)

    @http.route('/save/profile', type='http', auth='user', website=True, csrf=False)
    def save_applicant_profile(self, **post):
        vals = {}
        if post.get('save_personal_details') != 'true':
            if post['myfile']:
                user_data = base64.encodestring(post['myfile'].read())
                vals.update({'image_1920': user_data})

        if post.get('applicant_name'):
            vals['name'] = post.get('applicant_name')
        if post.get('email'):
            vals['email'] = post.get('email')
        if post.get('gender'):
            vals['app_gender'] = post.get('gender')
        if post.get('nationality'):
            vals['nationality'] = post.get('nationality')
        if post.get('blood_group'):
            vals['blood_group'] = post.get('blood_group')
        if post.get('language'):
            vals['language'] = post.get('language')
        if post.get('category'):
            vals['category'] = post.get('category')
        if post.get('aadhar_number'):
            vals['aadhar_number'] = post.get('aadhar_number')
        if post.get('phone'):
            vals['phone'] = post.get('phone')
        if post.get('source'):
            vals['source'] = post.get('source')
        if post.get('uploaded_by'):
            vals['uploaded_by'] = post.get('uploaded_by')
        if post.get('candidate_type'):
            vals['candidate_type'] = post.get('candidate_type')
        if post.get('candidate_exp'):
            vals['years_of_exp'] = post.get('candidate_exp')
        if post.get('visa_information'):
            vals['visa_info'] = post.get('visa_information')
        if post.get('address_type'):
            vals['address_type'] = post.get('address_type')
        if post.get('street'):
            vals['street'] = post.get('street')
        if post.get('street2'):
            vals['street2'] = post.get('street2')
        if post.get('city'):
            vals['city'] = post.get('city')
        if post.get('state'):
            vals['state_id'] = int(post.get('state'))
        if post.get('zip'):
            vals['zip'] = post.get('zip')
        if post.get('country_id'):
            vals['country_id'] = int(post.get('country_id'))
        if post.get('social_twitter_acc'):
            vals['social_twitter_acc'] = post.get('social_twitter_acc')
        if post.get('social_facebook_acc'):
            vals['social_facebook_acc'] = post.get('social_facebook_acc')
        if post.get('social_github_acc'):
            vals['social_github_acc'] = post.get('social_github_acc')
        if post.get('social_linkedin_acc'):
            vals['social_linkedin_acc'] = post.get('social_linkedin_acc')
        if post.get('social_youtube_acc'):
            vals['social_youtube_acc'] = post.get('social_youtube_acc')
        if post.get('social_googleplus_acc'):
            vals['social_googleplus_acc'] = post.get('social_googleplus_acc')
        if post.get('social_instagram_acc'):
            vals['social_instagram_acc'] = post.get('social_instagram_acc')
        if post.get('birth_date'):
            vals['date_of_birth'] = dt.strptime(
                str(post.get('birth_date')), "%Y-%m-%d")

        partner = request.env.user.partner_id
        partner.sudo().write(vals)
        if post.get('save_personal_details') == 'true':
            return json.dumps(post)
        else:
            if partner.applicant_id:
                vals['email_from'] = post.get('email')
                if post.get('email_cc'):
                    vals['email_cc'] = post.get('email_cc')
                if post.get('candiate_exp'):
                    vals['candidate_exp'] = post.get('candiate_exp')
                if post['myfile']:
                    user_data = base64.encodestring(post['myfile'].read())
                    vals.update({'image_128': user_data})
                if post.get('birth_date'):
                    vals['candidate_birth_date'] = dt.strptime(
                        str(post.get('birth_date')), "%Y-%m-%d")

                if 'image_1920' in vals:
                    del vals['image_1920']
                if 'email' in vals:
                    del vals['email']
                if 'date_of_birth' in vals:
                    del vals['date_of_birth']
                if 'phone' in vals:
                    del vals['phone']
                if 'years_of_exp' in vals:
                    del vals['years_of_exp']
                partner.applicant_id.sudo().write(vals)
            return request.render("gtalent_pro_customization.submit_form_template")

    @http.route('/add/degree/name', type='http', auth='public', website=True, csrf=False)
    def add_degree_name(self, **post):
        hr_recruitment_degree_obj = http.request.env['hr.recruitment.degree']
        vals = {}
        if post.get('degree_name'):
            vals['name'] = post.get('degree_name')
        hr_recruitment_degree_id = hr_recruitment_degree_obj.sudo().create(vals)
        # order_no = post.get('order_number')

    @http.route('/add/educational/institute', type='http', auth='public', website=True, csrf=False)
    def add_educational_institute(self, **post):
        res_partner_obj = http.request.env['res.partner']
        vals = {}
        if post.get('educational_institute'):
            vals['name'] = post.get('educational_institute')
        vals['is_college'] = True
        res_partner_id = res_partner_obj.sudo().create(vals)

    # @http.route('/update/state', type='http', auth='public', website=True, csrf=False)
    # def update_state(self, **post):
    #     state_id = http.request.env['res.country.state'].sudo().search([('country_id', 'in', post['res_country_id'])])
    #     value = {
    #         'state_id': state_id
    #     }
    #     return json.dumps(value)

    # @http.route('/save/educational_details', type='http', auth='user', website=True)
    # def save_educational_details(self, redirect=None, **post):


class AuthSignupHome(AuthSignupHome):

    @http.route()
    def web_login(self, *args, **kw):

        ensure_db()
        response = super(AuthSignupHome, self).web_login(*args, **kw)
        response.qcontext.update(self.get_auth_signup_config())

        current_uid = request.session.uid
        logged_user = request.env['res.users'].sudo().browse(current_uid)
        partner_dict = {}
        if logged_user:
            values = {}
            if kw.get('user_type'):
                if kw.get('user_type') == 'candidate':
                    user_access_group = request.env.ref(
                        'gtalent_pro_customization.g_candidate')
                    values['gtalent_users'] = 'candidate'
                if kw.get('user_type') == 'recruiter':
                    user_access_group = request.env.ref(
                        'gtalent_pro_customization.g_recruiter')
                    values['gtalent_users'] = 'employer'
                if kw.get('user_type') == 'college':
                    user_access_group = request.env.ref(
                        'gtalent_pro_customization.g_college')
                    values['gtalent_users'] = 'campus'
                if user_access_group:
                    logged_user.sudo().write(
                        {'groups_id': [(4, user_access_group.id)]})
            if logged_user.partner_id:
                if kw.get('gender'):
                    values['app_gender'] = kw.get('gender')
                if kw.get('nationality'):
                    values['nationality'] = kw.get('nationality')
                if kw.get('blood_group'):
                    values['blood_group'] = kw.get('blood_group')
                if kw.get('language'):
                    values['language'] = kw.get('language')
                if kw.get('aadhar_number'):
                    values['aadhar_number'] = kw.get('aadhar_number')
                if kw.get('street'):
                    values['street'] = kw.get('street')
                if kw.get('street2'):
                    values['street2'] = kw.get('street2')
                if kw.get('city'):
                    values['city'] = kw.get('city')
                if kw.get('zip'):
                    values['zip'] = kw.get('zip')
                if kw.get('country_id'):
                    values['country_id'] = int(kw.get('country_id'))
                if kw.get('state_id'):
                    values['state_id'] = int(kw.get('state_id'))
                if kw.get('phone'):
                    values['phone'] = kw.get('phone')
                if kw.get('date_of_birth'):
                    values['date_of_birth'] = dt.strptime(
                        str(kw.get('date_of_birth')), "%Y-%m-%d")
                if kw.get('experience'):
                    values['years_of_exp'] = kw.get('experience')
                if kw.get('qualification'):
                    values['qualification'] = kw.get('qualification')
                if kw.get('company_website'):
                    values['website'] = kw.get('company_website')
                if kw.get('industry'):
                    values['industry'] = int(kw.get('industry'))
                if kw.get('registered_id'):
                    values['registered_id'] = kw.get('registered_id')
                if kw.get('company_gsnt'):
                    values['gstn_id'] = kw.get('company_gsnt')
                if kw.get('university_name'):
                    values['university_name'] = kw.get('university_name')
                if kw.get('college_website'):
                    values['website'] = kw.get('college_website')
                if kw.get('affiliation_id'):
                    values['affiliation_id'] = kw.get('affiliation_id')
                if kw.get('college_gstn'):
                    values['gstn_id'] = kw.get('college_gstn')

                placement_officer = {}
                if kw.get('placement_officer_name'):
                    placement_officer['placement_officer_name'] = kw.get(
                        'placement_officer_name')
                if kw.get('placement_officer_mobile'):
                    placement_officer['placement_officer_contact'] = kw.get(
                        'placement_officer_mobile')
                if kw.get('placement_officer_email'):
                    placement_officer['placement_officer_email'] = kw.get(
                        'placement_officer_email')
                if placement_officer:
                    placement_officer['placement_officer_position'] = 'placement_officer'
                    placement_officer['campus_id'] = logged_user.partner_id.id
                    officer = request.env['campus.placement.details'].sudo().create(
                        placement_officer)

                placement_head = {}
                if kw.get('placement_head_name'):
                    placement_head['placement_officer_name'] = kw.get(
                        'placement_head_name')
                if kw.get('placement_head_mobile'):
                    placement_head['placement_officer_contact'] = kw.get(
                        'placement_head_mobile')
                if kw.get('placement_head_email'):
                    placement_head['placement_officer_email'] = kw.get(
                        'placement_head_email')
                if placement_head:
                    placement_head['placement_officer_position'] = 'placement_head'
                    placement_head['campus_id'] = logged_user.partner_id.id
                    officer = request.env['campus.placement.details'].sudo().create(
                        placement_head)

                logged_user.partner_id.sudo().write(values)
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            return http.redirect_with_hash(request.params.get('redirect'))
        return response

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode(
                                {'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _(
                        "Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        country = request.env['res.country'].sudo().search([])
        state = request.env['res.country.state'].sudo().search([])
        companies = request.env['res.partner'].sudo().search([])
        industry_obj = request.env['hr.recruitment.industry'].sudo().search([])
        #language = request.env['res.lang'].search([])
        #qcontext['lang'] = language
        qcontext['usertype'] = kw['user_type']
        qcontext['countries'] = country
        qcontext['state'] = state
        qcontext['companies'] = companies
        qcontext['industry_obj'] = industry_obj
        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class WebsiteHrRecruitment(WebsiteHrRecruitment):

    def sitemap_jobs(env, rule, qs):
        if not qs or qs.lower() in '/jobs':
            yield {'loc': '/jobs'}

    @http.route([
        '/jobs',
        '/jobs/<string:browseby>',
        '/jobs/country/<model("res.country"):country>',

        '/jobs/department/<model("hr.department"):department>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>',

        '/jobs/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/office/<int:office_id>',
        '/jobs/department/<model("hr.department"):department>/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/office/<int:office_id>',

        '/jobs/job_type/<string:job_type>',
        '/jobs/country/<model("res.country"):country>/job_type/<string:job_type>',
        '/jobs/department/<model("hr.department"):department>/job_type/<string:job_type>',
        '/jobs/office/<int:office_id>/job_type/<string:job_type>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/job_type/<string:job_type>',
        '/jobs/country/<model("res.country"):country>/office/<int:office_id>/job_type/<string:job_type>',
        '/jobs/department/<model("hr.department"):department>/office/<int:office_id>/job_type/<string:job_type>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/office/<int:office_id>/job_type/<string:job_type>',

        '/jobs/industry/<model("hr.recruitment.industry"):industry>',
        '/jobs/country/<model("res.country"):country>/industry/<model("hr.recruitment.industry"):industry>',
        '/jobs/job_type/<string:job_type>/industry/<model("hr.recruitment.industry"):industry>',
        '/jobs/country/<model("res.country"):country>/job_type/<string:job_type>/industry/<model("hr.recruitment.industry"):industry>',
    ], type='http', auth="public", website=True, sitemap=sitemap_jobs)
    def jobs(self, country=None, department=None, office_id=None, job_type=None, industry=None, search='', location='', browseby='', **kwargs):
        env = request.env(context=dict(request.env.context,
                                       show_address=True, no_tag_br=True))
        Country = env['res.country']
        Jobs = env['hr.job']
        # group_by_job_role = []
        # if 'group_by' in kwargs:
        #     if kwargs.get('group_by') == 'job_role':
        #         group_by_job_role = Jobs.read_group([], ["id"], groupby=["job_role"])
        #

        # List jobs available to current UID
        domain = request.website.website_domain()
        job_ids = Jobs.search(
            domain, order="is_published desc, no_of_recruitment desc").ids
        # Browse jobs as superuser, because address is restricted
        jobs = Jobs.sudo().browse(job_ids)

        if search:
            jobs = Jobs.search(
                ['|', ('name', 'ilike', search), ('company_id.name', 'ilike', search)])
        elif location:
            jobs = Jobs.search([('address_id.state_id', 'ilike', location)])
        if search and location:

            jobs = Jobs.search([('name', 'ilike', search), '|', ('company_id.name',
                                                                 'ilike', search), ('addresapps_id.state_id', 'ilike', location), ])
        # if browseby:
        #     jobs = Jobs.search([],groupby=browseby)

        # Default search by user country
        if not (country or department or office_id or kwargs.get('all_countries')):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                countries_ = Country.search([('code', '=', country_code)])
                country = countries_[0] if countries_ else None
                if not any(j for j in jobs if j.address_id and j.address_id.country_id == country):
                    country = False

        # Filter job / office for country
        if country and not kwargs.get('all_countries'):
            jobs = [j for j in jobs if
                    j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id]
            offices = set(j.address_id for j in jobs if
                          j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id)
        else:
            offices = set(j.address_id for j in jobs if j.address_id)

        # Deduce departments and countries offices of those jobs
        departments = set(j.department_id for j in jobs if j.department_id)
        countries = set(o.country_id for o in offices if o.country_id)

        if department:
            jobs = [
                j for j in jobs if j.department_id and j.department_id.id == department.id]

        job_types = set(j.job_type for j in jobs if j.job_type)
        if job_type:
            jobs = [j for j in jobs if j.job_type and j.job_type == job_type]

        industries = set(
            j.industry_type_id for j in jobs if j.industry_type_id)
        if industry:
            jobs = [
                j for j in jobs if j.industry_type_id and j.industry_type_id.id == industry.id]

        if office_id and office_id in [x.id for x in offices]:
            jobs = [j for j in jobs if j.address_id and j.address_id.id == office_id]
        else:
            office_id = False
        # Render page
        return request.render("gtalent_pro_customization.index_jobs", {
            'jobs': jobs,
            'countries': countries,
            'departments': departments,
            'offices': offices,
            'job_types': job_types,
            'industries': industries,
            'country_id': country,
            'department_id': department,
            'office_id': office_id,
            'job_type': job_type,
            'industry_id': industry,
            # 'group_by_job_role':group_by_job_role,
        })
