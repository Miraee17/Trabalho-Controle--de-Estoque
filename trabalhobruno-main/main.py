# main.py - Interface gráfica do Sistema de Controle de Estoque
import tkinter as tk
from tkinter import ttk, messagebox
import database

# ── Paleta de cores ──────────────────────────────────────────────────
COR_BG        = "#F0F4F8"   # fundo geral cinza claro
COR_SIDEBAR   = "#1E3A5F"   # azul escuro (barra lateral / cabeçalhos)
COR_ACCENT    = "#2E86AB"   # azul médio (botões principais)
COR_DANGER    = "#C0392B"   # vermelho (excluir)
COR_SUCCESS   = "#27AE60"   # verde (confirmar)
COR_TEXT      = "#1A1A2E"   # texto escuro
COR_LIGHT     = "#FFFFFF"
COR_ROW_ODD   = "#FFFFFF"
COR_ROW_EVEN  = "#E8F0FE"

FONTE_TITULO  = ("Segoe UI", 15, "bold")
FONTE_LABEL   = ("Segoe UI", 10)
FONTE_LABEL_B = ("Segoe UI", 10, "bold")
FONTE_BTN     = ("Segoe UI", 10, "bold")
FONTE_TABELA  = ("Segoe UI", 9)

# ── Utilitário: botão padrão ──────────────────────────────────────────
def btn(parent, texto, comando, cor=COR_ACCENT, fg=COR_LIGHT, **kw):
    b = tk.Button(parent, text=texto, command=comando,
                  bg=cor, fg=fg, font=FONTE_BTN,
                  relief="flat", cursor="hand2",
                  padx=14, pady=6, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=_escurecer(cor)))
    b.bind("<Leave>", lambda e: b.config(bg=cor))
    return b

def _escurecer(hex_cor):
    r, g, b_ = int(hex_cor[1:3],16), int(hex_cor[3:5],16), int(hex_cor[5:7],16)
    r, g, b_ = max(0,r-25), max(0,g-25), max(0,b_-25)
    return f"#{r:02x}{g:02x}{b_:02x}"

