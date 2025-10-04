# Quiz4Fun

Quiz4Fun é uma aplicação web desenvolvida para criação e compartilhamento de quizzes divertidos, permitindo que usuários criem questionários semelhantes aos encontrados em plataformas como Buzzfeed, mas com um diferencial importante: **nenhum dado pessoal dos usuários é coletado**.

---

## 👥 Criadores
- **Vinícius Machado da Rocha Viana** – Matrícula: 2111343  
- **Filipe Rogenfisch Quintans** – Matrícula: 2020857
---

## 📖 Descrição do Projeto
O **Quiz4Fun** foi desenvolvido como um projeto acadêmico com o objetivo de explorar conceitos de desenvolvimento web com **Django** no backend e templates no frontend.  

A aplicação permite:  
- Cadastro e autenticação de usuários via e-mail.  
- Ativação de conta por link enviado ao e-mail do usuário.  
- Recuperação e redefinição de senha de forma segura.  
- Criação de quizzes personalizados com perguntas e múltiplas opções de resposta.  
- Compartilhamento de quizzes com amigos.  
- Visualização e discussão dos resultados.  

---

## 🚀 Funcionalidades
- **Cadastro de usuários** com confirmação por e-mail.  
- **Login e logout** com autenticação via e-mail e senha.  
- **Gerenciamento de conta**, incluindo redefinição de senha via link enviado por e-mail.  
- **Criação de quizzes personalizados**:
  - Definição de título e descrição.  
  - Adição de múltiplas perguntas e respostas.  
- **Participação em quizzes** criados por outros usuários.  
- **Resultados imediatos**, possibilitando discussões e comparações.  

---

## 🛠️ Tecnologias Utilizadas
- **Backend**: Django 5.2.5  
- **Frontend**: HTML, CSS, Templates Django  
- **Banco de Dados**: SQLite (padrão, pode ser adaptado para outros SGBDs)  
- **Autenticação**: Sistema customizado com e-mail + envio de links de ativação e recuperação de senha  
- **Infraestrutura**: Configurado para rodar em ambiente local e no GitHub Codespaces  

---
## Como usar
- **Ambiente virtual**:
`python -m venv venv
- **Ativar o venv**:
`source venv/bin/activate
- **Instalar as dependencias**: (no diretorio base)
`pip install -r requirements.txt
- **Entrar no diretorio pra rodar o programa**:
`cd Backend/Quiz4FunProject
- **Rodar o programa**:
`python manage.py makemigrations
`python manage.py migrate
`python manage.py runserver

- **Criar uma conta**:
  