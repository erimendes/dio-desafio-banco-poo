# 💰 DIO - Desafio Sistema Bancário com POO

## 📘 Sobre o Projeto

Este projeto foi desenvolvido como parte do **Desafio de Projeto da [Digital Innovation One (DIO)](https://www.dio.me/)**.  
A proposta é evoluir o **sistema bancário simples** para uma versão que utiliza **Programação Orientada a Objetos (POO)** em **Python**.

O repositório contém o código-fonte de um **sistema bancário executado no terminal**, com foco em consolidar conceitos fundamentais da linguagem Python e de POO.

---

## 🚀 Funcionalidades

- 👤 Criação de usuários e contas  
- 💰 Realização de depósitos  
- 💸 Execução de saques  
- 📄 Consulta de extrato  

---

## 🧩 Requisitos

- Python **3.x** instalado no sistema  
- (Opcional) Ambiente virtual configurado com `venv` ou `poetry`

---

## ⚙️ Instalação e Execução

1. **Clone o repositório:**
```bash
    git clone <url_do_projeto_git>
```
2. Navegue até a pasta do projeto via terminal:
```bash
    cd dio-desafio-banco.
```
3. Execute o script principal com o comando:
```bash
    python desafio.py
```

## 💻 Como Usar o Sistema

Ao executar o arquivo principal, você verá o seguinte menu interativo:
```bash
================ MENU ================
[nu] Novo usuário
[nc] Nova conta
[d]  Depositar
[s]  Sacar
[e]  Extrato
[q]  Sair
======================================
```
Informe a opção desejada: nu
-> Novo usuário criado com sucesso!

Informe a opção desejada: nc
```
-> Conta criada e vinculada ao usuário.
```
Informe a opção desejada: d
```
-> Depósito de R$ 500,00 realizado com sucesso!
```
Informe a opção desejada: e
```bash
->  === EXTRATO ===
    Depósito: R$ 500,00
    Saldo atual: R$ 500,00
    =================
```
