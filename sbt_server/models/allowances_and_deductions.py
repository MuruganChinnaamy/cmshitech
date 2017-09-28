#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp
from openerp.tools.translate import _

import openerp.addons.hr_payroll

 


class allowances_and_deductions(models.Model):
    
    _name = 'allowances.and.deductions'
    _description = 'Allowances And Deductions'
  
  
    
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule', required=True)
    allowance_deduction_lines = fields.One2many('allowances.and.deductions.line', 'allowances_and_deductions_id', 'Lines')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),('cancel', 'Cancelled')], 'State', readonly=True)
    allowances_and_deductions_change_log = fields.One2many('allowances.and.deductions.change.log', 'allowances_and_deductions_id', 'Change Log', readonly=True)

    

    _defaults = {        
        'state': 'draft',
    }
    
    _sql_constraints = [('date_from_date_to_salary_rule_id_uniq', 'unique(date_from,date_to,salary_rule_id )', 'Date From,Date To and Salary Head should be unique !'),]
    
    def button_confirm(self, cr, uid, ids, context=None):
        """
        This function is to confirm the allowances and deductions records.Change log is also maintained.
        when this button is clicked,raises a warning if salary head is given without any employee. 
        """
        for record in self.browse(cr, uid, ids):
            if record.allowance_deduction_lines:
                allowance_deduction_lines = []
                change_log_dict = [(0,0, {
                                        'user_id': uid,
                                        'changed_on': datetime.now(),
                                        'from_state': record.state,
                                        'allowances_and_deductions_id' :record.id
                                    })]
                for line in record.allowance_deduction_lines:
                    allowance_deduction_lines.append(line.id)
                    self.pool.get('allowances.and.deductions.line').write(cr, uid, allowance_deduction_lines, {'state': 'done'})
                    self.write(cr, uid, record.id, {'state': 'done'})
                self.write(cr, uid, ids, {'allowances_and_deductions_change_log':change_log_dict} )
                self.pool.get('allowances.and.deductions.change.log').write(cr, uid, record.allowances_and_deductions_change_log[-1].id, {'to_state': record.state})
            else:
                raise osv.except_osv(_('Warning!'), _('You need to Enter atleast one Entry Before Confirmation!'))
        return True
    
    def button_reset(self, cr, uid, ids, context=None):
        """
        This function is to reset the allowances and deductions records.Change log is also maintained.
        """
        for record in self.browse(cr, uid, ids):
            allowance_deduction_lines = []
            change_log_dict = [(0,0, {
                                        'user_id': uid,
                                        'changed_on': datetime.now(),
                                        'from_state': record.state,
                                        'allowances_and_deductions_id' :record.id
                                    })]            
            for line in record.allowance_deduction_lines:
                allowance_deduction_lines.append(line.id)
                self.pool.get('allowances.and.deductions.line').write(cr, uid, allowance_deduction_lines, {'state': 'draft'})
                self.write(cr, uid, record.id, {'state': 'draft'})
            self.write(cr, uid, ids, {'allowances_and_deductions_change_log':change_log_dict} )
            self.pool.get('allowances.and.deductions.change.log').write(cr, uid, record.allowances_and_deductions_change_log[-1].id, {'to_state': record.state})
        return True
    
    def button_cancel(self, cr, uid, ids, context=None):
        """
        This function is to cancel the allowances and deductions records.Change log is also maintained.
        """
        for record in self.browse(cr, uid, ids):
            allowance_deduction_lines = []
            change_log_dict = [(0,0, {
                                        'user_id': uid,
                                        'changed_on': datetime.now(),
                                        'from_state': record.state,
                                        'allowances_and_deductions_id' :record.id
                                    })]            
            for line in record.allowance_deduction_lines:
                allowance_deduction_lines.append(line.id)
                self.pool.get('allowances.and.deductions.line').write(cr, uid, allowance_deduction_lines, {'state': 'cancel'})
                self.write(cr, uid, record.id, {'state': 'cancel'})
            self.write(cr, uid, ids, {'allowances_and_deductions_change_log':change_log_dict} )
            self.pool.get('allowances.and.deductions.change.log').write(cr, uid, record.allowances_and_deductions_change_log[-1].id, {'to_state': record.state})
        return True
    
allowances_and_deductions()

class allowances_and_deductions_change_log(models.Model):
    _name = "allowances.and.deductions.change.log"
    _description = "Allowances and Deductions Change Log"
        
    
        
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    changed_on =  fields.Datetime('Changed On', readonly=True)
    from_state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),('cancel', 'Cancelled')], 'From State', readonly=True)
    to_state  = fields.Selection([('draft', 'Draft'), ('done', 'Done'),('cancel', 'Cancelled')], 'To State', readonly=True)
    allowances_and_deductions_id = fields.Many2one('allowances.and.deductions', 'Allowances and Deductions', readonly=True)

      
    
allowances_and_deductions_change_log()


class allowances_and_deductions_line(models.Model):
    
    _name = 'allowances.and.deductions.line'
    _description = 'Allowances And Deductions Line'
    
    
    
    allowances_and_deductions_id = fields.Many2one('allowances.and.deductions', 'Allowances and Deductions')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    amount = fields.Float('Amount')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),('cancel', 'Cancelled')], 'State', readonly=True)

    
    
    _defaults = {        
        'state': 'draft',
    }

    _sql_constraints = [('allowances_and_deductions_id_employee_id_uniq', 'unique(allowances_and_deductions_id, employee_id)', 'Allowances and Deductions and Employee Should be Unique!'),]

    
allowances_and_deductions_line()