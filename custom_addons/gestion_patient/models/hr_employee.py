# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    patient_ids = fields.One2many('gestion.patient', 'employee_id', string="Employee")