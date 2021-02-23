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
# print(data)
# pprint(data)

# row = sheet.row_values(2)
# col = sheet.col_values(2)
# cell = sheet.cell(2,2).value

df = pd.DataFrame(sheet.get_all_records())
# print(df)

taskStatusList = df['Status']
# df2[df2["E"].isin(["two", "four"])]
selectedData = df[df['Status'].isin([0])]

print(selectedData['ProjectID'])
print(df['Status'])
print(len(selectedData))
# driver = close_task.initiateGoogleBrowser()
# driver = close_task.initiateFFbrowser()
def updateSheets(action_result,index,row):
    if action_result:
        print("This is index",index)
        # row['Status']=action_result
        # edit_row = sheet.(index)['Status']
        sheet.update_cell(index+2,6,1)
        print('Task Closed, Cell Status Updated')
    else:
        print("Task was not closed...")

#set url parameters:
for index, row in selectedData.iterrows():
    driver = close_task.initiateFFbrowser()
    # print(row)
    projectid = row['ProjectID']
    tasklistid = row['TaskListID']
    taskid = row['TaskID']
    task_url = row['TaskURL']
    print("This is Index",index)
    print("This is row",row)
    # print(row)
    time.sleep(10)
    closed = close_task.Crawl(driver,projectid,tasklistid,taskid,task_url)
    # closed = 1
    updateSheets(closed,index,row)
    driver.quit()
    time.sleep(15)
# print("row",row)
# print("col",col)
# print("cell",cell)
# pprint(row)
# pprint(col)
# pprint(cell)

# projectid = sheet.row_values(sheet.col_values(5)==1)

# print(projectid)
# #sheet.insert_row(insertRow,4)
# num = sheet.row_count
# print(len(sheet.get_all_records()))
# print(sheet.get_all_records())
# driver = close_task.initiateBrowser()
# close_task.Crawl(driver,)
