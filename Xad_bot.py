import telegram
import random
import os
import RPi.GPIO as GPIO
import time




menu_keyboard = telegram.ReplyKeyboardMarkup([['/d4','/d6','/d8','/d10'],['/d12','/d20','/d100'],['/start','/bell','/foto']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=True




bot1= telegram.Bot('166813950:AAEwgLAofYspsbBWH7ULKdAyz6E_vXbBESI')
chat_id1='135365753'
#mittente1=''
voice_file_counter=0









# Definizione delle variabili dei pin del display per le porte GPIO
LCD_RS = 25	# Pin RS del display collegato a GPIO25
LCD_E  = 24	# Pin E del display collegato a GPIO24
LCD_DB4 = 23	# Pin D4 del display collegato a GPIO23
LCD_DB5 = 17	# Pin D5 del display collegato a GPIO17
LCD_DB6 = 27	# Pin D6 del display collegato a GPIO27/GPIO21 in base a Rev2/Rev 1
LCD_DB7 = 22	# Pin D7 del display collegato a GPIO22

# Definizione di alcune costanti del display
LCD_WIDTH = 16	# Caratteri del display
LCD_CHR = True	# Carattere
LCD_CMD = False	# Comando
LCD_LINE_1 = 0x80	# Indirizzo RAM del display per la prima riga
LCD_LINE_2 = 0xC0	# Indirizzo RAM del display per la seconda riga

# Costanti del clock (Timing)
E_PULSE = 0.00005
E_DELAY = 0.00005


# Inizializzazione del display
def lcd_init():
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  

# Manda la stringa del messaggio
def lcd_string(message):

# Il metodo ljust di Python restituisce la stringa giustificata a sinistra
  message = message.ljust(LCD_WIDTH," ")
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
             
def lcd_byte(bits, mode):
  # Manda i byte ai pin di dati DB4-DB7
  # bit = data
  # mode = True  per il carattere, False per il comando

  GPIO.output(LCD_RS, mode) # modalita' RS

# Bit High
  GPIO.output(LCD_DB4, False)
  GPIO.output(LCD_DB5, False)
  GPIO.output(LCD_DB6, False)
  GPIO.output(LCD_DB7, False)
  
  if bits&0x10==0x10:
    GPIO.output(LCD_DB4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_DB5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_DB6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_DB7, True)

# Abilita il pin Enable
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

# Bit Low
  GPIO.output(LCD_DB4, False)
  GPIO.output(LCD_DB5, False)
  GPIO.output(LCD_DB6, False)
  GPIO.output(LCD_DB7, False)

  if bits&0x01==0x01:
    GPIO.output(LCD_DB4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_DB5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_DB6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_DB7, True)

# Abilita il pin Enable
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   


GPIO.setmode(GPIO.BCM)	   # Imposta la modalita' BCM
GPIO.setup(LCD_E, GPIO.OUT)	   # Imposta la porta E in uscita
GPIO.setup(LCD_RS, GPIO.OUT)   # Imposta la porta RS in uscita
GPIO.setup(LCD_DB4, GPIO.OUT) # Imposta la porta DB4 in uscita
GPIO.setup(LCD_DB5, GPIO.OUT) # Imposta la porta DB5 in uscita
GPIO.setup(LCD_DB6, GPIO.OUT) # Imposta la porta DB6 in uscita
GPIO.setup(LCD_DB7, GPIO.OUT) # Imposta la porta DB7 in uscita
GPIO.setwarnings(False) # Disabilita gli avvisi GPIO


# Funzione di inizializzazione del display
lcd_init()

# Stampa di alcuni testi
lcd_byte(LCD_LINE_1, LCD_CMD)
lcd_string("Raspberry Pi")
lcd_byte(LCD_LINE_2, LCD_CMD)
lcd_string("Hello World!")








def gestione_messaggi(bot, update):
	global voice_file_counter
	
	#bot.sendMessage(update.message.chat_id, "Hai inviato: "+ update.message.text)
	if update.message.voice:
		print " ----> VOCE <----"
		voice_file_counter=voice_file_counter+1		
		if voice_file_counter==10:
			voice_file_counter=1
		
		newFile = bot.getFile(update.message.voice.file_id)
		newFile.download('voice%d' % voice_file_counter )
		os.system("omxplayer -o local voice%d &" % voice_file_counter)


	if update.message.audio:
		print " ----> AUDIO <----"
		newFile = bot.getFile(update.message.audio.file_id)
		newFile.download('audio')
		os.system("omxplayer -o local audio &")

	if update.message.video:
		print " ----> VIDEO <----"
		newFile = bot.getFile(update.message.video.file_id)
		newFile.download('video')
		os.system("omxplayer -o local video &")
		
	if update.message.text:
		bot.sendMessage(update.message.chat_id, "Hai inviato: "+ update.message.text)
		message1=update.message.text[0:16]
		message2=update.message.text[16:32]
		lcd_byte(LCD_LINE_1, LCD_CMD)
		lcd_string(message1)
		lcd_byte(LCD_LINE_2, LCD_CMD)
		lcd_string(message2)


def comando_start(bot, update):
	mittente = update.message.from_user.first_name
	bot.sendMessage(update.message.chat_id, "Ciao %s !\n" % mittente, reply_markup=menu_keyboard)
	#bot.sendChatAction(update.message.chat_id, telegram.ChatAction.UPLOAD_PHOTO)
	#global chat_id1
	#chat_id1 = update.message.chat_id
	#global mittente1
	#mittente1 = update.message.from_user.first_name
	#global bot1
	#bot1= bot
	
def dado_4(bot, update, args):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,4)
	
	testo_add = " ".join(args)
	if len(testo_add)>0:
	 bot.sendMessage(update.message.chat_id, text = testo_add)	
	
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))	

