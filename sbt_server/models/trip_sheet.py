# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class site(models.Model):
    _name ='sbt.site'
    _description='Site'
    
    name = fields.Char('Site')
    
class area(models.Model):
    _name='sbt.area'
    _description='Area'
    
    name = fields.Char('Area')

class SbtSiteInfo(models.Model):
    _name = 'sbt.site.info'
    _description = 'Site Information'
    
    site_id = fields.Many2one('sbt.site', 'Site Name', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft','Draft'), ('active','Active'), ('archived','Archived')], 'State', default='draft')
    sbt_site_info_line_ids = fields.One2many('sbt.site.info.lines', 'sbt_site_info_id', 'Site Info Lines', required=True, readonly=True, states={'draft': [('readonly', False)]})
                
class SbtSiteInfoLines(models.Model):
    _name = 'sbt.site.info.lines'
    _description = 'Site Info Lines'
    
    sbt_site_info_id = fields.Many2one('sbt.site.info', 'Site Info ID')
    serial_no = fields.Integer('S.NO')
    area_id = fields.Many2one('sbt.area', 'My Commute Area', required=True, readonly=True, states={'draft': [('readonly', False)]})
    one_way = fields.Integer('One way')
    two_way = fields.Integer('Two way')
    state = fields.Selection([('draft','Draft'), ('active','Active'), ('archived','Archived')], 'State', default='draft')
    
class trip_sheet_entry(models.Model):
    _name = 'trip.sheet.entry'
    _description = 'Trip Sheet Entry'
    
    trip_date = fields.Date('Date', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft','Draft'), ('active','Active'), ('archived','Archived')], 'State', default='draft')
    trip_sheet_entry_line_ids = fields.One2many('trip.sheet.entry.lines', 'trip_sheet_entry_id', 'Trip Sheet Entry Lines', required=True, readonly=True, states={'draft': [('readonly', False)]})
    
class trip_sheet_entry_lines(models.Model):
    _name = 'trip.sheet.entry.lines'
    _description = 'Trip Sheet Entry Lines'
    
    trip_sheet_entry_id = fields.Many2one('Trip Sheet Entry')
    state = fields.Selection([('draft','Draft'), ('active','Active'), ('archived','Archived')], 'State', default='draft')
    site_id = fields.Many2one('sbt.site', 'Site Name', required=True, readonly=True, states={'draft': [('readonly', False)]})
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True, readonly=True, states={'draft': [('readonly', False)]})
    area_id = fields.Many2one('sbt.area', 'My Commute Area', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft','Draft'), ('active','Active'), ('archived','Archived')], 'State', default='draft')
    pickup_type = fields.Selection([('pickup','Pickup'), ('drop','Drop'), ('passing','Passing')], required=True, readonly=True, states={'draft': [('readonly', False)]})
    passing_kms = fields.Integer('Passing kms', readonly=True, states={'draft': [('readonly', False)]})
    total_kms = fields.Integer('Kilometers')
    
    
    @api.onchange('passing_kms')
    def onchange_passing_kms(self):
        if self.passing_kms and isinstance(self.passing_kms, int):
            self.total_kms += self.passing_kms 
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    