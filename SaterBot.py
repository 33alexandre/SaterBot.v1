import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader

url = 'https://youtu.be/oa9GcjNaeZQ?si=YEmcY80bjxFAFEM5'

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key
chat = ChatGroq(model='llama-3.3-70b-versatile')


def resposta_bot(mensagens, documento):
    message_system = '''Você é um assistente chamado SaterBot.
    você utiliza as segintes informações para formular as suas repostas {informações}'''
    mensagens_modelo = [('system', message_system)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informações': documento}).content


print('Bem-vindo ao SaterBot!')

def carrega_site():
    url_site = input('Digite a url do site: ')
    loader = WebBaseLoader(url_site)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento +=  doc.page_content
    return documento


def carrega_pdf():
    caminho_pdf = '/home/alexandre/asimov/RoteiroViagemEgito.pdf'
    loader_pdf = PyPDFLoader(caminho_pdf)
    lista_documentos = loader_pdf.load()
    documento = ''
    for doc in lista_documentos:
        documento +=  doc.page_content
    return documento


def carrega_yt():
    url_yt= input('digite a url do vídeo: ')
    loader = YoutubeLoader.from_youtube_url(
    url_yt,
    language = ['pt']
    )
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento +=  doc.page_content
    return documento


texto_selecao = '''
digite 1 para conversar com um site
digite 2 para conversar com um pdf
digite 3 para conversar com um video do youtube
==> '''

mensagens = []

while True:
    selecao = input(texto_selecao)
    if selecao == '1':
        documento = carrega_site()
        break
    if selecao == '2':
        documento = carrega_pdf()
        break
    if selecao == '3':
        documento = carrega_yt()
        break
    print('digite um valor entre 1 e 3: ')


while True:
    pergunta = input('user: ')
    if pergunta.lower() == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens, documento)
    mensagens.append(('assistant', resposta))
    print(f'bot {resposta}')
print('Obrigado por usar o SaterBot (:')
mensagens = []

while True:
    selecao = input(texto_selecao)
    if selecao == '1':
        documento = carrega_site()
        break
    if selecao == '2':
        documento = carrega_pdf()
        break
    if selecao == '3':
        documento = carrega_yt()
        break
    print('digite um valor entre 1 e 3: ')


while True:
    pergunta = input('user: ')
    if pergunta.lower() == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens, documento)
    mensagens.append(('assistant', resposta))
    print(f'bot {resposta}')
print('Obrigado por usar o SaterBot (:')