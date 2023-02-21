# Telegeram Bot

It **handles incoming messages** from users by **extracting the integers** from the message and **storing them in Google Sheets** and then **perform operations/calcutions** on those integers i.e `sum`, `mean` e.t.c

## Requirements

1. [Python Telegram Bot](https://pypi.org/project/python-telegram-bot/)
2. [Google Sheets API](https://developers.google.com/sheets/api/guides/concepts)
3. [Pandas](https://pypi.org/project/pandas/)
4. [Google Auth](https://pypi.org/project/google-auth/)
5. [Google Auth Oauthlib](https://pypi.org/project/google-auth-oauthlib/)
6. [Google Auth Httplib2](https://pypi.org/project/google-auth-httplib2/)
7. [Google API Python Client](https://pypi.org/project/google-api-python-client/)


## Prerequisites

Create Google Spreadsheet

1. Visit [Google Sheets](https://www.google.com/sheets/about/)
2. Click on **Go to sheets**
3. Give the sheet a title.
4. On the top right corner click on share and choose the peole you want to share the sheet with.
5. Replace the **range** value with the name of your sheet.
5. Copy the ID from the URL and add it to your application variable `SheetID`

## How to run the application

1. Clone this [repo](https://github.com/Arrotech/telegram_bot)

        git clone https://github.com/Arrotech/telegram_bot.git

2. Navigate into the directory that has been cloned to your machine and open it in a terminal.

3. Create virtual environment.

    (a). **Windows**

        python -m venv venv

    (b). **Linux**

        python3 -m venv venv


4. Activate the environment

    (a). **Windows**

        venv\Scripts\activate

    (b). **Linux**

        source venv/bin/activate

5. Install all the dependencies

        pip install -r requirements.txt

6. Run the application

        python try.py


7. Open Telegram App and serach for **@int_processor_bot**
8. Click on start
9. Type a number and you get a result i.e `sum, mean, standard deviation`

## Author

    Harun Gachanja, Software Engineer