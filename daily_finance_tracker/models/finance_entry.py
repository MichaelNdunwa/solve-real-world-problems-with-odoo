from odoo import models, fields, api

class FinanceEntry(models.Model):
    _name = 'finance.entry'
    _description = 'Daily Inflow/Outflow Record'
    _order = 'date desc'

    date = fields.Date(required=True, default=fields.Date.context_today)
    type = fields.Selection([
        ('inflow', 'Inflow'),
        ('outflow', 'Outflow')
    ], required=True)
    description = fields.Char(required=True)
    amount = fields.Float(required=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.uid, readonly=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('user_id'):
                vals['user_id'] = self.env.uid
        return super().create(vals_list)
