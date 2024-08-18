from odoo import http
import requests


class DonationController(http.Controller):

    # Donation form view
    @http.route('/don/faire-un-don', type='http', auth='public', website=True)
    def donation_form(self):
        return http.request.render('mobile_money_website_payment.donation_form')

    @http.route('/don/valider', type='http', auth='public', website=True)
    def donation_submit(self, **post):
        donor_name = post.get('donor_name')
        donor_phone_number = post.get('donor_phone_number')
        amount = int(post.get('amount'))

        # Create donation record in the database
        donation = http.request.env['cinetpay.donation'].create({
            'name': donor_name,
            'phone_number': donor_phone_number,
            'amount': amount,
            'state': 'pending'
        })
        if donation:
            print('success')
        # Init CinetPay's API payment
        api_key = http.request.env['ir.config_parameter'].sudo().get_param('cinetpay.api')
        site_id = http.request.env['ir.config_parameter'].sudo().get_param('cinetpay_site_id')
        url = "https://api-notitia.cinetpay.com/v1/?method=check"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        payload = {
            'api_key': api_key,
            'site_id': site_id,
            'amount': amount,
            'currency': 'XOF',
            'transaction_id': str(donation.id),
            'description': 'Don a DCR',
            'return_url': '/don/thanks',
            'notify_url': '/don/notify'
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            donation.transaction_id = data.get('transaction_id')
            return http.request.redirect(data.get('payment_url'))
        else:
            donation.state = 'cancelled'
            return http.request.render('mobile_money_website_payment.donation_error')

    # Thanks view
    @http.route('/don/thanks', type='http', auth='public', website=True)
    def donation_thanks(self, **kwargs):
        return http.request.render('mobile_money_website_payment.donation_thanks')

    # Notify view
    @http.route('/don/notify', type='json', auth='public', csrf=False)
    def donation_notify(self, **post):
        transaction_id = post.get('transaction_id')
        donation = http.request.env['cinetpay.donation'].search([('transaction_id', '=', transaction_id)], limit=1)
        if donation:
            donation.state = 'done'
        return {'status': 'success'}
