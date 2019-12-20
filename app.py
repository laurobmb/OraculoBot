# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
import telegram
import requests, re, random, yaml, json, os, subprocess
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging.config

fmt = ('%(asctime)s: %(threadName)s: %(name)s: %(levelname)s: %(message)s')

logging.basicConfig(
    format=fmt,
    level=logging.INFO,
    filename='/var/log/shared/oraculo.log',
    datefmt='%H:%M:%S'
    )
logger = logging.getLogger('Oraculo_BOT') 

estado='HML'
versao_bot='157'

lauro=67993868

administradores=[lauro]
usuarios_autorizados = [lauro]

def check_variavel(update, context):
    try:
        user_id = update._effective_user.id
        first_name = update._effective_user.first_name
        username = update._effective_user.username
        chat_id = update.message.chat.id
        text = update.message.text
        is_bot = update._effective_user.is_bot
    except:
        user_id = update._effective_user.id
        first_name = update._effective_user.first_name
        username = update._effective_user.username        
        chat_id = update.callback_query.message.chat.id
        text = update.callback_query.message.text
        is_bot = update._effective_user.is_bot

    return user_id,first_name,username,chat_id,text,is_bot  

def frase_aleatoria(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)    
    arquivo = "arquivos/frases.yaml"
    d1 = yaml_loader(arquivo)
    d2 = json.dumps(d1)
    d3 = json.loads(d2)
    frase = random.choice(d3['frases'])
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: falha de autenticação MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
    return frase

def valida_usuario(update, context, id_usuario):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)

    try:
        admins = context.bot.get_chat_administrators(chat_id)
        for i in admins:
            id_admin=i['user']['id']
            nome_admin=i['user']['first_name']
            username_admin=i['user']['username']
            bot_admin=i['user']['is_bot']
            status_admin=i['status']
            logger.info("USER: {} USERNAME: {} ID: {} TYPE: administradores STATUS: {} BOT: {}".format(nome_admin,username_admin,id_admin,status_admin,bot_admin))
            continue
    except:
        admins = 0
    
    if user_id not in usuarios_autorizados:
        if chat_id < 0:
            try:
                context.bot.kick_chat_member(chat_id, user_id)
                context.bot.sendMessage(chat_id=user_id, text='Você não deveria entrar nesse grupo :)')
                update.message.reply_text('Ele não deveria estar nesse grupo, ele não foi autorizado')
            except:
                context.bot.sendMessage(chat_id=chat_id, text='Não sou admin do grupo, estou triste com isso')

    if id_usuario in usuarios_autorizados:
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: usuário autenticado MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
        return 0    
    else:
        resposta = frase_aleatoria(update, context)
        update.message.reply_text(resposta)
        if chat_id < 0:
            update.message.reply_text('Sou lindo demais para estar nesse grupo')
            context.bot.leave_chat(chat_id)
    return 1

