# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import Warning, UserError


class MissionExterne(models.Model):
    _name = 'mission.externe'
    _description = 'Mission Externe'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Service Number', copy=False, default="Nouveau")
    person_name = fields.Many2one('res.partner', string="Nom et Prénom", required=True)
    employee_id = fields.Many2one('hr.employee', string='Employée', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True )
    date_creation = fields.Date(string='Date de Création', default=fields.Date.context_today, store=True, required=False)
    date_exp = fields.Date(string='Date d\'expération', required=False)

    @api.onchange('date_exp')
    def check_date(self):
        if self.date_exp != False:
            date_exp_string = datetime.strptime(str(self.date_exp), "%Y-%m-%d")
            date_create_string = datetime.strptime(str(self.date_creation), "%Y-%m-%d")
            if date_exp_string < date_create_string:
                raise UserError("la date d'expiration doit être supérieure à la date de création")


    mission = fields.Selection( string='Mission', selection=[('externe_all', 'Mission Externe Aller'),
                                                            ('externe_ret', 'Mission Externe Retour'),],
                                required=True, store=True, index=True, readonly=True, tracking=True, default="externe_all", change_default=True)
    passport = fields.Char(string='Numéro de Passport', required=False)
    objet = fields.Text(string="Objet Mission", required=False)

    post_v = fields.Char( string='Poste de voyage', required=False)
    chauffeur = fields.Boolean(string='Chauffeur', required=False)
    n_chauffeur = fields.Char(string='Nom de Chauffeur', required=False)
    chauffeur_cont = fields.Char(string='Contact de Chauffeur', required=False)
    matricule = fields.Char(string='Matricule de Véhicule', required=False)
    duree_b = fields.Char(string='Durée d\'util. de Véhi.',required=False)
    responsable = fields.Char(string='Nom de Responsable', required=False)
    post = fields.Char(string='Post de responsable', required=False)

    test_c = fields.Boolean(string='Test COVID', required=False)
    date_c = fields.Date(string='Date de test covid',required=False)

    hotel = fields.Char(string='Nom de Hotel', required=False)
    duree_s = fields.Float(string='Duree de séjour', required=False)
    duree_h = fields.Float( string='Duree de séjour hotel', required=False)

    frais_h = fields.Selection(string='Frais de hotel', selection=[('employee', 'Employée'), ('webb', 'Webb Fentaine')], required=False, )

    point_equi = fields.Text( string='Point Equipement', required=False)
    satisfact = fields.Selection(string='Satisfaction', selection=[('mauv', 'Mauvaise'),
                                                                   ('pass', 'Passable'),
                                                                   ('a_bien', 'Assez-bien'),
                                                                   ('bien', 'Bien'),
                                                                   ('t_bien', 'Trés-bien'),
                                                                   ('excel', 'Excelente'),], required=False, )



    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mission.externe') or _('Nouveau')
        res = super(MissionExterne, self).create(vals)
        return res


