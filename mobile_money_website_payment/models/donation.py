from odoo import models, fields


class CinetpayPayement(models.Model):
    _name = 'cinetpay.donation'
    _description = 'Donnation'

    STATE = [
        ('draft', 'Brouillon'),
        ('pending', 'En cours'),
        ('done', 'Success'),
        ('cancelled', 'Echec')
    ]

    name = fields.Char('Nom du donnateur', required=True)
    phone_number = fields.Char('Contact du donnateur', required=True)
    amount = fields.Integer('Montant', required=True)
    transaction_id = fields.Char('ID de transaction')
    state = fields.Selection(selection=STATE, default='draft')
