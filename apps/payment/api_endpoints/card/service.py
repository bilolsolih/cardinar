import requests

from django.conf import settings

from apps.payment.models import Transaction, TransactionStatus, UserCard


class KarmonPayClient:
    create_user_card_url = "https://gw.paylov.uz/merchant/userCard/createUserCard/"
    confirm_user_card_url = "https://gw.paylov.uz/merchant/userCard/confirmUserCardCreate/"
    get_all_user_cards_url = "https://gw.paylov.uz/merchant/userCard/getAllUserCards/"
    delete_user_card_url = "https://gw.paylov.uz/merchant/userCard/deleteUserCard/"
    receipts_create_url = "https://gw.paylov.uz/merchant/receipts/create/"
    receipts_pay_url = "https://gw.paylov.uz/merchant/receipts/pay/"

    def __init__(self):
        self.headers = {"api-key": settings.PROVIDERS["karmon_pay"]["api_key"]}

    def create_user_card(self, **kwargs):
        payload = {
            "userId": kwargs["user_uuid"],
            "cardNumber": kwargs["card_number"],
            "expireDate": kwargs["expire_date"],
        }

        response = requests.post(url=self.create_user_card_url, json=payload, headers=self.headers)
        if response.ok:
            response_data = response.json()

            # if response status is success but error is not null and result is null
            if response_data.get("result", None):
                otp_sent_phone = response_data["result"]["otpSentPhone"]
                cid = response_data["result"]["cid"]
                session = response_data["result"]["session"]

                UserCard.objects.get_or_create(
                    user=kwargs["user"],
                    card_id=cid,
                    card_number=kwargs["card_number"],
                    expire_date=kwargs["expire_date"],
                )
                return False, {"otp_sent_phone": otp_sent_phone, "session": session}

            return True, response_data

        return True, response.json()

    def get_user_cards(self, user_uuid):
        query_param = {"userId": user_uuid}
        response = requests.get(url=self.get_all_user_cards_url, headers=self.headers, params=query_param)
        if response.ok:
            if response.json().get("result", None):
                return False, response.json()
            return True, response.json()
        return True, response.json()

    def confirm_user_card(self, **kwargs):
        payload = {
            "cardId": kwargs["card_id"],
            "session": kwargs["session"],
            "otp": kwargs["otp"],
        }

        response = requests.post(url=self.confirm_user_card_url, json=payload, headers=self.headers)
        if response.ok:
            if response.json().get("result", None):
                user_card = UserCard.objects.get(user=kwargs["user"], card_number=kwargs["card_number"])
                user_card.confirmed = True
                user_card.save()
                return False, {"card_number": user_card.card_number, "confirmed": user_card.confirmed}
            return True, response.json()

        return True, response.json()

    def delete_user_card(self, card_id):
        query_param = {"userCardId": card_id}
        response = requests.delete(url=self.delete_user_card_url, headers=self.headers, params=query_param)
        if response.ok:
            if response.json().get("result", None):
                return False, response.json()
            return True, response.json()
        return True, response.json()

    def create_receipt(self, order):
        payload = {
            "userId": str(order.user.uuid),
            "amount": int(order.transaction_amount),
            "account": {"order_id": order.id},
        }

        response = requests.post(url=self.receipts_create_url, json=payload, headers=self.headers)

        if response.ok:
            if response.json().get("result", None):
                return False, response.json()
            return True, response.json()
        return True, response.json()

    def pay(self, order):
        error, response = self.create_receipt(order)
        if error:
            return error, response, None
        transaction = Transaction.objects.create(
            order=order,
            transaction_id=response["result"]["transactionId"],
            amount=order.transaction_amount,
            status=TransactionStatus.WAITING,
        )
        payload = {"transactionId": transaction.transaction_id, "cardId": order.user_card.card_id}

        response = requests.post(url=self.receipts_pay_url, json=payload, headers=self.headers)

        if response.ok:
            if response.json().get("result", None):
                return False, response.json(), transaction
            return True, response.json(), transaction

        return True, response.json(), transaction
