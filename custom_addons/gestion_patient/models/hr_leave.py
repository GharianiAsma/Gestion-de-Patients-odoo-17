# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    suivi_patient_requis = fields.Boolean(string="Suivi Patient Requis")

    # Supprimez la définition de domaine dans le champ
    patient_assigne_id = fields.Many2one(
        'gestion.patient',
        string="Patient Assigné"
    )

    # Ajoutez cette méthode pour calculer le domaine dynamiquement
    @api.depends('employee_id')
    def _compute_patient_domain(self):
        for record in self:
            if record.employee_id and record.employee_id.patient_ids:
                return [('id', 'in', record.employee_id.patient_ids.ids)]
            return [('id', '=', False)]  # Ne retourne aucun résultat si pas d'employé

    # Utilisez cette méthode comme domaine
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """Met à jour le domaine pour le champ patient_assigne_id"""
        domain = [('id', '=', False)]  # Par défaut, aucun résultat
        if self.employee_id and hasattr(self.employee_id, 'patient_ids'):
            # Vérifiez si patient_ids existe sur l'employé
            if self.employee_id.patient_ids:
                domain = [('id', 'in', self.employee_id.patient_ids.ids)]
        return {'domain': {'patient_assigne_id': domain}}

    @api.constrains('suivi_patient_requis', 'patient_assigne_id')
    def _check_patient_assignment(self):
        """ Empêche d'enregistrer un congé avec suivi patient sans patient assigné """
        for leave in self:
            if leave.suivi_patient_requis and not leave.patient_assigne_id:
                raise ValidationError("Un patient doit être assigné si le suivi patient est requis.")

    @api.onchange('suivi_patient_requis')
    def _onchange_suivi_patient_requis(self):
        """ Affiche un avertissement si 'Suivi Patient Requis' est activé sans assignation de patient. """
        if self.suivi_patient_requis and not self.patient_assigne_id:
            return {
                'warning': {
                    'title': "Assignation de patient requise",
                    'message': "Vous devez assigner un patient si le suivi est requis.",
                }
            }

    # Override pour ignorer la vérification de chevauchement pour les suivis patients
    def _check_overlap(self, date_from, date_to, employee_id):
        """ Vérifie s'il y a chevauchement avec d'autres congés,
            sauf si c'est pour un suivi patient requis """
        # Si le congé est pour un suivi patient, on ignore la vérification
        if self.suivi_patient_requis and self.patient_assigne_id:
            return False
        return super(HrLeave, self)._check_overlap(date_from, date_to, employee_id)

    # Méthode alternative pour les versions plus récentes d'Odoo (17+)
    def _get_overlapping_leaves(self):
        """Obtient les congés qui se chevauchent mais ignore ceux avec suivi patient"""
        if self.suivi_patient_requis and self.patient_assigne_id:
            return self.env['hr.leave']  # Retourne un recordset vide
        return super(HrLeave, self)._get_overlapping_leaves()