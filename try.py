

from googleapiclient.discovery import build
import pandas
from google.oauth2 import service_account
from telegram import Update
from telegram.ext import ApplicationBuilder, filters, ContextTypes, CommandHandler, MessageHandler

token = '6152786496:AAHuv1qgAwE2H1xxOscfWyvr_4cKWZe_Vm4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials_file = 'keys.json'
creds = None

creds = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=SCOPES)
SheetID = '1cd95jAUwW5L79zC09pcy9fW6DvBnjwx40yEWpmTXpOE'
range = 'Telebot'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


def post_to_sheet(val):
    post = sheet.values().append(spreadsheetId=SheetID, range=range,
                                 valueInputOption="USER_ENTERED", body={'values': val}).execute()
    return post


def get_results():
    result = sheet.values().get(spreadsheetId=SheetID, range=range).execute()
    values = result.get('values', [])
    emp = []
    for val in values:
        emp.append(int(val[0]))
    sum = pandas.DataFrame(emp).sum().tolist()
    mean = pandas.DataFrame(emp).mean().tolist()
    stdv = pandas.DataFrame(emp).std().tolist()
    return sum, mean, stdv


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter an NUMBER for calculations")


async def users_input(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        new_msg = int(update.message.text)
        post_to_sheet([[new_msg]])
        results = get_results()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"RESULTS:\n Sum {results[0][0]}\n Mean {results[1][0]}\n Standard Deviation {results[2][0]}")
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="try again can only accept numbers!!")

while True:
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    input_handler = MessageHandler(filters.Regex(r'\d+'), users_input)
    application.add_handler(start_handler)
    application.add_handler(input_handler)
    application.run_polling()
