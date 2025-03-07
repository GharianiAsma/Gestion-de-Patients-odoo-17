from odoo import models, fields

class GestionRDV(models.Model):
    _name = 'gestion.rdv'
    _description = 'Rendez-vous'

    name = fields.Char(string="Créneau horaire", required=True)
    date_rdv = fields.Date(string="Date du rendez-vous")
    patient_ids = fields.One2many('gestion.patient', 'rdv_id', string="Patients")