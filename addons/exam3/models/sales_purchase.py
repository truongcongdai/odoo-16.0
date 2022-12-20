from odoo import models, fields, api

class SalesPurchase(models.Model):
    _name = 'sales.purchase'

    def get_record_department(self):
        hr_department_record = self.env['hr.department'].sudo().search([])
        records = []
        for i in hr_department_record:
            tickets = {}
            if i:
                tickets['name']= i.name
                tickets['actual_revenue']= i.actual_revenue
                tickets['revenue_difference']= i.revenue_difference
                records.append(tickets)
        return records

    def get_record_sales_team(self):
        indicator_evaluation_record = self.env['indicator.evaluation'].sudo().search([])
        records = []
        for i in indicator_evaluation_record:
            tickets = {}
            if i:
                tickets['name'] = i.sale_team.name
                tickets['actual_revenue'] = i.actual_revenue
                tickets['revenue_difference'] = i.revenue_difference
                records.append(tickets)
        return records

    def btn_send_email(self):
        # lay ra ban ghi co nhom la accountant
        accountant_group_record = self.env['res.groups'].sudo().search([('name', '=', 'Accountant')])
        #lay ra id cua thuoc nhom Accountant cua res_partner
        res_users_id = accountant_group_record.users.mapped('partner_id').mapped('id')

        email_accountant = self.env['res.partner'].search([('id','in', res_users_id)]).mapped('email')
        self.get_record_department()
        self.get_record_sales_team()

        # indicator_evaluation_record = self.env['indicator.evaluation'].search([])
        # sales_team = indicator_evaluation_record.mapped('sale_team')
        # sales_team_name = sales_team.mapped('name')
        # actual_revenue = indicator_evaluation_record.mapped('actual_revenue')
        # revenue_difference = indicator_evaluation_record.mapped('revenue_difference')
        #
        # hr_department_record = self.env['hr.department'].search([])
        # department_name = hr_department_record.mapped('name')
        # department_actual_revenue = hr_department_record.mapped('actual_revenue')
        # department_revenue_defference = hr_department_record.mapped('revenue_difference')

        template_obj = self.env['mail.template'].sudo().search([('model', 'like', 'sales.purchase')], limit=1)

        # indicator_evaluation_record = self.env['indicator.evaluation'].search([])
        # records_sale = []
        # for i in indicator_evaluation_record:
        #     tickets_sale = {}
        #     if i:
        #         tickets_sale['name'] = i.sale_team.name
        #         tickets_sale['actual_revenue'] = i.actual_revenue
        #         tickets_sale['revenue_difference'] = i.revenue_difference
        #         records_sale.append(tickets_sale)
        # hr_department_record = self.env['hr.department'].search([])
        # records_department = []
        # for i in hr_department_record:
        #     tickets_department = {}
        #     if i:
        #         tickets_department['name'] = i.name
        #         tickets_department['actual_revenue'] = i.actual_revenue
        #         tickets_department['revenue_difference'] = i.revenue_difference
        #         records_department.append(tickets_department)

        mail_values = {
            'subject': template_obj.subject,
            'body_html':template_obj.body_html,
            'email_to': ';'.join(map(lambda x: x, email_accountant)),
            'email_from': 'dai77564@st.vimaru.edu.vn',
        }

        self.env['mail.mail'].create(mail_values).send()