from odoo import models, fields


class CinetpaySms(models.Model):
    _name = 'cinetpay.sms'
    _description = 'Cinetpay SMS'

    STATUS = [
        ('draft', 'Brouillon'),
        ('send', 'Envoyer'),
        ('failled', 'Echec')
    ]

    name = fields.Char('ID de l\'sms', readonly=True)
    recipient = fields.Char('No destinataire', required=True)
    message = fields.Text('Message', required=True),
    status =fields.Selection('Status', selection=STATUS)