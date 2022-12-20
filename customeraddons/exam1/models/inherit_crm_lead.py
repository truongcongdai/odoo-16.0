from odoo import models, fields , api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sale_team = fields.Many2one('crm.team', string='Sales Team')
    minimum_revenue = fields.Float(string='Minimum Revenue (VAT)')

    check_priority = fields.Boolean(defult=False, compute='_compute_check_priority')
    check_edit_minimum_revenue = fields.Boolean(default=True, compute='_compute_check_edit_minimum_revenue')

    actual_revenue = fields.Float(string='Actual Revenue', compute='_compute_actual_revenue', store=False)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=True)
    # check_selespreson = fields.Boolean(default = False)

    # Tinh actual_revenue = tong amount_total_opportunity
    def _compute_actual_revenue(self):
        for rec in self:
            if rec.id:
                amount_total = self.env['sale.order'].search([('opportunity_id', '=', rec.id)])
                amount_total_opportunity = amount_total.mapped('amount_total')
                rec.actual_revenue = sum(amount_total_opportunity)

    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                create_date = str(rec.create_date)
                create_month = create_date.split("-")
                rec.create_month = create_month[1]

    def _compute_check_edit_minimum_revenue(self):
        count_quotations = self.env['sale.order'].search_count([('opportunity_id','=',self.id)])
        self.check_edit_minimum_revenue = True
        if count_quotations > 0:
            self.check_edit_minimum_revenue = False

    #check priority = very high va tk co thuoc nhom leader
    @api.depends('priority')
    def _compute_check_priority(self):
        for r in self:
            r.check_priority = False
            if r.priority == '3' and not r.user_has_groups('exam1.group_lead_employee'):
                r.check_priority = True

    def btn_leader_lost(self):
        return super(CrmLead, self).action_set_lost()

    @api.constrains('minimum_revenue')
    def _check_minimum_revenue(self):
        if self.minimum_revenue <= 0:
            raise models.ValidationError('Minimum revenue > 0')