# Script Automator using OpenAI API
Hello! I created this repository to automate my bi-weekly log submissions using OpenAI. My script will run once every 2 weeks, once the summaries are completed, the original `.txt` files will be removed, the summary will be saved in another folder.

## What you need:
- OpenAI API Key (You will be charged a bit of money for every query)
- App Password (if you are using Gmail), you can use any other email providers.
  - [How to get app password](https://support.google.com/accounts/answer/185833?hl=en)

## How to start:
1. Clone my repo (feel free to create your own)
```
git clone
```

2. Create a virtual environment
```
python3.9 -m venv .env
```

3. Activate the virtual environment
```
source .virtual/bin/activate
```

4. I used cron to automate my task.
```
crontab -e
```
Enter the following in the terminal:
```
30 1 1,15 * * path/to/venv/.virtual/bin/python3 path/to/generate_summary.py >> ~/out.txt 2>&1
```
This would ensure that the script is ran once every 2 weeks, reference from: [stackoverflow](https://stackoverflow.com/questions/46109358/how-to-create-a-cron-expression-for-every-2-weeks), the `~/out.txt 2>&1` is for debugging purposes, reference from: [unix stackoverflow](https://unix.stackexchange.com/questions/99263/what-does-21-in-this-command-mean)

6. Get notified when your summaries are done once every week!
