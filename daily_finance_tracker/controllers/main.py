from odoo import http
from odoo.http import request
from datetime import datetime
import json

class FinanceEntryController(http.Controller):
    
    @http.route(['/my/finance-tracker'], type='http', auth='user', website=True)
    def finance_form(self, **kw):
        return request.render('daily_finance_tracker.template_finance_form', {
            'default_date': datetime.today().strftime('%Y-%m-%d')
        })

    @http.route(['/finance/submit'], type='json', auth='user', csrf=True)
    def submit_finance_entry(self, **post):
        entries = post.get('entries', [])
        for entry in entries:
            request.env['finance.entry'].sudo().create({
                    'date': entry['date'],
                    'type': entry['type'],
                    'description': entry['description'],
                    'amount': float(entry['amount']),
                    'user_id': request.env.uid
                })
            return {'status': 'success'}