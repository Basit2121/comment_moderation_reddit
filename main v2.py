import tkinter as tk
from tkinter import messagebox
import threading
import time
from tkinter import ttk
import subprocess
import os

def install_libraries(libraries):
    for library in libraries:
        try:
            subprocess.check_call(['pip', 'install', library])
            subprocess.check_call(['pip', 'install', '--upgrade', library])
            print(f'Successfully installed {library}')
        except subprocess.CalledProcessError:
            print(f'Failed to install {library}')

    # Clear the console after installing libraries
    os.system('cls' if os.name == 'nt' else 'clear')

# List of required libraries
required_libraries = ['praw']

# Install the libraries
install_libraries(required_libraries)

import praw

def monitor_reported_comments():
    # Get the values from the input fields
    username = entry_username.get()
    password = entry_password.get()
    client_id = entry_client_id.get()
    client_secret = entry_client_secret.get()
    user_agent = entry_username.get()
    subreddit_name = entry_subreddit.get()

    reddit = praw.Reddit(
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    subreddit = reddit.subreddit(subreddit_name)

    while True:
        print('Monitoring reported comments...')
        reported_comments = subreddit.mod.reports(limit=None)

        for report in reported_comments:
            comment = report[1]
            print(f'Processing comment: {comment.id}')
            print(f'Comment content: {comment.body}')
            comment.mod.remove()
            comment.mod.approve()
            print(f'Re-approved comment: {comment.id}')

        print('Waiting for 1 minute before checking again...')
        time.sleep(60)

def start_monitoring():
    # Create a new thread for the monitoring function
    thread = threading.Thread(target=monitor_reported_comments)
    thread.daemon = True
    thread.start()

# Create the main window
window = tk.Tk()
window.title('Reddit Bot')
window.geometry('300x500')  # Set window size

# Apply a modern theme to the window
style = ttk.Style()
style.theme_use('clam')
#window.iconbitmap('icon.ico')

# Create labels and entry fields for PRAW login details
label_username = ttk.Label(window, text='Username:')
label_username.pack()
entry_username = ttk.Entry(window)
entry_username.pack()

label_password = ttk.Label(window, text='Password:')
label_password.pack()
entry_password = ttk.Entry(window, show='*')
entry_password.pack()

label_client_id = ttk.Label(window, text='Client ID:')
label_client_id.pack()
entry_client_id = ttk.Entry(window)
entry_client_id.pack()

label_client_secret = ttk.Label(window, text='Client Secret:')
label_client_secret.pack()
entry_client_secret = ttk.Entry(window)
entry_client_secret.pack()

# Create label and entry field for subreddit name
label_subreddit = ttk.Label(window, text='Subreddit:')
label_subreddit.pack(pady=10)
entry_subreddit = ttk.Entry(window)
entry_subreddit.pack()

# Create a button to start the monitoring
button_start = ttk.Button(window, text='Start Monitoring', command=start_monitoring)
button_start.pack(pady=20)

copyright_text = "\nDiscord : basit_t1\nEmail : basitm5555@gmail.com\n\n" \
                 "© 2023 RedditBot All rights reserved."
copyright_label = tk.Label(
    window, text=copyright_text, fg="gray", bg='#f5f5f5'
)
copyright_label.pack()

window.mainloop()