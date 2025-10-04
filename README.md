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
```bash
python -m venv venv
```
- **Ativar o venv**:
```bash
source venv/bin/activate
```
- **Instalar as dependências**: (no diretorio base)
```bash
pip install -r requirements.txt
```
- **Entrar no diretório pra rodar o programa**:
```bash
cd Backend/Quiz4FunProject
```
- **Rodar o programa**:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Cadastro
- Completar as colunas com os seus dados
- Confirmar a criação da conta pelo link enviado ao email cadastrado
- Fazer o login utilizando e-mail e senha

## Navegação Principal
- **Página Inicial (Todos os Quizzes):** Exibe uma lista com todos os quizzes já criados por todos os usuários, permitindo descobrir novos desafios.
- **Acessando a Página Inicial:** Clique no logo **"Quiz4Fun"** no canto superior esquerdo para retornar a qualquer momento.

## Menu do Usuário
Após o login, um ícone de perfil aparecerá no canto superior direito. Ao clicar nele, você terá acesso às seguintes opções:

- **Criar Quiz:** Leva ao formulário de criação, onde é possível definir título, descrição, imagem de capa e adicionar perguntas com suas opções de resposta.
- **Meus Quizzes:** Mostra apenas os quizzes que você criou, permitindo gerenciar facilmente.
- **Logout:** Encerra a sessão e retorna à tela de login.

## Gerenciando Seus Quizzes
Na página **"Meus Quizzes"**, cada quiz terá um card com as seguintes ações:

- **Fazer Quiz:** Permite que você ou outros usuários respondam ao quiz.
- **Editar:** Abre o formulário de edição para alterar título, descrição, perguntas e opções do quiz.
- **Deletar:** Remove o quiz permanentemente, com mensagem de confirmação para evitar exclusões acidentais.

## Respondendo a um Quiz
- Clique em **"Fazer Quiz"** no card de qualquer quiz.
- Selecione uma resposta para cada pergunta.
- Clique em **"Enviar Quiz"** ao final.
- Após o envio, você será redirecionado à página de resultados para visualizar sua pontuação.
