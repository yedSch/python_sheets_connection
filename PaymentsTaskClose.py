from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import gspread
import requests
import time

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("yedaya-volta-7cabc6952bb0.json",scope)

client = gspread.authorize(creds)
print(client)
sheet = client.open("CloseTaskSheet").worksheet('payments')


# sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/14ni3dp84T1xNJ77FtOev8EYpb0pqLFJs6_NzWUrS0ng/edit?ts=606962fc#gid=2080014401")

# worksheet = sheet.get_worksheet(4)

data = sheet.get_all_records()
print(len(data))
df = pd.DataFrame(sheet.get_all_records())

updated_tasks = df[df['updated'].isin(['TRUE'])]
print(len(updated_tasks))

def getProjectByName(client_name,payment_number):

    url = "https://analyticsapi.zoho.com/api/adam@volta.solar/Volta Solar Zoho Projects/Tasks Master Table?ZOHO_OUTPUT_FORMAT=JSON&ZOHO_ERROR_FORMAT=JSON&ZOHO_API_VERSION=1.0"
    all_tasks_query = f"""SELECT * FROM "Tasks Master Table" WHERE "Task Identifier" = '{payment_number}' AND "Tasks.Project Name" LIKE '%{client_name}%'"""
    print(all_tasks_query)
    params = {
        "authtoken": "1589529a40508e0e3d16dbae15169fb9",
        "ZOHO_ACTION": "EXPORT",
        "ZOHO_SQLQUERY": all_tasks_query,
        "KEY_VALUE_FORMAT": "true",
        "ZOHO_VALID_JSON": "true"
    }
    r = requests.post(url, params=params)
    print(r.status_code)
    all_tasks = r.json().get('data')
    return all_tasks


counter = 1
for index, row in updated_tasks.iterrows():
    # driver = close_task_new_version.initiateFFbrowser()
    # print(row)
    client = row['client']
    amount = row['amount']
    status = row['updated']
    payment_number = row['payment_number']
    percentage = row['percentage']
    print(client)
    print(payment_number)
    task_details = getProjectByName(client,payment_number)
    print(task_details[0])
    project_id = task_details[0]['Tasks.Project ID']
    task_id = task_details[0]['Task ID']
    task_list_id = task_details[0]['Task List ID']
    task_link = task_details[0]['Task Link']
    task_current_status = task_details[0]['Tasks.Status']

    print(project_id,task_list_id,task_id)

    if task_current_status != "Closed" and status =="TRUE":
        sheet.update_cell(index+2,6,0)

    # print(project_id)
    if counter ==1:
        break
    # task_id = getTaskId(project_id,payment_number)

    # print(client,amount)
# print(data)
# pprint(data)

# row = sheet.row_values(2)
# col = sheet.col_values(2)
# cell = sheet.cell(2,2).value
# print(worksheet)