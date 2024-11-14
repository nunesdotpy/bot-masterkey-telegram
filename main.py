from datetime import datetime
import requests
import telebot

# Substitua 'YOUR_API_TOKEN' pelo token do seu bot
API_TOKEN = '8163341767:AAEnevGm6Zi6_8h_xGX6XnCBaKbi-GOiMZ0'
THINGSPEAK_API_URL = "https://api.thingspeak.com/channels/2739760/fields/1.json?api_key=8QGIQR5DK2TIZPTP&results=10"
bot = telebot.TeleBot(API_TOKEN)

USUARIOS = {
    "Igor": 1234,
    "João": 5678,
    "Carlos": 4321,
    "Jorge": 8765
}

@bot.message_handler(commands=['relatorio'])
def send_report(user_message):
    response = requests.get(THINGSPEAK_API_URL)
    response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
    data = response.json()
    feed = data.get('feeds', [])
    message = "Últimos feeds do Thingspeak:\n"
    for f in feed:
        created_at = f.get('created_at')
        if created_at:
            dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            formatted_time = dt.strftime("%d/%m/%y %H:%M")
        else:
            formatted_time = "N/A"
        valor = f.get('field1')
        message += f"Horário: {formatted_time}\n"
        usuario_encontrado = False
        for usuario, codigo in USUARIOS.items():
            if valor == str(codigo):
                message += f"Usuário: {usuario}\n"
                usuario_encontrado = True
                break
        if not usuario_encontrado:
            message += "Usuário: Convidado\n"
        message += "----------\n"
    bot.reply_to(user_message, message)



# Inicia o polling para receber mensagens
bot.polling()
