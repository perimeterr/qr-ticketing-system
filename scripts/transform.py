import gspread
import uuid
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('../credentials.json', scope)
client = gspread.authorize(creds)

ss = client.open("Tickets_Database") 
resp_sheet = ss.worksheet("Ticket Order Form")
master_sheet = ss.worksheet("Master_Tickets")

responses = resp_sheet.get_all_records()
existing = master_sheet.get_all_records()
processed_times = {str(row['order_timestamp']) for row in existing}

new_tickets = []
ticket_types = ['VIP-Balcony', 'VIP-Floor', 'GenAd-Floor'] 

for row in responses:
    ts = str(row['Timestamp'])
    if ts in processed_times:
        continue 

    for t_type in ticket_types:
        qty = row.get(t_type, 0)
        if qty and int(qty) > 0:
            for _ in range(int(qty)):
                new_tickets.append([
                    str(uuid.uuid4()), 
                    row['Full Name'],
                    t_type,
                    'Valid',           
                    ts                 
                ])

if new_tickets:
    master_sheet.append_rows(new_tickets)
    print(f"Added {len(new_tickets)} tickets to Master_Tickets!")
else:
    print("No new orders found.")