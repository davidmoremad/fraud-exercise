import os
from supabase.client import create_client, Client

supabase_url = "*************************"
supabase_key = "*************************"

supabase: Client = create_client(supabase_url, supabase_key)


def get_users():
    query = "*"
    return supabase.table("users").select(query).execute().data


def get_transactions():
    query = "*, sender_id(*), receiver_id(*)"
    return supabase.table("transactions").select(query).execute().data


def is_fraud(transaction):
    sender = transaction["sender_id"]
    receiver = transaction["receiver_id"]
    amount = transaction["amount"]
    description = transaction["description"]
    # Sender details
    sender_name = sender["name"] + " " + sender["surname"]
    sender_email = sender["email"]
    sender_country = sender["country"]
    # Receiver details
    receiver_name = receiver["name"] + " " + receiver["surname"]
    receiver_email = receiver["email"]
    receiver_country = receiver["country"]

    # Si pais de origen y destino es diferente, es fraude
    if sender_country != receiver_country:
        return True

    # Si el monto es mayor a 4000€, reportar como fraude
    if amount > 4000:
        return True

    # Si el emisor y el receptor son la misma persona, es fraude
    if (
        sender == receiver
        or sender_email == receiver_email
        or sender_name == receiver_name
    ):
        return True

    # @proton.me son emails usados por criminales, reportar como fraude
    if "@proton.me" in sender_email:
        return True

    return False


transactions = get_transactions()
for transaction in transactions:
    if is_fraud(transaction):
        sender = transaction["sender_id"]["name"]
        receiver = transaction["receiver_id"]["name"]
        amount = transaction["amount"]
        reason = transaction["description"]
        timestamp = transaction["created_at"][:19]

        print(f"{timestamp}\t {sender} envió {amount}€ a {receiver} por {reason}")
