from email.message import EmailMessage
import pygsheets
import datetime
gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')

sh = gc.open('kbthebest18@gmail.com')

# gc.sheet.create("Tesstttt")
# sh = gc.open("Tesstttt")
# sh.share("kbthebest181@gmail.com", role='writer', type = 'user', emailMessage = 'Helzu')
# sh.add_worksheet("test1")
# print(sh)
sh.delete()

# wks.create_protected_range()




