# 📊 Dashboard de Salários na Área de Dados

 Este projeto foi desenvolvido durante a **Imersão de Análise de Dados com Python** promovida pela Alura em agosto de 2025.
 O objetivo é explorar dados salariais na área de tecnologia, utilizando Python, Streamlit e Plotly para criar um dashboard interativo e personalizável.

 ---

## 🚀 Funcionalidades

 - Upload de arquivo CSV com estrutura esperada
 - Filtros interativos por ano, senioridade, tipo de contrato e tamanho da empresa
 - Visualização de métricas salariais (média, mediana, máximo, cargo mais frequente)
 - Gráficos interativos com Plotly (barras, histogramas, boxplots, mapas)
 - Exportação dos dados filtrados em formato `.xlsx`

 ---

 ## 🧰 Tecnologias utilizadas

 - Python 3.10+
 - Streamlit
 - Pandas
 - Plotly
 - OpenPyXL

 ---

 ## ⚙️ Como executar o projeto

 ### 1. Clone o repositório:

     git clone https://github.com/gitJotaStudy/imersao-dados-python.git
     cd imersao-dados-python

 ### 2. Crie e ative o ambiente virtual:

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
     
### 3. Instale as dependências:
   
```bash
pip install -r requirements.txt
pip install openpyxl
```

### 4. Execute o projeto com Streamlit:

```bash
streamlit run app.py
```

### 5. Acesse o dashboard:
```bash
http://localhost:8501
```

---

## 📁 Estrutura esperada do arquivo CSV

O dashboard espera um arquivo `.csv` com as seguintes colunas:

     ano,senioridade,contrato,cargo,salario,moeda,usd,residencia,remoto,empresa,tamanho_empresa,residencia_iso3
     2025,senior,integral,Solutions Engineer,214000,USD,214000,US,remoto,US,media,USA

 Você pode fazer upload do arquivo diretamente pela barra lateral do dashboard.

 ---

## 📌 Observações

- O limite de upload é de 200MB por arquivo (definido pelo Streamlit)
- O dashboard foi desenvolvido com foco em aprendizado e boas práticas de visualização de dados
- Sinta-se à vontade para adaptar o projeto para outras áreas ou conjuntos de dados

---

## 🤝 Contribuições

Contribuições são bem-vindas!
Se quiser sugerir melhorias, abrir issues ou enviar pull requests, fique à vontade.

---

## 📄 Licença

Este projeto é de uso educacional e está sob a licença MIT.
Consulte o arquivo LICENSE para mais detalhes.

---

## ✨ Créditos


Projeto desenvolvido durante a Imersão de Análise de Dados com Python da Alura, agosto de 2025.

