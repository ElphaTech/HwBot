import json
from datetime import datetime
from datetime import timedelta

fileName="homework.json"
importedJson=open(fileName,"r")
homework=json.loads(importedJson.read())
importedJson.close()

def saveJson(dictName):
    importedJson=open(fileName,"w")
    importedJson.write(json.dumps(dictName))
    importedJson.close()

year=datetime.now().year
today=datetime(year,datetime.now().month,datetime.now().day)
tomorow=today+timedelta(days=1)
modifier=0

for i in range(len(homework)):
    curI=homework[i-modifier]
    due=datetime(year,int(curI["dueMonth"]),int(curI["dueDay"]))
    if due<tomorow:
        homework.pop(i-modifier)
        modifier+=1
    else:
        print(f"- {int(curI['dueDay']):02}/{int(curI['dueMonth']):02} {curI['subject']} {curI['txt']}")

saveJson(homework)

while True:
    homework.append({})
    homework[-1]['subject']=input("Subject(3 letters): ")
    homework[-1]['txt']=input("Work: ")
    homework[-1]['dueDay']=input("Day due: ")
    homework[-1]['dueMonth']=input("Month due: ")
    print("---------------")
    saveJson(homework)