class MissionInterne(models.Model):
    _name = 'mission.interne'
    _description = 'Mission Interne'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Service Number', copy=False, default="Nouveau")
    person_name = fields.Many2one('res.partner', string="Nom et Prénom", required=True)
    employee_id = fields.Many2one('hr.employee', string='Employée', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True )
    date_creation = fields.Date(string='Date de Création', default=fields.Date.context_today, store=True, required=False)
    date_exp = fields.Date(string='Date d\'expération', required=False)

    @api.onchange('date_exp')
    def check_date(self):
        if self.date_exp != False:
            date_exp_string = datetime.strptime(str(self.date_exp), "%Y-%m-%d")
            date_create_string = datetime.strptime(str(self.date_creation), "%Y-%m-%d")
            if date_exp_string < date_create_string:
                raise UserError("la date d'expiration doit être supérieure à la date de création")


    mission = fields.Selection( string='Mission', selection=[('interne_all', 'Mission étranger départ'),
                                                            ('interne_ret', 'Mission étranger retour'),],
                                required=True, store=True, index=True, readonly=True, tracking=True, default="interne_all", change_default=True)

    passport = fields.Char(string='Numéro de Passport', required=False)
    objet = fields.Text(string="Objet Mission", required=False)
    o_mission = fields.Selection(string='Ordre de mission', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    biller = fields.Selection(string='Achat Biller d\'avion', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    visa = fields.Selection(string='Visa', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    l_invitation = fields.Selection(string='Lettre d\'invitation', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )

    vehicule = fields.Selection(string='Besoin de véhicule?', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    n_chauffeur = fields.Char(string='Nom de Chauffeur', required=False)
    chauffeur_cont = fields.Char(string='Contact de Chauffeur', required=False)
    matricule = fields.Char(string='Matricule de Véhicule', required=False)
    duree_b = fields.Char(string='Durée d\'util. de Véhi.',required=False)
    responsable = fields.Char(string='Nom de Responsable', required=False)
    post = fields.Char(string='Post de responsable', required=False)

    test_c = fields.Selection(string='Test COVID', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_c = fields.Date(string='Date de test covid',required=False)

    frais_m = fields.Selection(string='Frais de Mission', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_f = fields.Date(string='Date de frais de mission', required=False)
    p_financier= fields.Selection(string='Point financier?', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_pf = fields.Date(string='Date point financier', required=False)


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mission.interne') or _('Nouveau')
        res = super(MissionInterne, self).create(vals)
        return res

class MissionOrdinaire(models.Model):
    _name = 'mission.ordinaire'
    _description = 'Mission Ordinaire'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Service Number', copy=False, default="Nouveau")
    person_name = fields.Many2one('res.partner', string="Nom et Prénom", required=True)
    employee_id = fields.Many2one('hr.employee', string='Employée', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True )
    date_creation = fields.Date(string='Date de Création', default=fields.Date.context_today, store=True, required=False)
    date_exp = fields.Date(string='Date d\'expération', required=False)

    @api.onchange('date_exp')
    def check_date(self):
        if self.date_exp != False:
            date_exp_string = datetime.strptime(str(self.date_exp), "%Y-%m-%d")
            date_create_string = datetime.strptime(str(self.date_creation), "%Y-%m-%d")
            if date_exp_string < date_create_string:
                raise UserError("la date d'expiration doit être supérieure à la date de création")


    mission = fields.Selection( string='Mission', selection=[('ordinaire_all', 'Mission ordinaire aller'),
                                                            ('ordinaire_ret', 'Mission ordinaire retour'),],
                                required=True, store=True, index=True, readonly=True, tracking=True, default="ordinaire_all", change_default=True)

    passport = fields.Char(string='Numéro de Passport', required=False)
    objet = fields.Text(string="Objet Mission", required=False)
    o_mission = fields.Selection(string='Ordre de mission', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    biller = fields.Selection(string='Achat Biller d\'avion', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    visa = fields.Selection(string='Visa', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    l_invitation = fields.Selection(string='Lettre d\'invitation', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )

    vehicule = fields.Selection(string='Besoin de véhicule?', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    n_chauffeur = fields.Char(string='Nom de Chauffeur', required=False)
    chauffeur_cont = fields.Char(string='Contact de Chauffeur', required=False)
    matricule = fields.Char(string='Matricule de Véhicule', required=False)
    duree_b = fields.Char(string='Durée d\'util. de Véhi.',required=False)
    responsable = fields.Char(string='Nom de Responsable', required=False)
    post = fields.Char(string='Post de responsable', required=False)

    test_c = fields.Selection(string='Test COVID', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_c = fields.Date(string='Date de test covid',required=False)

    frais_m = fields.Selection(string='Frais de Mission', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_f = fields.Date(string='Date de frais de mission', required=False)
    p_financier= fields.Selection(string='Point financier?', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_pf = fields.Date(string='Date point financier', required=False)


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mission.ordinaire') or _('Nouveau')
        res = super(MissionOrdinaire, self).create(vals)
        return res