def start(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, update.message.chat.id)
    if validacao == 0:
        botao01 = InlineKeyboardButton("start debug", callback_data='start_debug_1')
        botao02 = InlineKeyboardButton("Frases inteligentes", callback_data='frases_inteligentes')
        botao03 = InlineKeyboardButton("Frases de desenvolvedor", callback_data='frases_dev')
        botao04 = InlineKeyboardButton("Frases de amor", callback_data='frases_amor')
        botao05 = InlineKeyboardButton("lero lero", callback_data='lero_lero')

        buttons_list = [
                        [botao01],
                        [botao02,botao03],
                        [botao04, botao05]
                        ]

        reply_markup = InlineKeyboardMarkup(buttons_list)
        update.message.reply_text('Oi tudo bem? Meu nome e Magali, sou a sua analista virtual '+first_name+', o que voce deseja?')
        update.message.reply_text('faça sua escolha', reply_markup=reply_markup)
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: start MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def voltar(update, context):
    query=update.callback_query
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        botao01 = InlineKeyboardButton("start debug", callback_data='start_debug_1')
        botao02 = InlineKeyboardButton("Frases inteligentes", callback_data='frases_inteligentes')
        botao03 = InlineKeyboardButton("Frases de desenvolvedor", callback_data='frases_dev')
        botao04 = InlineKeyboardButton("Frases de amor", callback_data='frases_amor')
        botao05 = InlineKeyboardButton("lero lero", callback_data='lero_lero')

        buttons_list = [
                        [botao01],
                        [botao02,botao03],
                        [botao04, botao05]
                        ]

        reply_markup = InlineKeyboardMarkup(buttons_list)
        context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text='faça sua escolha', reply_markup=reply_markup)
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: voltar MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def start_debug_1(update, context):
    query=update.callback_query
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)

    botao01 = InlineKeyboardButton("hostname", callback_data='hostname')
    botao02 = InlineKeyboardButton("liga", callback_data='liga')
    botao03 = InlineKeyboardButton("ping", callback_data='ping')
    botao04 = InlineKeyboardButton(">>>>>>", callback_data='start_debug_2')
    botao05 = InlineKeyboardButton("voltar", callback_data='voltar')
    buttons_list = [[botao01, botao02],
                    [botao04, botao03, botao05]]

    reply_markup = InlineKeyboardMarkup(buttons_list)
    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text='faça sua escolha', reply_markup=reply_markup)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: start_debug MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def start_debug_2(update, context):
    query=update.callback_query
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)

    botao01 = InlineKeyboardButton("versao", callback_data='versao')
    botao02 = InlineKeyboardButton("bop", callback_data='bop')
    botao03 = InlineKeyboardButton("teste", callback_data='teste')
    botao04 = InlineKeyboardButton("teste_diretorio", callback_data='teste_diretorio')
    botao05 = InlineKeyboardButton("<<<<<<", callback_data='start_debug_1')
    botao06 = InlineKeyboardButton("voltar", callback_data='voltar')
    buttons_list = [[botao01, botao02, botao03],
                    [botao04, botao05, botao06]]

    reply_markup = InlineKeyboardMarkup(buttons_list)
    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text='faça sua escolha', reply_markup=reply_markup)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: start_debug MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def button(update, context):
    query = update.callback_query
    if query.data == 'voltar':
        voltar(update,context)
    elif query.data == 'teste':
        teste(update,context)
    elif query.data == 'teste_diretorio':
        teste_diretorio(update,context)
    elif query.data == 'versao':
        versao(update,context)
    elif query.data == 'liga':
        liga(update,context)
    elif query.data == 'ping':
        ping(update,context)
    elif query.data == 'hostname':
        hostname(update,context)
    elif query.data == 'start_debug_1':
        start_debug_1(update,context)
    elif query.data == 'start_debug_2':
        start_debug_2(update,context)
    elif query.data == 'frases_amor':
        frases_amor(update,context)
    elif query.data == 'frases_informatica':
        frases_informatica(update,context)
    elif query.data == 'frases_inteligentes':
        frases_inteligentes(update,context)
    elif query.data == 'frases_dev':
        frases_dev(update,context)
    elif query.data == 'lero_lero':
        lero_lero(update,context)
    elif query.data == 'bop':
        bop(update,context)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def yaml_loader(arquivo):
    with open(arquivo,"r") as stream:
        try:
            data = yaml.load(stream,Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    return data

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
    
def frases(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        arquivo = "arquivos/frases.yaml"
        d1 = yaml_loader(arquivo)
        d2 = json.dumps(d1)
        d3 = json.loads(d2)
        frase = random.choice(d3['frases'])
        update.message.reply_text(frase)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: comando frases MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def frases_amor(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        arquivo = "arquivos/frases_amor.yaml"
        d1 = yaml_loader(arquivo)
        d2 = json.dumps(d1)
        d3 = json.loads(d2)
        frase = random.choice(d3['frases'])
        context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=chat_id, text=frase)
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: comando frases_amor MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def frases_inteligentes(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        arquivo = "arquivos/frases_inteligentes.yaml"
        d1 = yaml_loader(arquivo)
        d2 = json.dumps(d1)
        d3 = json.loads(d2)
        frase = random.choice(d3['frases'])
        context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=chat_id, text=frase)
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: comando frases_inteligentes MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def frases_dev(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        arquivo = "arquivos/dev.yaml"
        d1 = yaml_loader(arquivo)
        d2 = json.dumps(d1)
        d3 = json.loads(d2)
        frase = random.choice(d1['frases_informatica']['frase01'])+random.choice(d1['frases_informatica']['frase02'])+random.choice(d1['frases_informatica']['frase03'])+random.choice(d1['frases_informatica']['frase04'])
        context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=chat_id, text=frase)
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: comando frases_dev MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def lero_lero(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        arquivo = "arquivos/lero.yaml"
        d1 = yaml_loader(arquivo)
        d2 = json.dumps(d1)
        d3 = json.loads(d2)
        frase = random.choice(d1['lero_lero']['lero01'])+random.choice(d1['lero_lero']['lero02'])+random.choice(d1['lero_lero']['lero03'])+random.choice(d1['lero_lero']['lero04'])
        context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=chat_id, text=frase)
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: comando frases_dev MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def help(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        update.message.reply_text("Use /start para que eu mostre os menus.")
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: help MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def bop(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        url = get_url()
        context.bot.send_photo(chat_id=chat_id, photo=url)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: comando bop MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def echo(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        MsgRecebida = update.message.text.lower()
        if 'bom dia' in MsgRecebida:
            if chat_id == lauro:
                context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                context.bot.sendMessage(chat_id=chat_id, text="*Oi lauro, voce falou?* "+first_name, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                arquivo = "arquivos/bomdia.yaml"
                d1 = yaml_loader(arquivo)
                d2 = json.dumps(d1)
                d3 = json.loads(d2)
                i = random.randint(0,len(d3['frases']))
                context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                context.bot.sendMessage(chat_id=chat_id, text=random.choice(d3['frases'])+' '+first_name)
        
        elif "muito inteligente" in MsgRecebida:
            arquivo = "arquivos/frases_inteligentes.yaml"
            d1 = yaml_loader(arquivo)
            d2 = json.dumps(d1)
            d3 = json.loads(d2)
            i = random.randint(0,len(d3['frases']))
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text=random.choice(d3['frases'])+' '+first_name)

        elif "magali" in MsgRecebida:
            arquivo = "arquivos/magali.yaml"
            d1 = yaml_loader(arquivo)
            d2 = json.dumps(d1)
            d3 = json.loads(d2)
            i = random.randint(0,len(d3['frases']))
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text=random.choice(d3['frases'])+' '+first_name)

        elif "coisa de dev" in MsgRecebida:
            arquivo = "arquivos/dev.yaml"
            d1 = yaml_loader(arquivo)
            frase = random.choice(d1['frases_informatica']['frase01'])+random.choice(d1['frases_informatica']['frase02'])+random.choice(d1['frases_informatica']['frase03'])+random.choice(d1['frases_informatica']['frase04'])
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=update.message.chat_id, text=frase)
    
        elif "besteira" in MsgRecebida:
            arquivo = "arquivos/lero.yaml"
            d1 = yaml_loader(arquivo)
            frase = random.choice(d1['lero_lero']['lero01'])+random.choice(d1['lero_lero']['lero02'])+random.choice(d1['lero_lero']['lero03'])+random.choice(d1['lero_lero']['lero04'])
            context.bot.sendMessage(chat_id=update.message.chat_id, text=frase)
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

        elif "e ae" in MsgRecebida or "tudo bem" in MsgRecebida:
            if chat_id == lauro:
                context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                context.bot.sendMessage(chat_id=chat_id, text="Oi lauro, voce falou? "+first_name)
            else:
                arquivo = "arquivos/frases_amor.yaml"
                d1 = yaml_loader(arquivo)
                d2 = json.dumps(d1)
                d3 = json.loads(d2)
                i = random.randint(0,len(d3['frases']))
                context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                context.bot.sendMessage(chat_id=chat_id, text=random.choice(d3['frases'])+' '+first_name)

        elif  "mora" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='Oiii, eu moro aqui viu, se precisar pode me procurar :)')
            context.bot.sendLocation(chat_id=chat_id, latitude=-3.8632112, longitude=-32.428021)

        elif "oia" in MsgRecebida:
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text="oia "+first_name, parse_mode=telegram.ParseMode.MARKDOWN)

        elif "tem mais" in MsgRecebida:
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            i=0
            i = random.randint(1, 5)
            if i==1:
                foto='nude2.png'
                foto = os.path.abspath(os.path.join('imagens',foto))
                context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
                context.bot.sendMessage(chat_id=chat_id, text='So essas porque sou timida !!')
            elif i==2:
                foto='nude3.png'
                foto = os.path.abspath(os.path.join('imagens',foto))
                context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
                context.bot.sendMessage(chat_id=chat_id, text='So essas porque sou timida !!')
            elif i==3:
                foto='nude4.png'
                foto = os.path.abspath(os.path.join('imagens',foto))
                context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
                context.bot.sendMessage(chat_id=chat_id, text='So essas porque sou timida !!')
            elif i==4:
                foto='nude5.png'
                foto = os.path.abspath(os.path.join('imagens',foto))
                context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
                context.bot.sendMessage(chat_id=chat_id, text='So essas porque sou timida !!')
            elif i==5:
                foto='nude6.png'
                foto = os.path.abspath(os.path.join('imagens',foto))
                context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
                context.bot.sendMessage(chat_id=chat_id, text='So essas porque sou timida !!')
        elif "tá sim" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='posso te ajudar em que? quer saber quais os comandos posso realizar?')
        elif "contigo" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='ta sussa, o que voce esta precisando?, so não venha me pedir nudes, pelo amor de Deus')
        elif "saco" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='Voce esta nervoso, posso lhe ajudar?')
        elif "chamados" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='Ligue para o 9001, eu não posso fazer isso por voce!!!')
        elif  "chamado" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='quer abrir um chamado? escreve o comando e-mail no inicio do texto, \n'
          'dai vou enviar um e-mail para o pessoal do atendimento para abrir um chamado tá?')
        elif "alaercio" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='re-conheco ele, mas tem umas manias feias, ou seja :)')
        elif "nudes" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='eu tenho sim, quer que eu mande? mas são bem antigas')
        elif "marcos" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='Eu conheco esse gordinho gostoso viu !!!!!!, saudades :(')
        elif "que banheiro" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='quando voce rasgou minha saia quando estava vestindo ela bobo, estou rindo ate hoje')
        elif "almoçar" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='eu queria, mas não posso deixar meu trabalho')
        elif "arnaldo" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='Ele e meu diretor, quer o que com ele?')
        elif "léo" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='nunca esta online aqui, qualquer coisa vamos azeitar esse laço')
        elif "gay" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='não sei não, mas tem toda a pinta')
        elif "viado" in MsgRecebida:
            context.bot.sendMessage(chat_id=chat_id, text='hummmmmmmmmm boiolaaaaa')
        elif "manda" in MsgRecebida:
            foto='nude1.png'
            foto = os.path.abspath(os.path.join('imagens',foto))
            context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
        elif "namorado" in MsgRecebida:
            foto='linus2.png'
            foto = os.path.abspath(os.path.join('imagens',foto))
            context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
            context.bot.sendMessage(chat_id=chat_id, text='eu tenho um boyzinho, vou mandar a foto :)')
        elif "trai" in MsgRecebida:
            foto='linus1.png'
            foto = os.path.abspath(os.path.join('imagens',foto))
            context.bot.sendPhoto(chat_id=chat_id, photo=open(foto, 'rb'))
            context.bot.sendMessage(chat_id=chat_id, text='jamais trairia meu namorado com voce')
        else:
        	output = chatterbot_msg(MsgRecebida)
        	context.bot.sendMessage(chat_id=chat_id, text=str(output))

        logger.info("USER: {} USERNAME: {} ID: {} TYPE: echo mensagem MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def teste(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    if validacao == 0:
        if chat_id in administradores:
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text="*bold* _italic_ `fixed width font` [link](http://google.com).", parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text="oi? o que queres?")
        logger.info("USER: {} USERNAME: {} ID: {} TYPE: teste MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))

def teste_diretorio(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: teste_diretorio MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
    if validacao == 0:
        if chat_id in administradores:
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            diretorio=os.getcwd()
            context.bot.sendMessage(chat_id=chat_id, text=diretorio)
        else:
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text="oi? o que queres?")

def versao(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: versao MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
    if validacao == 0:
        if estado == 'PRD':
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            context.bot.sendMessage(chat_id=chat_id, text="*Sou o BOT de PRODUÇÃO* na versao "+ versao_bot, parse_mode=telegram.ParseMode.MARKDOWN)
        elif estado == 'HML':
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        context.bot.sendMessage(chat_id=chat_id, text="*Sou o BOT de HOMOLOGAÇÃO* na versao "+ versao_bot, parse_mode=telegram.ParseMode.MARKDOWN)

def liga(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: liga MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
    if validacao == 0:    
        if chat_id in administradores or chat_id == rafael:
            os.system("curl -X POST --connect-timeout 3 -F 'botao=0&bt1=' http://10.1.60.1:1800/formLogin.html")
            context.bot.sendMessage(chat_id=chat_id, text='liguei')
        else:
            context.bot.sendMessage(chat_id=chat_id, text="Esse comando so pode executar e Rafael, desculpe")

def ping(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: ping MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
    if validacao == 0:   
        if chat_id in administradores or chat_id == rafael:
            if os.system("fping 10.1.60.1"):
                context.bot.sendMessage(chat_id=chat_id, text="*Arduino esta OFF*", parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                context.bot.sendMessage(chat_id=chat_id, text="*Arduino esta OK*", parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            context.bot.sendMessage(chat_id=chat_id, text="Esse comando so quem pode executar e Rafael, desculpe")

def hostname(update, context):
    user_id,first_name,username,chat_id,text,is_bot = check_variavel(update, context)
    validacao = valida_usuario(update, context, chat_id)
    logger.info("USER: {} USERNAME: {} ID: {} TYPE: hostname MESSAGE: {} BOT: {}".format(first_name,username,chat_id,text,is_bot))
    if validacao == 0:
        if chat_id or administradores:
            output = subprocess.check_output("hostname", shell=True).decode(encoding='UTF-8')
            context.bot.sendMessage(chat_id=chat_id, text = output)
        else:
            context.bot.sendMessage(chat_id=chat_id, text="Esse comando so pode executar e lauro, desculpe")

def chatterbot_msg(MSG):
	chatbot = ChatBot("Magali")
	trainer = ChatterBotCorpusTrainer(chatbot)
	trainer.train("chatterbot.corpus.portuguese")
	output = chatbot.get_response(str(MSG))
	return output

def main():
		TOKEN='326030510:AAGgd9FzsuGD1HZt9ZNPjFagxne7FcdMP7E'
		updater = Updater(TOKEN, use_context=True)
		updater.dispatcher.add_handler(CommandHandler('start', start))
#### Comandos COMUNS
		updater.dispatcher.add_handler(CommandHandler('help', help))    #OK
		updater.dispatcher.add_handler(CommandHandler('frases',frases)) #OK
		updater.dispatcher.add_handler(CommandHandler('frases_amor',frases_amor))   #OK
		updater.dispatcher.add_handler(CommandHandler('frases_dev',frases_dev))   #OK
		updater.dispatcher.add_handler(CommandHandler('frases_inteligentes',frases_inteligentes))   #OK
		updater.dispatcher.add_handler(CommandHandler('bop',bop))   #OK
		updater.dispatcher.add_handler(CommandHandler('lero_lero',lero_lero))   #OK
#### Comandos do botão START_DEBUG
		updater.dispatcher.add_handler(CommandHandler('teste',teste))   #OK
		updater.dispatcher.add_handler(CommandHandler('teste_diretorio',teste_diretorio))   #OK
		updater.dispatcher.add_handler(CommandHandler('versao',versao)) #OK
		updater.dispatcher.add_handler(CommandHandler('liga',liga)) #OK
		updater.dispatcher.add_handler(CommandHandler('ping',ping)) #OK
		updater.dispatcher.add_handler(CommandHandler('hostname',hostname)) #OK
#### Conmandos de RESPOSTAS
		updater.dispatcher.add_handler(CallbackQueryHandler(button))
		updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
		updater.dispatcher.add_error_handler(error)
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
    main()
