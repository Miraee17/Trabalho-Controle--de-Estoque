# database.py - Módulo responsável pelo armazenamento de dados
import json
import os

ARQUIVO_FORNECEDORES = "fornecedores.json"
ARQUIVO_COMPRAS = "compras.json"


# ──────────────────────────────────────────
# UTILITÁRIOS INTERNOS
# ──────────────────────────────────────────

def _carregar(arquivo):
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def _proximo_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


# ──────────────────────────────────────────
# FORNECEDORES
# ──────────────────────────────────────────

def inserir_fornecedor(nome, documento, contato, telefone, cep, cnpj):
    fornecedores = _carregar(ARQUIVO_FORNECEDORES)
    novo = {
        "id": _proximo_id(fornecedores),
        "nome": nome,
        "documento": documento,
        "contato": contato,
        "telefone": telefone,
        "cep": cep,
        "cnpj": cnpj
    }
    fornecedores.append(novo)
    _salvar(ARQUIVO_FORNECEDORES, fornecedores)
    return novo

def listar_fornecedores():
    return _carregar(ARQUIVO_FORNECEDORES)

def buscar_fornecedor_por_id(id_fornecedor):
    for f in _carregar(ARQUIVO_FORNECEDORES):
        if f["id"] == id_fornecedor:
            return f
    return None

def buscar_fornecedor_por_cnpj(cnpj):
    for f in _carregar(ARQUIVO_FORNECEDORES):
        if f["cnpj"] == cnpj:
            return f
    return None

def atualizar_fornecedor(id_fornecedor, nome=None, documento=None, contato=None,
                         telefone=None, cep=None, cnpj=None):
    fornecedores = _carregar(ARQUIVO_FORNECEDORES)
    for f in fornecedores:
        if f["id"] == id_fornecedor:
            if nome:      f["nome"]      = nome
            if documento: f["documento"] = documento
            if contato:   f["contato"]   = contato
            if telefone:  f["telefone"]  = telefone
            if cep:       f["cep"]       = cep
            if cnpj:      f["cnpj"]      = cnpj
            _salvar(ARQUIVO_FORNECEDORES, fornecedores)
            return f
    return None

def excluir_fornecedor(id_fornecedor):
    fornecedores = _carregar(ARQUIVO_FORNECEDORES)
    nova_lista = [f for f in fornecedores if f["id"] != id_fornecedor]
    if len(nova_lista) == len(fornecedores):
        return False
    _salvar(ARQUIVO_FORNECEDORES, nova_lista)
    return True


# ──────────────────────────────────────────
# COMPRAS
# ──────────────────────────────────────────

def inserir_compra(produto, id_fornecedor, quantidade, data, categoria):
    compras = _carregar(ARQUIVO_COMPRAS)
    nova = {
        "id": _proximo_id(compras),
        "produto": produto,
        "id_fornecedor": id_fornecedor,
        "quantidade": quantidade,
        "data": data,
        "categoria": categoria
    }
    compras.append(nova)
    _salvar(ARQUIVO_COMPRAS, compras)
    return nova

def listar_compras():
    return _carregar(ARQUIVO_COMPRAS)

def buscar_compra_por_id(id_compra):
    for c in _carregar(ARQUIVO_COMPRAS):
        if c["id"] == id_compra:
            return c
    return None

def buscar_compras_por_categoria(categoria):
    return [c for c in _carregar(ARQUIVO_COMPRAS)
            if c["categoria"].lower() == categoria.lower()]

def buscar_compras_por_data(data):
    return [c for c in _carregar(ARQUIVO_COMPRAS) if c["data"] == data]

def atualizar_compra(id_compra, produto=None, quantidade=None, data=None, categoria=None):
    compras = _carregar(ARQUIVO_COMPRAS)
    for c in compras:
        if c["id"] == id_compra:
            if produto:    c["produto"]    = produto
            if quantidade: c["quantidade"] = quantidade
            if data:       c["data"]       = data
            if categoria:  c["categoria"]  = categoria
            _salvar(ARQUIVO_COMPRAS, compras)
            return c
    return None

def excluir_compra(id_compra):
    compras = _carregar(ARQUIVO_COMPRAS)
    nova_lista = [c for c in compras if c["id"] != id_compra]
    if len(nova_lista) == len(compras):
        return False
    _salvar(ARQUIVO_COMPRAS, nova_lista)
    return True