def dado_6(bot, update):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,6)
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))
	
def dado_8(bot, update):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,8)
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))
	
def dado_10(bot, update):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,10)
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))
	
def dado_12(bot, update):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,12)
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))
	
def dado_20(bot, update):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,20)
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))
	
def dado_100(bot, update):
	mittente = update.message.from_user.first_name
	ris=random.randint(1,100)
	bot.sendMessage(update.message.chat_id, " %s il risultato del tuo lancio e' %s !\n" % (mittente, ris))
	
def bell(bot, update):
	bot.sendChatAction(update.message.chat_id, telegram.ChatAction.UPLOAD_AUDIO)
	bot.sendAudio(update.message.chat_id, open("Doorbell.mp3"))
	

def sconosciuto(bot, update):
	bot.sendMessage(update.message.chat_id, "Comando non valido /help \n")

def gestione_pulsante(channel):
	bot1.sendMessage(chat_id1, "ATTENZIONE e' stato premuto il pulsante!\n")
	print("Premuto il pulsante")
	
def send_foto(bot, update):
	print "Richiesta foto da", update.message.from_user
	#print "Richiesta foto da", update.message.from_user.first_name," con id", update.message.chat_id
	bot.sendChatAction(update.message.chat_id, telegram.ChatAction.UPLOAD_PHOTO)
	os.system("python webcam.py")
	time.sleep(3)
	bot.sendPhoto(update.message.chat_id, photo=open('photo.jpg'))

	




# Definizione variabile per il pulsante
PULSANTE = 18 # Pin 18 GPIO e' del pulsante
GPIO.setup(PULSANTE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(PULSANTE, GPIO.RISING, callback=gestione_pulsante, bouncetime=500)




updater = telegram.Updater(token='166813950:AAEwgLAofYspsbBWH7ULKdAyz6E_vXbBESI')
dispatcher = updater.dispatcher


dispatcher.addTelegramMessageHandler(gestione_messaggi)
dispatcher.addTelegramCommandHandler("start",comando_start)
dispatcher.addTelegramCommandHandler("d4",dado_4)
dispatcher.addTelegramCommandHandler("d6",dado_6)
dispatcher.addTelegramCommandHandler("d8",dado_8)
dispatcher.addTelegramCommandHandler("d10",dado_10)
dispatcher.addTelegramCommandHandler("d12",dado_12)
dispatcher.addTelegramCommandHandler("d20",dado_20)
dispatcher.addTelegramCommandHandler("d100",dado_100)
dispatcher.addTelegramCommandHandler("bell",bell)
dispatcher.addTelegramCommandHandler("foto", send_foto)
dispatcher.addUnknownTelegramCommandHandler(sconosciuto)




#bot1.sendMessage(chat_id1, "Ciao questo e' il tuo chat_id %s!\n" % chat_id1)




updater.start_polling()


updater.idle()


