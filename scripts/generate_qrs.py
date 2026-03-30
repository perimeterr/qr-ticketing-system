import gspread
import qrcode
import os
from oauth2client.service_account import ServiceAccountCredentials

QR_DIR = "../qrcodes"
if not os.path.exists(QR_DIR):
    os.makedirs(QR_DIR)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('../credentials.json', scope)
client = gspread.authorize(creds)

ss = client.open("Tickets_Database")
master_sheet = ss.worksheet("Master_Tickets")
tickets = master_sheet.get_all_records()

print(f"Checking {len(tickets)} tickets...")

count = 0
for t in tickets:
    uuid_str = str(t['ticket_uuid'])
    guest_name = str(t['name']).replace(" ", "_") 
    filename = f"{QR_DIR}/{guest_name}_{uuid_str[:8]}.png" 

    if not os.path.exists(filename):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uuid_str)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        
        print(f"Generated: {filename}")
        count += 1

print(f"Done! Created {count} new QR codes.")