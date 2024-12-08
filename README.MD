# Sistema de Controle de Estoque
Este é um sistema simples de controle de estoque desenvolvido com Python e Tkinter para a interface gráfica, utilizando o SQL Server como banco de dados. O sistema permite gerenciar produtos, incluindo funcionalidades de cadastro, edição, exclusão, pesquisa, exportação e importação de dados em formato CSV, além de gerar relatórios resumidos do estoque.

# Funcionalidades
- Cadastro de Produtos: Adicione novos produtos com nome, quantidade e preço.
- Listagem de Produtos: Exiba todos os produtos cadastrados no banco de dados em uma tabela.
- Edição de Produtos: Atualize as informações de produtos existentes.
- Exclusão de Produtos: Remova produtos do estoque.
- Pesquisa de Produtos: Pesquise produtos pelo nome.
- Exportação de Dados: Exporte os dados do estoque para um arquivo .csv.
- Importação de Dados: Importe produtos de um arquivo .csv para o sistema.
- Relatório de Estoque: Gere um resumo do estoque com:
- Total de produtos cadastrados.
- Quantidade total em estoque.
- Valor total do estoque (em reais).
# Pré-requisitos
- Python 3.x
- SQL Server configurado e em execução.
- Bibliotecas Python necessárias:
  - pyodbc
  - tkinter
  - csv
# Para instalar a biblioteca pyodbc, execute:

pip install pyodbc
# Configuração
## Configurar o Banco de Dados:

- Crie um banco de dados no SQL Server chamado estoque_db (ou qualquer nome que desejar).
- Crie a tabela produtos com o seguinte comando:

- CREATE TABLE produtos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nome NVARCHAR(100),
    quantidade INT,
    preco FLOAT
);
## Configurar o Código:

- Atualize as credenciais de conexão no código:
server = 'SEU_SERVIDOR'  
database = 'estoque_db'  
username = 'SEU_USUARIO'  
password = 'SUA_SENHA'  
- Como Usar
  - Execute o programa:
    - python app.py
- Use a interface gráfica para realizar as operações:
- Preencha os campos de Nome, Quantidade e Preço para adicionar um novo produto.
- Use os botões para realizar operações como adicionar, editar, excluir e pesquisar produtos.
- Exporte ou importe os dados do estoque usando os botões correspondentes.
- Gere um relatório com informações resumidas do estoque.
- Estrutura do Projeto
sistema-controle-estoque/  
├── app.py              # Código principal do sistema  
├── estoque.csv         # Arquivo CSV usado para importação/exportação (opcional)  
└── README.md           # Documentação do projeto