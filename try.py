from googleapiclient.discovery import build
import pandas
from google.oauth2 import service_account
from telegram import *
from telegram.ext import ApplicationBuilder, filters, ContextTypes, CommandHandler, MessageHandler, Updater
from datetime import datetime, timedelta

token = '6134747674:AAFZebmgRopl70450N86i2RCOWfdBSmKS4w'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials_file = 'keys.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=SCOPES)
SheetID = '1L9LoClNhWKrY3MuYfnCLGJnwzYyN2kJ1FbaUGBP-W-E'
range = 'Sheet1'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


def post_to_sheet(val):
    post = sheet.values().append(spreadsheetId=SheetID, range=range,
                                 valueInputOption="USER_ENTERED", body={'values': val}).execute()
    return post


def get_results():
    result = sheet.values().get(spreadsheetId=SheetID, range=range).execute()
    values = result.get('values', [])
    global current_count
    current_count = len(values)
    emp = []
    for val in values:
        emp.append(int(val[0]))
    sum = pandas.DataFrame(emp).sum().tolist()
    mean = pandas.DataFrame(emp).mean().tolist()
    mean = round((mean[0]), 2)
    sum = str(sum[0])

    return sum, mean, current_count


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter an NUMBER for calculations")
    user_id = update.effective_chat.id
    with open("users.txt", 'r+') as file:
        reader = file.readlines()
        # reader.strip('\n')

        for id in reader:

            if str(user_id) != id:
                file.write('\n' + str(user_id))


async def users_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = get_results()[-1]
    except:
        count = 0
    finally:

        if update.message.text.isnumeric():
            new_msg = int(update.message.text)
            try:
                post_to_sheet([[new_msg]])
                if count % 20 != 0:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Received {new_msg}")
                else:
                    with open("users.txt", 'r') as file:
                        line = file.readlines()
                        try:
                            results = get_results()
                            for user in line:
                                await context.bot.send_message(chat_id=user,
                                                               text=f"RESULTS at {datetime.now().strftime('%m/%Y %H:%M ')} \n SUM: {results[0]}\n MEAN: {results[1]}")

                        except:
                            print(
                                f"{user } blocked this bot or no longer exists")

            except:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Google sheet raised an error !! Ensure the spreadsheet exists or enable share")
        else:

            await context.bot.send_message(chat_id=update.effective_chat.id, text="try again can only accept numbers!!")


async def scheduled_results(context: ContextTypes.DEFAULT_TYPE):

    with open("users.txt", 'r') as file:
        line = file.readlines()
        try:

            results = get_results()
            for user in line:
                await context.bot.send_message(chat_id=user, text=f"RESULTS at {datetime.now().strftime('%m/%Y %H:%M ')} \n SUM: {results[0]}\n MEAN: {results[1]}")
        except:
            for user in line:
                await context.bot.send_message(chat_id=user, text=f"RESULTS at {datetime.now().strftime('%m/%Y %H:%M ')} \n NO RESULTS TO PROCESS SHEET IS EMPTY")


while True:
    application = ApplicationBuilder().token(token).build()
    que = application.job_queue

    start_handler = CommandHandler('start', start)
    input_handler = MessageHandler(filters.Text(), users_input)

    send_update = que.run_repeating(scheduled_results, interval=360, first=0)
    application.add_handler(start_handler)
    application.add_handler(input_handler)
    application.run_polling()
