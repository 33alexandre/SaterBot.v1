import sys
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
venv_path = base_dir / "venv" / "lib64" / "python3.14" / "site-packages"
venv_path_alt = base_dir / "venv" / "lib" / "python3.14" / "site-packages"

if venv_path.exists():
    sys.path.insert(0, str(venv_path))
if venv_path_alt.exists():
    sys.path.insert(0, str(venv_path_alt))

# injeção corretiva do caminho do ambiente virtual para garantia das dependencias e do carregamento do .env
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import (
    YoutubeLoader,
    PyPDFLoader,
    WebBaseLoader,
)

# Carrega o .env da pasta correta
load_dotenv(dotenv_path=base_dir / ".env")


base_dir = Path(__file__).resolve().parent.parent
venv_lib = base_dir / "venv" / "lib" / "python3.14" / "site-packages"

if venv_lib.exists():
    sys.path.insert(0, str(venv_lib))
else:
    print(
        "Aviso: Diretório de dependências não encontrado. Certifique-se de que o ambiente virtual está configurado corretamente."
    )


# Carrega as variáveis do arquivo .env
load_dotenv()


class SaterBot:
    def __init__(self):
        """Inicializa as configurações e o modelo de IA."""
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            print("Erro: GROQ_API_KEY não encontrada no arquivo .env")
            sys.exit(1)

        # Configuração do modelo Llama via Groq
        self.chat = ChatGroq(model="llama-3.3-70b-versatile", api_key=self.api_key)
        self.historico_mensagens = []

    def carregar_conteudo(self, selecao, entrada):
        """Gerencia o carregamento de dados de diferentes fontes."""
        try:
            if selecao == "1":
                loader = WebBaseLoader(entrada)
            elif selecao == "2":
                loader = PyPDFLoader(entrada)
            elif selecao == "3":
                loader = YoutubeLoader.from_youtube_url(entrada, language=["pt", "en"])
            else:
                print("Opção inválida de carregamento.")
                return None

            # Extrai o texto de todos os documentos carregados
            documentos = loader.load()
            return "".join([doc.page_content for doc in documentos])

        except Exception as e:
            print(f"Erro ao processar a fonte: {e}")
            return None

    def obter_resposta(self, contexto, pergunta_usuario):
        """Envia o contexto e a pergunta para a IA e retorna a resposta."""
        self.historico_mensagens.append(("user", pergunta_usuario))

        # Cria o template de conversa (Prompt)
        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Você é o SaterBot. Use as seguintes informações para responder: {informacao}",
                ),
                *self.historico_mensagens,
            ]
        )

        chain = template | self.chat
        resposta = chain.invoke({"informacao": contexto}).content

        self.historico_mensagens.append(("assistant", resposta))
        return resposta


def iniciar_programa():
    """Função principal que controla o fluxo do user."""
    bot = SaterBot()

    print("--- Bem-vindo ao SaterBot! ---")
    menu = """
Escolha o que deseja analisar:
1 - Site
2 - PDF
3 - Vídeo do YouTube
==> """

    while True:
        selecao = input(menu)
        alvo = input("Digite a URL ou o caminho do arquivo: ")

        documento = bot.carregar_conteudo(selecao, alvo)

        if documento:
            print("\n Conteúdo carregado com sucesso!")
            break
        else:
            print("Tente novamente.\n")

    print("\n Agora você pode conversar com o bot (digite 'x' para sair).")

    while True:
        pergunta = input("\nUser: ")
        if pergunta.lower() == "x":
            break

        print("SaterBot pensando...")
        resposta = bot.obter_resposta(documento, pergunta)
        print(f"SaterBot: {resposta}")

    print("\n Obrigado por usar o SaterBot!")


# Input do script
if __name__ == "__main__":
    iniciar_programa()
