from tkinter import *
import threading
import subprocess

#button main function
def klik():

    #loading screen
    loading = Label(application, text="Loading...", font=('Arial', 15), bg="black", fg="white")
    loading.place(relx=0.5, rely=0.7, anchor="center")
    application.update()


    #run both scripts
    def run_scripts():
        subprocess.run(["python", r"e:\Pythone\Email secretary\Fetch_Mails.py"])
        subprocess.run(["python", r"e:\Pythone\Email secretary\summarize.py"])
        application.after(0, open_table)

    def open_table():
        import pyodbc

        #new window
        prozor = Toplevel(application)
        prozor.title("Emails")
        prozor.geometry("1200x600")
        prozor.config(bg="#000000")
        application.withdraw()

        headers = ["Posiljalac", "Datum", "Naslov", "Opis", "Kategorija"]

        conection2 = pyodbc.connect(
            "DRIVER={SQL Server};"
            "Server=NEKOMPIJUTER\\SQLEXPRESS02;"
            "Database=Emailbot;"
            "Trusted_Connection=yes"
        )

        def refresh():
            for widget in prozor.winfo_children():
                widget.destroy()

            cursor2 = conection2.cursor()
            cursor2.execute("SELECT Posiljalac, DatumPrimanja, Naslov, Opis, Kategorija FROM EmailTabela ORDER BY DatumPrimanja DESC")
            emails2 = cursor2.fetchall()
            cursor2.close()

            Button(prozor, text="Refresh", command=refresh, bg="gray", fg="white", font=('Arial', 10)).grid(row=0, column=0, columnspan=5, pady=5)

            for i, h in enumerate(headers):
                Label(prozor, text=h, font=('Arial', 10, 'bold'), bg="gray", fg="white", relief=RAISED, width=20).grid(row=1, column=i, padx=1, pady=1)

            for row_num, email in enumerate(emails2, start=2):
                for col_num, value in enumerate(email):
                    w = 60 if col_num == 3 else 20
                    wrap = 400 if col_num == 3 else 150
                    Label(prozor, text=str(value), font=('Arial', 9), fg="white", bg="black", relief=RAISED, width=w, wraplength=wrap).grid(row=row_num, column=col_num, padx=1, pady=1)

        refresh()
        prozor.config(bg="#000000") 
    threading.Thread(target=run_scripts).start()
#aplication name
application = Tk()

#window title and size
application.title ("Email Sumarize") 
#idk hot it works but it centers the window
application.update_idletasks()
sw = application.winfo_screenwidth()
sh = application.winfo_screenheight()
x = (sw - 560) // 2
y = (sh - 560) // 2
application.geometry(f"560x560+{x}+{y}")

#button
dugme = Button (application, text= 'FETCH AND SUMARIZE', width=30, height=2, font=('Arial',20,''), bg="black", fg="white", command=klik)
dugme.place(relx=0.5, rely=0.5, anchor="center") 


#change backgroud
application.config(bg="#000000") 

#start it
application.mainloop()