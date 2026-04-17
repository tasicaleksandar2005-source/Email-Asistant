# Email Secretary Bot

## Project Overview

Email Secretary is a Python-based desktop application that automatically fetches unread emails from a Gmail inbox, stores them in a SQL Server database, and uses the Claude AI API to generate short summaries and categories for each email. The goal is to give the user a quick overview of their inbox without having to open each email manually — like a secretary that reads your mail and tells you what each one is about.

The user can still access their original emails in Gmail at any time. This tool only reads and summarizes, it does not delete or modify any emails.

---

## Tech Stack

- **Python 3.14**
- **Gmail IMAP** — for fetching emails
- **SQL Server (SSMS)** — for storing email data
- **Claude API (claude-haiku-4-5-20251001)** — for AI summarization and categorization
- **Tkinter** — for the desktop UI
- **Libraries:** `imaplib`, `pyodbc`, `anthropic`, `email`, `tkinter`, `subprocess`, `threading`

---

## Setup & Installation

### 1. Install required libraries
```
pip install pyodbc anthropic
```

### 2. Gmail setup
- Enable IMAP in Gmail settings: Settings → Forwarding and POP/IMAP → Enable IMAP
- Generate an App Password: Google Account → Security → 2-Step Verification → App Passwords
- Use the generated 16-character password in `Fetch_Mails.py`

### 3. Claude API setup
- Create an account at [console.anthropic.com](https://console.anthropic.com)
- Generate an API key and paste it into `key.txt` in the project folder

### 4. Database setup
- Create a database called `Emailbot` in SQL Server
- Create a table called `EmailTabela` with the schema below

### 5. Run the app
```
python UIEmail.py
```
Or run the compiled `.exe` from the `dist/` folder.

---

## Database Schema

**Table: EmailTabela**

| Column | Type | Description |
|---|---|---|
| ID | INT (PK, Auto) | Unique identifier |
| Posiljalac | NVARCHAR | Sender email address |
| DatumPrimanja | DATETIME | Date and time email was received |
| Naslov | NVARCHAR | Email subject line |
| Sadrzaj | NVARCHAR(MAX) | Full email body text |
| Opis | NVARCHAR(MAX) | AI-generated summary |
| Kategorija | NVARCHAR | AI-assigned category (e.g. Work, Finance, Spam, Personal) |

---

## File Structure

| File | Purpose |
|---|---|
| `Fetch_Mails.py` | Connects to Gmail via IMAP, fetches unread emails, stores them in the database |
| `summarize.py` | Reads unsummarized emails from the DB, sends them to Claude API, saves summary and category back |
| `main.py` | Runs Fetch_Mails.py and summarize.py in sequence |
| `UIEmail.py` | Desktop UI with a fetch button and email table viewer |
| `key.txt` | Stores the Claude API key (never commit this to version control) |

---

## How It Works

1. User clicks **"Fetch and Summarize"** in the UI
2. `Fetch_Mails.py` connects to Gmail via IMAP, fetches all unread emails, and inserts them into the SQL Server database. Emails older than 48 hours are automatically deleted from the database.
3. `summarize.py` reads emails where `Opis` is NULL, sends the subject and body to the Claude API, and writes the summary and category back to the database.
4. The UI opens a new window displaying all emails from the database in a table format with columns for sender, date, subject, summary, and category.

---

## Known Issues / Limitations

- Credentials (Gmail email, App Password, server name) are currently hardcoded in `Fetch_Mails.py` and need to be moved to user input via the UI
- The app only fetches **unread** emails — already read emails in Gmail are skipped
- Emails with unusual encodings may have some characters skipped (handled with `errors="ignore"`)
- The table window does not auto-refresh; user must reopen it to see changes

---

## Future Ideas

- Add a login/settings screen in the UI for entering Gmail credentials and API key
- Add support for other email providers (Outlook, Yahoo)
- Add the ability to click on an email row and see the full body
- Add a refresh button in the table window
- Schedule automatic fetching every X hours in the background
