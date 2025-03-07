# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class GestionPatient(models.Model):
    _name = 'gestion.patient'
    _description = 'Gestion des Patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom patient", tracking=True)
    prenom = fields.Char(string="Prénom patient",  tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    rdv_id = fields.Many2one('gestion.rdv', string="Rendez vous", required=True, tracking=True)
    status = fields.Selection([
        ('nouveau', 'Nouveu patient'),
        ('consultation', 'Consultation en cours'),
        ('termine', 'Terminé'),
        ('gueri', 'Guéri'),
        ('hospitalise', 'Hospitalisé')
    ], string="Status", default='nouveau', tracking=True)
    courriel = fields.Char(string="Courriel", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    employee_id = fields.Many2one('hr.employee', string="Employee")

    def action_valider(self):
        """Fait progresser le statut du patient à l'étape suivante"""
        for record in self:
            if record.status == 'nouveau':
                record.status = 'consultation'
                # Ajouter Anita Olivier comme abonné
                partner = self.env['res.partner'].search([('name', '=', 'Anita Oliver')], limit=1)
                if partner:
                    # Utiliser record au lieu de self pour l'abonnement
                    record.message_subscribe(partner_ids=[partner.id])
                    # Ajouter un message de confirmation
                    record.message_post(
                        body=f"Anita olivier a été ajoutée comme abonnée",
                        subtype_xmlid="mail.mt_note"
                    )
                else:
                    # Message si le contact n'est pas trouvé
                    record.message_post(
                        body="Contact 'Anita olivier' non trouvé dans le système",
                        subtype_xmlid="mail.mt_note"
                    )
            elif record.status == 'consultation':
                record.status = 'termine'
            elif record.status == 'termine':
                record.status = 'gueri'
            elif record.status == 'gueri':
                record.status = 'hospitalise'
        return True

    def action_retour(self):
        """Revient à l'étape précédente"""
        for record in self:
            if record.status == 'consultation':
                record.status = 'nouveau'
            elif record.status == 'termine':
                record.status = 'consultation'
            elif record.status == 'gueri':
                record.status = 'termine'
            elif record.status == 'hospitalise':
                record.status = 'gueri'
        return True


def get_age_statistics(self):
    """Calcule la distribution des patients par tranche d'âge."""
    age_groups = {
        '0-5': 0,
        '6-10': 0,
        '11-18': 0,
        '19-30': 0,
        '31-50': 0,
        '51+': 0
    }

    total_patients = self.search_count([])  # Nombre total de patients

    if total_patients == 0:
        return {group: 0 for group in age_groups}  # Évite la division par zéro

    # Récupérer tous les patients et les classer dans les tranches d'âge
    for patient in self.search([]):
        if patient.age <= 5:
            age_groups['0-5'] += 1
        elif 6 <= patient.age <= 10:
            age_groups['6-10'] += 1
        elif 11 <= patient.age <= 18:
            age_groups['11-18'] += 1
        elif 19 <= patient.age <= 30:
            age_groups['19-30'] += 1
        elif 31 <= patient.age <= 50:
            age_groups['31-50'] += 1
        else:
            age_groups['51+'] += 1

    # Convertir en pourcentage
    age_percentages = {group: round((count / total_patients) * 100, 2) for group, count in age_groups.items()}

    return age_percentages
