import telebot
from telebot import *
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context
bot = telebot.TeleBot("")

#global vuoro  #vaihda tahan https://stackoverflow.com/questions/10851906/python-3-unboundlocalerror-local-variable-referenced-before-assignment

#kohdat = [-1,-1,-1,-1,-1,-1,-1,-1,-1,]

class Peli:
  def __init__(self, vuoro, kohdat):
    self.vuoro = vuoro
    self.kohdat = list(kohdat)

tictactoe = Peli(0, [-1,-1,-1,-1,-1,-1,-1,-1,-1,])

#Harkitse OOPin avulla julkista bottia
#Rekisteröi pelaajat X:ksi ja O:ksi

#Tee verify ominaisuus
chat_id = -1001202328267

def oikearyhma(message):
    if chat_id == message.chat.id:
        return True
    else:
        return False

def pyyhilauta():
    tictactoe.kohdat = [-1,-1,-1,-1,-1,-1,-1,-1,-1,]

def taulu():
    nro = 0
    teksti = ""
    print(tictactoe.kohdat)
    for laatikko in tictactoe.kohdat:
        nro += 1
        if laatikko == 0:
            laatikko = "x"
        if laatikko == 1:
            laatikko = "o"
        if laatikko == -1:
            laatikko = " "
        if nro == 3:
            teksti += laatikko + " "
            teksti += "\n--+---+---\n"
            nro = 0
        else:
            teksti += laatikko + " | "
    return teksti

def tarkastavoitto():
    if tictactoe.kohdat[0] ==  tictactoe.kohdat[1] ==  tictactoe.kohdat[2] : return tictactoe.kohdat[0] #vertikaalit
    if tictactoe.kohdat[3] ==  tictactoe.kohdat[4] ==  tictactoe.kohdat[5] : return tictactoe.kohdat[3]
    if tictactoe.kohdat[6] ==  tictactoe.kohdat[7] ==  tictactoe.kohdat[8] : return tictactoe.kohdat[6]
    if tictactoe.kohdat[0] ==  tictactoe.kohdat[3] ==  tictactoe.kohdat[6] : return tictactoe.kohdat[0] #horisontaalit
    if tictactoe.kohdat[1] ==  tictactoe.kohdat[4] ==  tictactoe.kohdat[7] : return tictactoe.kohdat[1]
    if tictactoe.kohdat[2] ==  tictactoe.kohdat[5] ==  tictactoe.kohdat[8] : return tictactoe.kohdat[2]
    if tictactoe.kohdat[0] ==  tictactoe.kohdat[4] ==  tictactoe.kohdat[8] : return tictactoe.kohdat[0] #Diagonaali 1
    if tictactoe.kohdat[6] ==  tictactoe.kohdat[4] ==  tictactoe.kohdat[2] : return tictactoe.kohdat[6] #Diagonaali 2

taulu()

def onkotasapeli():
    montako = 0
    for kohta in tictactoe.kohdat:
        if kohta == -1:
            montako += 1
        else:
            pass
    if montako < 1:
        return True
    else:
        return False

def pilaileeko(pilailevamuuttuja):
    if pilailevamuuttuja.isdigit():
        if int(pilailevamuuttuja) < 1 or int(pilailevamuuttuja) > 9:
            return True
        else:
            return False
    else:
        return True

@bot.message_handler(commands=['start', 'apua', 'komennot', 'aloita'])
def apu_ja_aloitus(message):
    if oikearyhma(message):
        bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<pre>+------------------+\n|      OHJEET      |\n| Siirtojen muoto: |\n|1 = kohta 1       |\n|4 = kohta 4       |\n+------------------+</pre>")

@bot.message_handler(commands=['lauta'])
def aloitapeli(message):
    if oikearyhma(message):
        if tictactoe.vuoro == 0:
            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<pre>" + taulu() + "</pre>\n\nVuoro ✖️")
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<pre>" + taulu() + "</pre>\n\nVuoro ⭕️")

@bot.message_handler(commands=['pyyhilauta'])
def pyyhilautakomento(message):
    if oikearyhma(message):
        pyyhilauta()
        bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>❕Lauta on pyyhitty!</b>")

@bot.message_handler(commands=['siirto'])
def teesiirto(message):
    if oikearyhma(message):
        kokoteksti = message.text #TODO: tarkasta onko tiedosto jo olemassa
        kohde = kokoteksti.split()[1:]
        try:
            siirto = kohde[0]
        except IndexError:
            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>❕Kerro siirtosi!</b>")
            return
        else:
            siirto = kohde[0]
            if pilaileeko(siirto):
                bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>❕Eipäs mennä pelilaudan ulkopuolelle!</b>")
            else:
                if tictactoe.vuoro == 0:
                    ruutu = int(siirto)-1
                    if tictactoe.kohdat[ruutu] == -1:
                        kohta = ruutu
                        if tictactoe.kohdat[ruutu] == -1:
                            tictactoe.kohdat[kohta] += 1
                            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<i>Siirto tehty!</i>")
                            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<pre>" + taulu() + "</pre>\n\nVuoro ⭕️") #✖️✔️
                            if tarkastavoitto() == 0:
                                bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>🎉🎉 X (✖️) voitti!</b>")
                                pyyhilauta()
                            if onkotasapeli():
                                bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>🤔 Tasapeli...</b>")
                                pyyhilauta()
                            tictactoe.vuoro += 1
                        else:
                            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>❗️Paikka on jo valittu!</b>") #

                else:
                    ruutu = int(siirto)-1
                    if tictactoe.kohdat[ruutu] == -1:
                        kohta = ruutu
                        tictactoe.kohdat[kohta] += 2
                        bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<i>Siirto tehty!</i>")
                        bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<pre>" + taulu() + "</pre>\n\nVuoro ✖️") #
                        if tarkastavoitto() == 1:
                            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>🎉🎉 X (⭕️) voitti!</b>")
                            pyyhilauta()
                        if onkotasapeli():
                            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>🤔 Tasapeli...</b>")
                            pyyhilauta()
                        tictactoe.vuoro -= 1
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text="<b>❗️Paikka on jo valittu!</b>") #✖️
bot.polling()
