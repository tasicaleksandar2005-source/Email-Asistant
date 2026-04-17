import anthropic
import pyodbc

#uzima api key iz key.txt-a
with open("key.txt", "r") as f:
    api_key = f.read().strip()

#key
client = anthropic.Anthropic(api_key=api_key)

#connecting to database
conection = pyodbc.connect(
        "DRIVER={SQL Server};"
        "Server=NEKOMPIJUTER\\SQLEXPRESS02;"
        "Database=Emailbot;"
        "Trusted_Connection=yes"
    )
cursor = conection.cursor()

#get mails that i didnt get alredy
cursor.execute("SELECT ID, Naslov, Sadrzaj FROM EmailTabela WHERE Opis IS NULL")
emails = cursor.fetchall()

#get mails here
for email in emails:
    id = email[0]
    subject = email[1]
    body = email[2]
    #give claude mails
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this email in 2-3 sentences and give it a category (e.g. Work, Finance, Spam, Personal). Subject: {subject}\n\nBody: {body}\n\nRespond in this format:\nSummary: ...\nCategory: ..."
            }
        ]
    )
    #we take only claudes answer for result
    result = response.content[0].text

    summary = ""
    category = ""

    for line in result.splitlines():
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Category:"):
             category = line.replace("Category:", "").strip()

    cursor.execute("UPDATE EmailTabela SET Opis = ?, Kategorija = ? WHERE ID = ?", (summary, category, id))


conection.commit()
cursor.close()
conection.close()