# ── Utilitário: tabela com scroll ─────────────────────────────────────
def criar_tabela(parent, colunas, larguras):
    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True, padx=10, pady=6)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Est.Treeview",
                    background=COR_ROW_ODD, fieldbackground=COR_ROW_ODD,
                    rowheight=26, font=FONTE_TABELA)
    style.configure("Est.Treeview.Heading",
                    background=COR_SIDEBAR, foreground=COR_LIGHT,
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Est.Treeview", background=[("selected", COR_ACCENT)])

    tree = ttk.Treeview(frame, columns=colunas, show="headings",
                        style="Est.Treeview", selectmode="browse")
    for col, larg in zip(colunas, larguras):
        tree.heading(col, text=col)
        tree.column(col, width=larg, anchor="center")
    tree.tag_configure("par",   background=COR_ROW_EVEN)
    tree.tag_configure("impar", background=COR_ROW_ODD)

    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tree

def preencher_tabela(tree, linhas):
    tree.delete(*tree.get_children())
    for i, linha in enumerate(linhas):
        tag = "par" if i % 2 == 0 else "impar"
        tree.insert("", "end", values=linha, tags=(tag,))

# ── Utilitário: formulário em dialog ─────────────────────────────────
def abrir_form(parent, titulo, campos, dados_iniciais=None):
    """
    Abre uma janela modal com os campos listados.
    Retorna dict {campo: valor} ou None se cancelado.
    """
    resultado = {}
    dlg = tk.Toplevel(parent)
    dlg.title(titulo)
    dlg.configure(bg=COR_BG)
    dlg.resizable(False, False)
    dlg.grab_set()

    # Cabeçalho
    tk.Label(dlg, text=titulo, font=FONTE_TITULO,
             bg=COR_SIDEBAR, fg=COR_LIGHT,
             padx=20, pady=10).pack(fill="x")

    corpo = tk.Frame(dlg, bg=COR_BG, padx=24, pady=16)
    corpo.pack(fill="both")

    entradas = {}
    for i, campo in enumerate(campos):
        tk.Label(corpo, text=campo, font=FONTE_LABEL_B,
                 bg=COR_BG, fg=COR_TEXT, anchor="w").grid(
                     row=i, column=0, sticky="w", pady=4)
        e = tk.Entry(corpo, font=FONTE_LABEL, width=30,
                     relief="solid", bd=1)
        if dados_iniciais and campo in dados_iniciais:
            e.insert(0, dados_iniciais[campo])
        e.grid(row=i, column=1, padx=(10,0), pady=4)
        entradas[campo] = e

    def confirmar():
        for campo, entry in entradas.items():
            resultado[campo] = entry.get().strip()
        dlg.destroy()

    def cancelar():
        dlg.destroy()

    rodape = tk.Frame(dlg, bg=COR_BG, pady=10)
    rodape.pack()
    btn(rodape, "Salvar", confirmar, cor=COR_SUCCESS).pack(side="left", padx=6)
    btn(rodape, "Cancelar", cancelar, cor=COR_DANGER).pack(side="left", padx=6)

    parent.wait_window(dlg)
    return resultado if resultado else None


# ════════════════════════════════════════════════════════════════════
# ABA FORNECEDORES
# ════════════════════════════════════════════════════════════════════
def aba_fornecedores(notebook):
    frame = tk.Frame(notebook, bg=COR_BG)

    # Cabeçalho
    tk.Label(frame, text="Fornecedores", font=FONTE_TITULO,
             bg=COR_SIDEBAR, fg=COR_LIGHT, padx=16, pady=10).pack(fill="x")

    # Barra de busca
    busca_frame = tk.Frame(frame, bg=COR_BG, pady=8)
    busca_frame.pack(fill="x", padx=10)
    tk.Label(busca_frame, text="Buscar por nome:", font=FONTE_LABEL,
             bg=COR_BG).pack(side="left")
    busca_var = tk.StringVar()
    tk.Entry(busca_frame, textvariable=busca_var, font=FONTE_LABEL,
             width=24, relief="solid", bd=1).pack(side="left", padx=6)
    btn(busca_frame, "Buscar", lambda: atualizar_tabela(), cor=COR_ACCENT).pack(side="left")
    btn(busca_frame, "Limpar", lambda: (busca_var.set(""), atualizar_tabela()),
        cor="#7F8C8D").pack(side="left", padx=4)

    # Tabela
    cols = ["ID", "Nome", "Documento", "Contato", "Telefone", "CEP", "CNPJ"]
    larg = [40, 160, 110, 110, 110, 90, 140]
    tree = criar_tabela(frame, cols, larg)

    # Botões de ação
    acoes = tk.Frame(frame, bg=COR_BG, pady=8)
    acoes.pack()

    CAMPOS_FORN = ["Nome", "Documento", "Contato", "Telefone", "CEP", "CNPJ"]

    def atualizar_tabela():
        todos = database.listar_fornecedores()
        filtro = busca_var.get().lower()
        if filtro:
            todos = [f for f in todos if filtro in f["nome"].lower()]
        linhas = [(f["id"], f["nome"], f["documento"], f["contato"],
                   f["telefone"], f["cep"], f["cnpj"]) for f in todos]
        preencher_tabela(tree, linhas)

    def cadastrar():
        dados = abrir_form(frame, "Cadastrar Fornecedor", CAMPOS_FORN)
        if not dados or not dados.get("Nome"):
            return
        database.inserir_fornecedor(
            dados["Nome"], dados["Documento"], dados["Contato"],
            dados["Telefone"], dados["CEP"], dados["CNPJ"])
        messagebox.showinfo("Sucesso", "Fornecedor cadastrado!")
        atualizar_tabela()

    def editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um fornecedor.")
            return
        id_ = int(tree.item(sel[0])["values"][0])
        f = database.buscar_fornecedor_por_id(id_)
        iniciais = {"Nome": f["nome"], "Documento": f["documento"],
                    "Contato": f["contato"], "Telefone": f["telefone"],
                    "CEP": f["cep"], "CNPJ": f["cnpj"]}
        dados = abrir_form(frame, "Editar Fornecedor", CAMPOS_FORN, iniciais)
        if not dados:
            return
        database.atualizar_fornecedor(id_, dados["Nome"], dados["Documento"],
            dados["Contato"], dados["Telefone"], dados["CEP"], dados["CNPJ"])
        messagebox.showinfo("Sucesso", "Fornecedor atualizado!")
        atualizar_tabela()

    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um fornecedor.")
            return
        id_ = int(tree.item(sel[0])["values"][0])
        nome = tree.item(sel[0])["values"][1]
        if messagebox.askyesno("Confirmar", f"Excluir fornecedor '{nome}'?"):
            database.excluir_fornecedor(id_)
            atualizar_tabela()

    btn(acoes, "+ Cadastrar", cadastrar, cor=COR_SUCCESS).pack(side="left", padx=5)
    btn(acoes, "✎ Editar",   editar,    cor=COR_ACCENT).pack(side="left", padx=5)
    btn(acoes, "✕ Excluir",  excluir,   cor=COR_DANGER).pack(side="left", padx=5)
    btn(acoes, "↺ Atualizar", atualizar_tabela, cor="#7F8C8D").pack(side="left", padx=5)

    atualizar_tabela()
    return frame


# ════════════════════════════════════════════════════════════════════
# ABA COMPRAS
# ════════════════════════════════════════════════════════════════════
def aba_compras(notebook):
    frame = tk.Frame(notebook, bg=COR_BG)

    tk.Label(frame, text="Compras / Produtos", font=FONTE_TITULO,
             bg=COR_SIDEBAR, fg=COR_LIGHT, padx=16, pady=10).pack(fill="x")

    cols = ["ID", "Produto", "Fornecedor", "Quantidade", "Data", "Categoria"]
    larg = [40, 160, 150, 90, 100, 120]
    tree = criar_tabela(frame, cols, larg)

    acoes = tk.Frame(frame, bg=COR_BG, pady=8)
    acoes.pack()

    CAMPOS_COMPRA = ["Produto", "ID Fornecedor", "Quantidade",
                     "Data (DD/MM/AAAA)", "Categoria"]

    def nome_forn(id_):
        f = database.buscar_fornecedor_por_id(id_)
        return f["nome"] if f else f"ID {id_}"

    def atualizar_tabela():
        compras = database.listar_compras()
        linhas = [(c["id"], c["produto"], nome_forn(c["id_fornecedor"]),
                   c["quantidade"], c["data"], c["categoria"]) for c in compras]
        preencher_tabela(tree, linhas)

    def registrar():
        dados = abrir_form(frame, "Registrar Compra", CAMPOS_COMPRA)
        if not dados or not dados.get("Produto"):
            return
        try:
            id_f = int(dados["ID Fornecedor"])
            qtd  = int(dados["Quantidade"])
        except ValueError:
            messagebox.showerror("Erro", "ID Fornecedor e Quantidade devem ser números.")
            return
        database.inserir_compra(dados["Produto"], id_f, qtd,
                                dados["Data (DD/MM/AAAA)"], dados["Categoria"])
        messagebox.showinfo("Sucesso", "Compra registrada!")
        atualizar_tabela()

    def editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma compra.")
            return
        id_ = int(tree.item(sel[0])["values"][0])
        c = database.buscar_compra_por_id(id_)
        iniciais = {"Produto": c["produto"], "ID Fornecedor": str(c["id_fornecedor"]),
                    "Quantidade": str(c["quantidade"]),
                    "Data (DD/MM/AAAA)": c["data"], "Categoria": c["categoria"]}
        dados = abrir_form(frame, "Editar Compra", CAMPOS_COMPRA, iniciais)
        if not dados:
            return
        try:
            qtd = int(dados["Quantidade"]) if dados["Quantidade"] else None
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número.")
            return
        database.atualizar_compra(id_, dados["Produto"], qtd,
                                  dados["Data (DD/MM/AAAA)"], dados["Categoria"])
        messagebox.showinfo("Sucesso", "Compra atualizada!")
        atualizar_tabela()

    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma compra.")
            return
        id_ = int(tree.item(sel[0])["values"][0])
        produto = tree.item(sel[0])["values"][1]
        if messagebox.askyesno("Confirmar", f"Excluir compra '{produto}'?"):
            database.excluir_compra(id_)
            atualizar_tabela()

    btn(acoes, "+ Registrar", registrar, cor=COR_SUCCESS).pack(side="left", padx=5)
    btn(acoes, "✎ Editar",   editar,    cor=COR_ACCENT).pack(side="left", padx=5)
    btn(acoes, "✕ Excluir",  excluir,   cor=COR_DANGER).pack(side="left", padx=5)
    btn(acoes, "↺ Atualizar", atualizar_tabela, cor="#7F8C8D").pack(side="left", padx=5)

    atualizar_tabela()
    return frame


# ════════════════════════════════════════════════════════════════════
# ABA RELATÓRIOS
# ════════════════════════════════════════════════════════════════════
def aba_relatorios(notebook):
    frame = tk.Frame(notebook, bg=COR_BG)

    tk.Label(frame, text="Relatórios e Pesquisa", font=FONTE_TITULO,
             bg=COR_SIDEBAR, fg=COR_LIGHT, padx=16, pady=10).pack(fill="x")

    # Filtros
    filtro_frame = tk.LabelFrame(frame, text="  Filtrar compras  ",
                                  bg=COR_BG, fg=COR_TEXT,
                                  font=FONTE_LABEL_B, padx=12, pady=8)
    filtro_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(filtro_frame, text="Categoria:", font=FONTE_LABEL,
             bg=COR_BG).grid(row=0, column=0, padx=(0,4))
    cat_var = tk.StringVar()
    tk.Entry(filtro_frame, textvariable=cat_var, font=FONTE_LABEL,
             width=18, relief="solid", bd=1).grid(row=0, column=1, padx=4)

    tk.Label(filtro_frame, text="Data (DD/MM/AAAA):", font=FONTE_LABEL,
             bg=COR_BG).grid(row=0, column=2, padx=(16,4))
    data_var = tk.StringVar()
    tk.Entry(filtro_frame, textvariable=data_var, font=FONTE_LABEL,
             width=14, relief="solid", bd=1).grid(row=0, column=3, padx=4)

    cols = ["ID", "Produto", "Fornecedor", "Quantidade", "Data", "Categoria"]
    larg = [40, 160, 150, 90, 100, 120]
    tree = criar_tabela(frame, cols, larg)

    # Rodapé com totalizadores
    rodape = tk.Frame(frame, bg=COR_SIDEBAR, pady=6)
    rodape.pack(fill="x", side="bottom")
    total_lbl  = tk.Label(rodape, text="Registros: 0", font=FONTE_LABEL_B,
                           bg=COR_SIDEBAR, fg=COR_LIGHT)
    total_lbl.pack(side="left", padx=16)
    itens_lbl  = tk.Label(rodape, text="Total de itens: 0", font=FONTE_LABEL_B,
                           bg=COR_SIDEBAR, fg=COR_LIGHT)
    itens_lbl.pack(side="left", padx=16)

    def nome_forn(id_):
        f = database.buscar_fornecedor_por_id(id_)
        return f["nome"] if f else f"ID {id_}"

    def pesquisar():
        cat  = cat_var.get().strip()
        data = data_var.get().strip()
        compras = database.listar_compras()
        if cat:
            compras = [c for c in compras if c["categoria"].lower() == cat.lower()]
        if data:
            compras = [c for c in compras if c["data"] == data]
        linhas = [(c["id"], c["produto"], nome_forn(c["id_fornecedor"]),
                   c["quantidade"], c["data"], c["categoria"]) for c in compras]
        preencher_tabela(tree, linhas)
        total_lbl.config(text=f"Registros: {len(compras)}")
        itens_lbl.config(text=f"Total de itens: {sum(c['quantidade'] for c in compras)}")

    def limpar():
        cat_var.set("")
        data_var.set("")
        pesquisar()

    btn(filtro_frame, "Pesquisar", pesquisar, cor=COR_ACCENT).grid(
        row=0, column=4, padx=(16,4))
    btn(filtro_frame, "Mostrar todos", limpar, cor="#7F8C8D").grid(
        row=0, column=5, padx=4)

    pesquisar()
    return frame


# ════════════════════════════════════════════════════════════════════
# JANELA PRINCIPAL
# ════════════════════════════════════════════════════════════════════
def executar_sistema():
    root = tk.Tk()
    root.title("Sistema de Controle de Estoque 2026")
    root.geometry("860x560")
    root.minsize(760, 480)
    root.configure(bg=COR_BG)

    # Topo
    topo = tk.Frame(root, bg=COR_SIDEBAR, pady=12)
    topo.pack(fill="x")
    tk.Label(topo, text="📦  Sistema de Controle de Estoque",
             font=("Segoe UI", 14, "bold"),
             bg=COR_SIDEBAR, fg=COR_LIGHT).pack(side="left", padx=20)
    tk.Label(topo, text="2026", font=("Segoe UI", 11),
             bg=COR_SIDEBAR, fg="#7FB3D3").pack(side="right", padx=20)

    # Abas
    style = ttk.Style()
    style.configure("TNotebook", background=COR_BG, borderwidth=0)
    style.configure("TNotebook.Tab", font=FONTE_LABEL_B,
                    padding=[16, 8], background="#D0D8E4", foreground=COR_TEXT)
    style.map("TNotebook.Tab",
              background=[("selected", COR_ACCENT)],
              foreground=[("selected", COR_LIGHT)])

    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    notebook.add(aba_fornecedores(notebook), text="  🏭  Fornecedores  ")
    notebook.add(aba_compras(notebook),      text="  🛒  Compras  ")
    notebook.add(aba_relatorios(notebook),   text="  📊  Relatórios  ")

    root.mainloop()

if __name__ == "__main__":
    executar_sistema()