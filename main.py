import subprocess

print("Fetching emails...")
subprocess.run(["python", "Fetch_Mails.py"])

print("Summarizing emails...")
subprocess.run(["python", "summarize.py"])

print("Done!")