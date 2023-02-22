import os
from imbox import Imbox  # pip install imbox
import traceback
import ssl
import datetime
import time
# enable less secure apps on your google account
# https://myaccount.google.com/lesssecureapps
# bootleg kod av Nima --:(:O
f = open("/home/thecave/Dokument/pythonprojekt/logs.txt", "a")
tid = str(datetime.datetime.now().time())
#f.write("Kl: " + tid + "\n") #logga logga logga i din fula bil
host = "imap.one.com"
username = EMAIL
password = EMAIL_PASSWORD
download_folder = "/home/thecave/Bilder"
context = ssl._create_unverified_context()
if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)

mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=context, starttls=False)
messages = mail.messages(subject='Upload TV', unread=True)  # defaults to inbox
delete_messages = mail.messages(subject='Ta bort TV', unread=True)

for (uid, message) in messages:
    mail.mark_seen(uid)  # optional, mark message as read

    for idx, attachment in enumerate(message.attachments):
        try:
            att_fn = attachment.get('filename')
            if (att_fn.endswith(".png") or att_fn.endswith("jpg") or att_fn.endswith(".jpeg") or att_fn.endswith(".tiff") or att_fn.endswith(".bmp")):
                download_path = f"{download_folder}/{att_fn}"
                print(download_path)
                f.write("Laddat ned " + download_path + " \n")
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            else:
                print("Fel filformat")
                f.write("Fel filformat \n")


        except:
            print(traceback.print_exc())

for (delete_uid, delete_message) in delete_messages:
    mail.mark_seen(delete_uid)  # optional, mark message as read
    #print(delete_message)

    tempFil = delete_message.body.get("plain")
    tempFil = tempFil[0]
    filLista = tempFil.split("\r\n")
    fil = filLista[0]
    print(fil)
    if (fil.endswith(".png") or fil.endswith("jpg") or fil.endswith(".jpeg") or fil.endswith(".tiff") or fil.endswith(".bmp")):
        try:
            path = os.path.join(download_folder, fil)
            os.remove(path)
            print("%s has been removed successfully" %fil)
            f.write("%s has been removed successfully " + fil + " \n")
        except:
            print("Filen finns inte")
            f.write("Filen finns inte \n")
    else:
        print("fel filformat på filen som ville raderas")
        f.write("fel filformat på filen som ville raderas \n")

#gå igenom gamla filer och radera de:
directory = os.fsencode("/home/thecave/Bilder")

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    if (filename.endswith(".png") or filename.endswith("jpg") or filename.endswith(".jpeg") or filename.endswith(".tiff") or filename.endswith(".bmp")):
        if time.time() - os.path.getmtime(download_folder+"/"+filename) > (15 * 24 * 60 * 60):
            os.remove(download_folder+"/"+filename)
    else:
        continue
#haha it works. bootleg kod
f.close()
mail.logout()
