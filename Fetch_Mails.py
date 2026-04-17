import imaplib
import pyodbc
import email
from email.utils import parsedate_to_datetime
try:
    #define what type of mail is in use
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    #login in your mail #HARDCODIRAO SI OVO ALEKSANDRE NAMESTI PROMENLJIVE DA UZIMA PODATKE DA RADI I ZA DRUGE MAILOVE
    mail.login("tasicaleksandar.2005@gmail.com", "syxt rtev pyvn njer")


    #connecting to database
    conection = pyodbc.connect(
        "DRIVER={SQL Server};"
        "Server=NEKOMPIJUTER\\SQLEXPRESS02;"
        "Database=Emailbot;"
        "Trusted_Connection=yes"
    )
    cursor = conection.cursor()

    #Take it from this box
    mail.select("inbox")

    #take all mail
    result, data = mail.search(None, "UNSEEN")
    mail_ids = data[0].split()

    #delete old
    cursor.execute("DELETE FROM EmailTabela WHERE DatumPrimanja < DATEADD(hour, -48, GETDATE())")
    conection.commit()


    #going throu all mails
    for mail_id in mail_ids:
        result, msg_data = mail.fetch(mail_id, "(RFC822)")

        #put what we got in a list (just bites)
        raw_email = msg_data[0][1]
        
        #make those bites in a mail
        msg = email.message_from_bytes(raw_email)
        
        #put things from fileds into variables
        sender = msg["From"]
        date = parsedate_to_datetime(msg["Date"])
        subject = msg["Subject"]
        
        #if mail multple parts, we just read text
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    #ako ne moze da procita nek ga preskoci
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")    
                    break
        #if one part, just take it all
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        #put it in the table
        cursor.execute("""
            INSERT INTO EmailTabela (Posiljalac, DatumPrimanja, Naslov, Sadrzaj)
            VALUES (?, ?, ?, ?)
        """, (sender, date, subject, body))
        
    #odradjivanje
    conection.commit()
except Exception as e:
    print(f"Something went wrong: {e}")
finally:
    #closing connections
    cursor.close()
    conection.close()
    mail.logout()
