import json
import os

ARQUIVO = "produtos.json"


def carregar_produtos():
    if os.path.exists(ARQUIVO):
        arquivo = open(ARQUIVO, "r", encoding="utf-8")
        produtos = json.load(arquivo)
        arquivo.close()
        return produtos
    else:
        return []


def salvar_produtos(produtos):
    arquivo = open(ARQUIVO, "w", encoding="utf-8")
    json.dump(produtos, arquivo, ensure_ascii=False, indent=4)
    arquivo.close()


def inserir_produto(nome, preco, quantidade, categoria):
    produtos = carregar_produtos()
    novo_id = len(produtos) + 1
    novo_produto = {
        "id": novo_id,
        "nome": nome,
        "preco": float(preco),
        "quantidade": int(quantidade),
        "categoria": categoria
    }
    produtos.append(novo_produto)
    salvar_produtos(produtos)
    return novo_produto


def listar_produtos():
    return carregar_produtos()


def buscar_produto_por_id(id_produto):
    for p in carregar_produtos():
        if p["id"] == id_produto:
            return p
    return None


def atualizar_produto(id_produto, nome=None, preco=None, quantidade=None, categoria=None):
    produtos = carregar_produtos()
    for p in produtos:
        if p["id"] == id_produto:
            if nome:       p["nome"]       = nome
            if preco:      p["preco"]      = float(preco)
            if quantidade: p["quantidade"] = int(quantidade)
            if categoria:  p["categoria"]  = categoria
            salvar_produtos(produtos)
            return p
    return None


def excluir_produto(id_produto):
    produtos = carregar_produtos()
    lista_nova = []
    encontrou = False
    for p in produtos:
        if p["id"] == id_produto:
            encontrou = True
        else:
            lista_nova.append(p)
    if encontrou:
        salvar_produtos(lista_nova)
    return encontrou
