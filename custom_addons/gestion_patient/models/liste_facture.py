# -*- coding: utf-8 -*-

from odoo import models, fields


class ListeFacture(models.Model):
    _name = 'liste.facture'
    _description = 'Liste Facture'

    name = fields.Char(string="Référence", required=True)
    patient_id = fields.Many2one('gestion.patient', string="Patient", required=True)
    date_facture = fields.Date(string="Date de facturation", default=fields.Date.today)
    montant = fields.Float(string="Montant")
    state = fields.Selection([
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée')
    ], string="État", default='nouveau')