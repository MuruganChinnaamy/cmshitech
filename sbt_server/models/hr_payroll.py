#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import logging
import time
import base64
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta


import babel

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval as eval
from odoo.tools.amount_to_text import amount_to_text as amount_to_text_in

from odoo.addons import decimal_precision as dp

#import email_report

_logger = logging.getLogger(__name__)

month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
              7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 
              12: 'December'}

def date_to_india(date_db):
    date_split = False
    if date_db:
        date_split = date_db.split('-')
        date_split = date_split[2]+'/'+date_split[1]+'/'+date_split[0]
    return date_split 





class hr_payslip(models.Model):
    '''
    Pay Slip
    '''

    _name = 'hr.payslip'
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'
    
   

    
    def _get_perday(self):
        start_date = self.date_from
        end_date = self.date_to
        from_date = start_date.split('-')
        till_date = end_date.split('-')
        total_days = (date(int(till_date[0]), int(till_date[1]), int(till_date[2]))-date(int(from_date[0]), int(from_date[1]), int(from_date[2]))).days+1
        gross = self.contract_id.wage
        self.per_day = float(gross)/total_days
        return True  

    def _get_total_days(self):
        start_date = self.date_from
        end_date = self.date_to
        from_date = start_date.split('-')
        till_date = end_date.split('-')
        total_days = (date(int(till_date[0]), int(till_date[1]), int(till_date[2]))-date(int(from_date[0]), int(from_date[1]), int(from_date[2]))).days+1
        self.total_days = total_days            
        return True
    
    def _get_work_days(self):
        self.work_days = self.total_days - self.lop_days             
        return True    
    
    def _get_month_year(self):
        date_start = self.date_from
        date_end = self.date_to
        months_dict = {1: "January",2: "February",3: "March",4: "April",5: "May",6: "June",7: "July",8: "August",9: "September",10: "October",11: "November",12: "December"}
        month_in_number = int(date_start.split('-')[1])
        month_in_word = months_dict[month_in_number]
        year =  date_start.split('-')[0]
        data = (month_in_word+' '+year)
        self.month_year = data
        return True
    
    def _amount_in_words(self):
        net_br = self.env['hr.payslip.line'].browse([('slip_id', '=', self.id), ('code', '=', 'NET')])
        
        if net_br:
            self.amount_in_words = amount_to_text_in(net_br.amount, "Rupee").title()
        else:
            self.amount_in_words = False
        return True  
    
   
    
    
                    
    lop_days = fields.Float('LOP days', readonly=True, states={'draft': [('readonly', False)]})
    total_days = fields.Float(compute = '_get_total_days', string='Days', readonly=True)
    work_days = fields.Float(compute ='_get_work_days', string='Work days',readonly=True)
    per_day = fields.Float(compute = '_get_perday', string='Per day',  readonly=True)
    
    unique_id = fields.Char(related='employee_id.unique_id', string='Employee ID')                 
    company_id = fields.Many2one('res.company', 'Branch', required=False, readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    date_to = fields.Date('Date To', readonly=True, states={'draft': [('readonly', False)]}, required=True)
    department_id =fields.Many2one(related='employee_id.department_id', string='Department',
                                                    relation='hr.department', readonly=True, store=True)
    
    month_year = fields.Char(compute='_get_month_year', string='Month and Year')
    
    amount_in_words = fields.Char(compute='_amount_in_words')
 

                
     
    _order = "date_to desc"    
    
    
    def refresh_sheet(self, cr, uid, ids, context=None):
        obj_rule = self.pool.get('hr.salary.rule')
        localdict = {}
        
        for payslip in self.browse(cr, uid, ids, context=context):
            net_amount = 0.0
            for line in payslip.line_ids:
                if line.salary_rule_id.category_id.code in ('GROSS', 'AALW'):
                    net_amount += line.amount
                if line.salary_rule_id.category_id.code in ('DED',):
                    net_amount -= line.amount 
            
            net = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', payslip.id), ('code', '=', 'NET')])
            
            zero_lines = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', payslip.id), ('amount', '=', 0.0)])            
            self.pool.get('hr.payslip.line').unlink(cr, uid, zero_lines)            
            
            if net:                
                net_br = self.pool.get('hr.payslip.line').browse(cr, uid, net)[0]
                """
                amount, qty, rate = obj_rule.compute_rule(cr, uid, net_br.salary_rule_id.id, localdict, context=context)
                """
                self.pool.get('hr.payslip.line').write(cr, uid, net_br.id, {'amount': net_amount}, context=context)
        return True    


    