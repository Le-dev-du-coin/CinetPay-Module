from odoo import models, fields, api
from odoo.exceptions import UserError
import requests


class SMSApi(models.Model):
    _name = 'sms.orange'
    _description = 'Orange SMS API integration'

    name = fields.Char('Nom', required=True)
    api_key = fields.Char('Cle API', required=True)
    sender_name = fields.Char('Nom Expediteur', required=True)
    sender_number = fields.Char('Numero Expediteur', required=True)

    def send_sms(self, recipient_phone_number, message):
        self.ensure_one()
        url = f"https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{self.sender_number}/requests"

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "outboundSMSMessageRequest": {
                "address": f"tel:+{recipient_phone_number}",
                "senderAddress": f"tel:+{self.sender_number}",
                "senderName": self.sender_name,
                "outboundSMSTextMessage": {
                    "message": message
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 201:
            raise UserError(f"Ereur lors de l'envoi du SMS: {response.text}")
        return response.json()


