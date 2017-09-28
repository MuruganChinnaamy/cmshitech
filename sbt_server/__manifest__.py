# -*- coding: utf-8 -*-

# Customized Module for Managing Vehicles by Deta Entity.


{
    'name': 'SBT vehicle Management',
    'version': '1.0',
    'category': 'Vehicle Management',
    'author': 'Deta Entity, Chennai',
    'website': 'detaentity.in',
    'summary' : 'Vehicle, leasing, insurances, costs',
    'description' : """
Vehicle, leasing, insurances, cost
==================================
With this module, Odoo helps you managing all your vehicles, the
contracts associated to those vehicle as well as services, fuel log
entries, costs and many other features necessary to the management 
of your fleet of vehicle(s)

Main Features
-------------
* Add vehicles to your System
* Manage contracts for vehicles
* Reminder when a contract reach its expiration date
* Add services, fuel log entry, odometer values for all vehicles
* Show all costs associated to a vehicle or to a type of service
* Analysis graph for costs
""",
    'depends': [
        'hr',
        'hr_payroll',
        'hr_contract',
        'hr_holidays',
        'hr_attendance',
        'base',
        'mail',
        'fleet',
        
        
    ],
    'data': [
        'security/sbt_security.xml',
        'security/ir.model.access.csv',
        'views/view_vehicle_info.xml',
        'views/trip_sheet_view.xml',
        'views/hr_view.xml',
        'views/hr_payroll_view.xml',
        'views/allowances_and_deductions_view.xml',
	
    ],

    'demo': [],

    'installable': True,
    'application': True,
}
