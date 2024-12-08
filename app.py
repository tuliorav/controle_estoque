import pyodbc
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import csv

server = 'DESKTOP-9GO7DHV'
database = 'estoque_db'
username = 'sa'
password = 'admin123'

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

def validar_dados(nome, quantidade, preco):
    if not nome or not quantidade or not preco:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    if not quantidade.isdigit() or int(quantidade) <= 0:
        messagebox.showerror("Erro", "A quantidade deve ser um número positivo.")
        return False
    try:
        float(preco)
    except ValueError:
        messagebox.showerror("Erro", "O preço deve ser um valor numérico.")
        return False
    return True

def adicionar_produto():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    preco = entry_preco.get()
    
    if validar_dados(nome, quantidade, preco):
        cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        listar_produtos()
        limpar_campos()

def listar_produtos():
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM produtos")
    for row in cursor.fetchall():
        produto_id = row[0]
        nome = row[1]
        quantidade = row[2]
        preco = f"{row[3]:.2f}"
        
        tree.insert("", "end", values=(produto_id, nome, quantidade, preco))

def editar_produto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um produto para editar.")
        return
    
    item = tree.item(selected_item)
    produto_id = int(item['values'][0])
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    preco = entry_preco.get()
    
    if validar_dados(nome, quantidade, preco):
        cursor.execute("""
        UPDATE produtos
        SET nome = ?, quantidade = ?, preco = ?
        WHERE id = ?
        """, (nome, quantidade, preco, produto_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
        listar_produtos()
        limpar_campos()

def excluir_produto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um produto para excluir.")
        return
    
    item = tree.item(selected_item)
    produto_id = item['values'][0]
    
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
    listar_produtos()

def pesquisar_produtos():
    search_term = entry_pesquisa.get().lower()
    
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM produtos")
    for row in cursor.fetchall():
        if search_term in row[1].lower():
            preco = f"{row[3]:.2f}"
            tree.insert("", "end", values=(row[0], row[1], row[2], preco))

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_pesquisa.delete(0, tk.END)

def exportar_para_csv():
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            cursor.execute("SELECT * FROM produtos")
            rows = cursor.fetchall()
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nome", "Quantidade", "Preço"])  # Cabeçalhos
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("Sucesso", f"Dados exportados para '{filename}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao exportar: {e}")

def importar_de_csv():
    try:
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
                                   (row["Nome"], row["Quantidade"], row["Preço"]))
            conn.commit()
            listar_produtos()
            messagebox.showinfo("Sucesso", f"Dados importados de '{filename}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao importar: {e}")

def gerar_relatorio():
    cursor.execute("SELECT COUNT(*), SUM(quantidade), SUM(quantidade * preco) FROM produtos")
    total_produtos, total_quantidade, valor_total = cursor.fetchone()
    relatorio = (
        f"Total de Produtos: {total_produtos}\n"
        f"Quantidade Total em Estoque: {total_quantidade}\n"
        f"Valor Total do Estoque: R$ {valor_total:.2f}"
    )
    messagebox.showinfo("Relatório de Estoque", relatorio)

root = tk.Tk()
root.title("Sistema de Controle de Estoque")

label_nome = tk.Label(root, text="Nome do Produto")
label_nome.pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

label_quantidade = tk.Label(root, text="Quantidade")
label_quantidade.pack()
entry_quantidade = tk.Entry(root)
entry_quantidade.pack()

label_preco = tk.Label(root, text="Preço")
label_preco.pack()
entry_preco = tk.Entry(root)
entry_preco.pack()

label_pesquisa = tk.Label(root, text="Pesquisar Produto")
label_pesquisa.pack()
entry_pesquisa = tk.Entry(root)
entry_pesquisa.pack()

button_adicionar = tk.Button(root, text="Adicionar Produto", command=adicionar_produto)
button_adicionar.pack()

button_editar = tk.Button(root, text="Editar Produto", command=editar_produto)
button_editar.pack()

button_excluir = tk.Button(root, text="Excluir Produto", command=excluir_produto)
button_excluir.pack()

button_pesquisar = tk.Button(root, text="Pesquisar Produto", command=pesquisar_produtos)
button_pesquisar.pack()

button_limpar = tk.Button(root, text="Limpar Campos", command=limpar_campos)
button_limpar.pack()

button_exportar = tk.Button(root, text="Exportar para CSV", command=exportar_para_csv)
button_exportar.pack()

button_importar = tk.Button(root, text="Importar de CSV", command=importar_de_csv)
button_importar.pack()

button_relatorio = tk.Button(root, text="Gerar Relatório", command=gerar_relatorio)
button_relatorio.pack()

tree = ttk.Treeview(root, columns=("ID", "Nome", "Quantidade", "Preço"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Preço", text="Preço")

tree.column("ID", anchor="center", width=100)
tree.column("Nome", anchor="center", width=200)
tree.column("Quantidade", anchor="center", width=150)
tree.column("Preço", anchor="center", width=150)

tree.pack()

listar_produtos()

root.mainloop()

conn.close()