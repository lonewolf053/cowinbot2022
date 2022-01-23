import telegram.ext as telegram
import random
import re
from datetime import date
import cowincommands as commands
import datetime
import json

with open('./apikey.json', 'r+') as apifile:
    API_Key = json.loads(apifile.read())['my_key']


HELP_TEXT = "Hello and welcome to the COWIN helper bot.\nYou have the following commands:\n\n/pin <space> pin code <space> date(DD-MM-YYYY) : \nGet a list of available centres using pin code and date.\n\n/district <space> district <space> state <space> date(DD-MM-YYYY): \nGet a list of available centres in a district."  # TODO: Fill in HELP data
hello_text = HELP_TEXT + "\n\n /help:\n Shows all commands"


def start(update, context):
    update.message.reply_text(hello_text)


def help_user(update, context):
    update.message.reply_text(HELP_TEXT)


def pin(update, context):
    try:
        context.args[1] = datetime.datetime.strptime(context.args[1], '%d-%m-%Y').strftime('%d-%m-%Y')
    except IndexError:
        context.args += [date.today().strftime('%d-%m-%Y')]
    except:
        context.args[1] = date.today().strftime('%d-%m-%Y')
    try:
        # print(context.args)
        # pcode = context.args[0].replace(' ', '')
        if not context.args[0].replace(' ', '').isdigit() or not re.match(
                re.compile("^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"), context.args[0].replace(' ', '')):
            raise BrokenPipeError
    except BrokenPipeError:
        update.message.reply_text('Invalid Pin code')
    except IndexError:
        if len(context.args) < 2:
            update.message.reply_text('Arguments incomplete')
    else:
        # update.message.reply_text('Your pin is %s and date is %s' % (context.args[0].replace(' ', ''), context.args[1]))
        if commands.getpin(context.args[0], context.args[1]):
            for i in commands.getpin(context.args[0], context.args[1]):
                x = "\n          ".join(i['slots'])
                update.message.reply_text(f'''
Centre name : {i['name']}
Address : {i['address']}
Slots:  {x}
Vaccine : {i['vaccine']}
Fee : {i['fee']}
Minimum Age : {i['min_age_limit']}
                            ''')
            # TODO: do stuff with pincode
        else:
            update.message.reply_text('No data found. Please try again with a different date and/or pin')


def handle_text(update, context):
    msg = update.message.text.lower().strip()
    greetings = ['hello', 'hi', 'hola', 'greetings']
    if msg in greetings:
        del greetings[greetings.index(msg)]
        update.message.reply_text(random.choice(greetings) + '!')
    else:
        update.message.reply_text('Sorry, I do not understand')


def districts(update, context):
    # TODO: Complete processing of districts
    try:
        update.message.reply_text('Here is a list of all the available districts in %s' % context.args[0])
    except:
        update.message.reply_text('Please provide name of state')


def bydistrict(update, context):
    try:
        context.args[2] = datetime.datetime.strptime(context.args[1], '%d-%m-%Y').strftime('%d-%m-%Y')
    except IndexError:
        context.args += [date.today().strftime('%d-%m-%Y')]
    except:
        context.args[2] = date.today().strftime('%d-%m-%Y')
    if commands.getdist(context.args[0], context.args[1], context.args[2]):
        for i in commands.getdist(context.args[0], context.args[1], context.args[2]):
            x = "\n           ".join(i['slots'])
            update.message.reply_text(f'''
Centre name : {i['name']}
Address : {i['address']}
Pin: {i['pincode']}
Slots:  {x}
Vaccine : {i['vaccine']}
Fee : {i['fee']}
Minimum Age : {i['min_age_limit']}''')
    else:
        update.message.reply_text('No data found. Please try again with a different state,district and/or pin')


updater = telegram.Updater(API_Key, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.CommandHandler('start', start))
disp.add_handler(telegram.CommandHandler('getDistricts', districts, pass_args=True))
disp.add_handler(telegram.CommandHandler('help', help_user))
disp.add_handler(telegram.CommandHandler('pin', pin, pass_args=True))
disp.add_handler(telegram.CommandHandler('district', bydistrict, pass_args=True))
disp.add_handler(telegram.MessageHandler(telegram.Filters.text, handle_text))

updater.start_polling()
updater.idle()
