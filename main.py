import os
from supabase.client import create_client, Client

supabase_url = "************************"
supabase_key = "************************"

supabase: Client = create_client(supabase_url, supabase_key)


def get_users():
    query = "*, sender_id(*), receiver_id(*)"
    return supabase.table("users").select(query).execute().data


def get_transactions():
    query = "*, sender_id(*), receiver_id(*)"
    return supabase.table("transactions").select(query).execute().data


transactions = get_transactions()
for transaction in transactions:
    sender = transaction["sender_id"]["name"]
    receiver = transaction["receiver_id"]["name"]
    amount = transaction["amount"]
    reason = transaction["description"]
    timestamp = transaction["created_at"][:19]

    print(f"{timestamp}\t {sender} envió {amount}€ a {receiver} por {reason}")
