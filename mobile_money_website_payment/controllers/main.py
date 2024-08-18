from odoo import http
from cinetpay_sdk.s_d_k import Cinetpay


class DonationController(http.Controller):

    # Donation form view
    @http.route('/don/faire-un-don', type='http', auth='public', website=True)
    def donation_form(self):
        return http.request.render('mobile_money_website_payment.donation_form')

    @http.route('/don/valider', type='http', auth='public', website=True)
    def donation_submit(self, **post):
        donor_surname = post.get('donor_surname')
        donor_name = post.get('donor_name')
        donor_phone_number = post.get('donor_phone_number')
        amount = int(post.get('amount'))

        donor_full_name = f"{donor_surname}  {donor_name}"

        # Create donation record in the database
        donation = http.request.env['cinetpay.donation'].create({
            'name': donor_full_name,
            'phone_number': donor_phone_number,
            'amount': amount,
            'state': 'pending'
        })

        if donation:
            print('Enregistre avec success')

        print('Initialisation ...')
        print('Obtention des information', )
        # Get CinetPay's API param via Odoo
        api_key = http.request.env['ir.config_parameter'].sudo().get_param('cinetpay.api')
        site_id = http.request.env['ir.config_parameter'].sudo().get_param('cinetpay.site_id')

        if api_key and site_id:
            print('api_key:', api_key, 'type:', type(api_key))
            print('site_id', site_id)
        else:
            print('Erreur d\'obtention des informations d\'API')

        if donation:
            # Init CinetPay
            client = Cinetpay(api_key, site_id)

            # Create transction
            data = {
                'apikey': api_key,
                'site_id': site_id,
                'amount': amount,
                'currency': 'XOF',
                'transaction_id': str(donation.id),
                'customer_surname': donor_surname,
                'customer_name': donor_name,
                'channels': 'MOBILE_MONEY',
                'customer_phone_number': f"+223{donor_phone_number}",
                'lock_phone_number': True,
                'mode': 'PRODUCTION',
                'description': 'Don a DCR',
                'return_url': 'http://localhost:8069/don/thanks',
                'notify_url': 'http://localhost:8069/don/notify'
            }
            # Call API for the payment
            response = client.PaymentInitialization(data)
            print('Response:', response)
            print('Code', response['code'])

            if 'status' in response:
                status = response['status']
                print('status', status)
                if status == '00':
                    donation.transaction_id = response.get('transaction_id')
                    donation.state = 'pending'
                    return http.request.redirect(response.get('payment_url'))
            else:
                state = 'cancelled'
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
