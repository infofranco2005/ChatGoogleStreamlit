import streamlit as st
import google.generativeai as genai
import os
import time # Para simular o loading

# --- Configuração da API Key ---
try:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if GOOGLE_API_KEY is None:
        st.error("A chave API 'GOOGLE_API_KEY' não foi encontrada. Por favor, configure-a como uma variável de ambiente.")
        st.stop()
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Ocorreu um erro inesperado ao configurar a API: {e}")
    st.stop()

# --- Configurações do Modelo de IA ---
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

@st.cache_resource
def get_gemini_model():
    return genai.GenerativeModel(model_name="gemini-2.0-flash",
                                 generation_config=generation_config,
                                 safety_settings=safety_settings)

model = get_gemini_model()

# --- Função Principal do Aplicativo Streamlit ---
def meu_amigo_nerd_streamlit():
    st.set_page_config(
        page_title="Meu Amigo Nerd 📚",
        page_icon="🤖" # Ícone de robôzinho na aba do navegador
    )

    # --- Estilo CSS Personalizado para um Toque Nerd ---
    st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a2e; /* Fundo escuro */
            color: #e0e0e0; /* Cor do texto claro */
            font-family: 'Courier New', monospace; /* Fonte com estilo de terminal/código */
        }
        .st-emotion-cache-1c7y2qn { /* Classe do container principal, pode mudar com as versões */
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            color: #00ff00; /* Verde neon para o título */
            text-align: center;
            font-size: 2.5em;
            text-shadow: 0 0 10px #00ff00; /* Brilho no título */
        }
        .stMarkdown {
            color: #b0b0b0;
        }
        .stTextInput label {
            color: #00ff00 !important; /* Cor do label do input */
            font-size: 1.1em;
        }
        .stTextInput div div input {
            background-color: #2b2b4d; /* Fundo do input */
            color: #00ff00; /* Texto do input */
            border: 1px solid #00ff00; /* Borda do input */
            border-radius: 8px;
            padding: 10px;
        }
        .stTextInput div div input:focus {
            box-shadow: 0 0 10px #00ff00; /* Brilho no foco */
        }
        .stButton button {
            background-color: #00ff00; /* Cor do botão */
            color: #1a1a2e; /* Texto do botão */
            border-radius: 8px;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #00cc00; /* Cor do botão ao passar o mouse */
        }
        .st-chat-message-user div {
            background-color: #4a4a6e; /* Fundo da mensagem do usuário */
            color: #e0e0e0;
            border-radius: 15px 15px 0 15px; /* Bordas arredondadas */
            padding: 10px 15px;
            margin-bottom: 10px;
        }
        .st-chat-message-assistant div {
            background-color: #004d00; /* Fundo da mensagem do assistente (verde escuro nerd) */
            color: #e0e0e0;
            border-radius: 15px 15px 15px 0; /* Bordas arredondadas */
            padding: 10px 15px;
            margin-bottom: 10px;
        }
        .st-chat-message-user .st-emotion-cache-s1h49p { /* Avatar do usuário */
            background-image: url("https://em-content.zobj.net/source/microsoft-teams/337/person_1f9d1.png"); /* Ícone de pessoa */
            background-size: cover;
            width: 35px;
            height: 35px;
            border-radius: 50%;
        }
        .st-chat-message-assistant .st-emotion-cache-s1h49p { /* Avatar do assistente */
            background-image: url("https://em-content.zobj.net/source/microsoft-teams/337/robot_1f916.png"); /* Ícone de robô */
            background-size: cover;
            width: 35px;
            height: 35px;
            border-radius: 50%;
        }
        /* Ajuste para o avatar de robô com óculos */
        .st-chat-message-assistant .st-emotion-cache-s1h49p {
             background-image: url('https://i.imgur.com/your_nerd_robot_icon.png'); /* **IMPORTANTE: COLOQUE AQUI O LINK DO SEU ÍCONE DE ROBOZINHO COM ÓCULOS** */
             background-size: cover;
             width: 40px; /* Ajuste o tamanho conforme necessário */
             height: 40px; /* Ajuste o tamanho conforme necessário */
             border-radius: 50%;
             border: 2px solid #00ff00; /* Borda verde neon */
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Conteúdo Principal ---
    st.title("🤖 Meu Amigo Nerd! 📚")
    st.markdown("Olá! Sou seu assistente de estudos. Faça uma pergunta sobre suas aulas e vou te ajudar a entender!")
    st.markdown("---")

    # Inicializa o histórico do chat na sessão do Streamlit
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat = model.start_chat(history=[])

    # Exibe o histórico do chat
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    # Campo de entrada para a pergunta do usuário
    pergunta = st.chat_input("✏️ Faça sua pergunta aqui...")

    if pergunta:
        st.chat_message("user").write(pergunta)
        st.session_state.chat_history.append(("user", pergunta))

        if not pergunta.strip():
            with st.chat_message("assistant"):
                st.write("Por favor, digite uma pergunta para que eu possa ajudar.")
            st.session_state.chat_history.append(("assistant", "Por favor, digite uma pergunta para que eu possa ajudar."))
            return # Sai da função para evitar processamento desnecessário

        # --- Adiciona o loading antes da resposta ---
        with st.chat_message("assistant"):
            with st.spinner("🤓 Pensando..."):
                try:
                    prompt_para_ia = f"""
                    Você é "Meu Amigo Nerd", um assistente de IA amigável e paciente, especializado em ajudar alunos do ensino fundamental e médio a entenderem suas aulas.
                    Responda à pergunta do aluno de forma clara, didática e encorajadora.
                    Use exemplos simples e analogias quando apropriado.
                    Se a pergunta for muito complexa ou fora do escopo escolar, tente simplificá-la ou peça ao aluno para reformulá-la.
                    Evite respostas excessivamente longas, a menos que necessário para uma boa explicação.

                    Pergunta do aluno: {pergunta}
                    """
                    response = st.session_state.chat.send_message(prompt_para_ia)
                    resposta_chatbot = response.text

                    st.write(resposta_chatbot)
                    st.session_state.chat_history.append(("assistant", resposta_chatbot))

                except Exception as e:
                    st.error(f"😥 Desculpe, ocorreu um erro ao tentar processar sua pergunta: {e}")
                    st.write("Tente perguntar de uma forma diferente ou verifique sua conexão e configuração da API.")
                    st.session_state.chat_history.append(("assistant", f"😥 Desculpe, ocorreu um erro: {e}. Tente novamente."))

# Inicia o aplicativo Streamlit
if __name__ == "__main__":
    meu_amigo_nerd_streamlit()