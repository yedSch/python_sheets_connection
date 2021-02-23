import close_task
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import time

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("yedaya-volta-7cabc6952bb0.json",scope)

client = gspread.authorize(creds)

sheet = client.open("CloseTaskSheet").sheet1

data = sheet.get_all_records()

# pprint(data)

cell_to_edit = sheet.cell(2,6).value
sheet.update_cell(2,6,1)
cell_to_edit = sheet.cell(2,6).value
pprint(cell_to_edit)