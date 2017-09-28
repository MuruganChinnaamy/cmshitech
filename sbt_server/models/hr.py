# -*- coding: utf-8 -*-
# from openerp.osv import fields, osv
# from openerp import tools
# from openerp.tools.translate import _
# from openerp.modules.module import get_module_resource

from openerp.osv import expression
from openerp.tools.float_utils import float_round as round
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _
from odoo import tools, _

import dateutil.relativedelta
import dateutil.parser
import calendar


from datetime import datetime, date, time, timedelta
import time
import dateutil
import base64
import sys
from bsddb.dbtables import _columns
from email import _name
from openerp.http import request
import httplib
import json
from dateutil.relativedelta import relativedelta

import logging
from openid.store.nonce import time_fmt
_logger = logging.getLogger(__name__)


def date_indian(date):
    date_split = date.split('-')
    date_indian = date_split[2]+'/'+date_split[1]+'/'+date_split[0] 
    return date_indian



class Employee(models.Model):
    
    _inherit = "hr.employee"
    
    unique_id = fields.Char('Employee ID', size=12, readonly=True) 
    #unique_id_integer= fields.Integer('Employee ID', readonly=True) 
    date_joined = fields.Date("Date joined")
    date_left =  fields.Date("Date left")
    
#     
    
    @api.model
    @api.multi
    def create(self, vals):
        unique_id = self.env['ir.sequence'].get('hr.employee')
        vals['unique_id'] = unique_id     
        #vals['unique_id_integer'] = int(unique_id)
          
        name = "Contract"+":"+vals['unique_id']+":"+vals['name']
        #tools.image_resize_images(vals)
        #return super(Employee, self).create(vals)  
        hr_employee_id = super(Employee, self).create(vals)
         
         
        if 'date_joined' in vals:
            date_joined = vals['date_joined']
            name += ":"+date_indian(vals['date_joined'])
        if 'job_id' in vals:
            job_id = vals['job_id']
            name += ":"+self.env['hr.job'].browse(vals['job_id']).name        
        
        contract_data = {
                     'name': name,
                     'job_id': job_id,
                     'employee_id':(hr_employee_id.ids)[0],
                     'type_id': 1,
                     'struct_id': 1,
                     'date_start': date_joined,
                     'wage': 0.0,
                     'schedule_pay':'monthly',
                     'state':'draft'
                        }
        self.env["hr.contract"].create(contract_data)
          
        return hr_employee_id
        

        
    
Employee() 