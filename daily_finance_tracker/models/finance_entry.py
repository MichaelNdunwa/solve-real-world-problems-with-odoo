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
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.uid, readyonly=True)
    
    @api.model
    def create(self, vals):
        # auto-assign current user if missing
        if not vals.get('user_id'):
            vals['user_id'] = self.env.uid
        return super().create
