import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace with your Telegram Bot API token
API_TOKEN = '7647483261:AAECdz_so9MJelxE-ntxpwZpI9E5zmh9zOw'
bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store the representative data
representatives = {
    'Chhatrapati Shivaji Maharaj': {
        'BE Mentor': 'Piyush: 7905061506',
        'Captain': 'Pratham Kumar: 7037719984',
        'Vice-Captain': 'Khushi Yadav: 9256517911',
        'Faculty in-charge': 'Prof MB Lonare'
    },
    'Maharana Pratap': {
        'BE Mentor': 'Pranay Puniya: 7851847604',
        'Captain': 'Krishan Kumar: 8949198900',
        'Vice-Captain': 'Ritika Kumari: 8824693065',
        'Faculty in-charge': 'Dr. Ashwini Sapkal'
    },
    'Maharaj Krishnadevaraya': {
        'BE Mentor': 'Shivram: 9351447398',
        'Captain': 'Rohit Kumar: 9462007939',
        'Vice-Captain': 'Piyush Saini: 9599478220',
        'Faculty in-charge': 'Dr. Pritee Purohit'
    },
    'Samrat Ashoka': {
        'BE Mentor': 'Ayush Ojha: 6264389700',
        'Captain': 'Ankit Yadav: 7494920441',
        'Vice-Captain': 'Akash Singh: 9571266507',
        'Faculty in-charge': 'Prof JB Jawale'
    }
}

# Starting point of the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(KeyboardButton('Maharana Pratap'),
               KeyboardButton('Chhatrapati Shivaji Maharaj'),
               KeyboardButton('Maharaj Krishnadevaraya'),
               KeyboardButton('Samrat Ashoka'))
    bot.send_message(message.chat.id, "Welcome! Please select your house:", reply_markup=markup)

# House selection
@bot.message_handler(func=lambda message: message.text in representatives)
def select_representative_type(message):
    house = message.text
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(KeyboardButton('Faculties'),
               KeyboardButton('Students'))
    bot.send_message(message.chat.id, f"You selected {house}. Now, choose representative type:", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: select_representative_role(msg, house))

# Representative type selection
def select_representative_role(message, house):
    rep_type = message.text
    if rep_type == 'Faculties':
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(KeyboardButton('Faculty in-charge'))
        bot.send_message(message.chat.id, f"You chose {rep_type}. Select the role:", reply_markup=markup)
    elif rep_type == 'Students':
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(KeyboardButton('BE Mentor'),
                   KeyboardButton('Captain'),
                   KeyboardButton('Vice-Captain'))
        bot.send_message(message.chat.id, f"You chose {rep_type}. Select the role:", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: show_contact_details(msg, house))

# Showing contact details
def show_contact_details(message, house):
    role = message.text
    contact_info = representatives[house].get(role, "No contact information available for this role.")
    bot.send_message(message.chat.id, f"Contact info for {role}: {contact_info}")
    ask_for_more_help(message)

# Asking if user needs further assistance
def ask_for_more_help(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(KeyboardButton('Yes'), KeyboardButton('No'))
    bot.send_message(message.chat.id, "Do you need further assistance?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_further_assistance)

# Further assistance handler
def handle_further_assistance(message):
    if message.text == 'Yes':
        send_welcome(message)  # Restart the bot
    else:
        bot.send_message(message.chat.id, "Thank you! Have a great day!")

# Start polling
bot.polling()
