<p align="right">
  <a href="README.md">🇺🇸 English</a> | 
  <a href="README-pt.md">🇧🇷 Português</a>
</p>

# MCDA Decision API

API RESTful para **Análise de Decisão Multicritério (MCDA)** com suporte a **PROMETHEE II** e **ELECTRE II**, incluindo **agregação de múltiplos avaliadores** para apoio à decisão em grupo.

Este projeto implementa um modelo de **Decision-as-a-Service**, permitindo que sistemas externos realizem análises multicritério por meio de requisições HTTP.

---

## 📌 Motivação

A tomada de decisão em contextos reais frequentemente envolve múltiplos critérios conflitantes, como:

- Custo
- Impacto ambiental
- Benefício social
- Tempo de execução

Métodos de **Multi-Criteria Decision Analysis (MCDA)** auxiliam nesse processo, porém muitas ferramentas existentes:

- São complexas
- Não suportam múltiplos avaliadores
- Não são facilmente integráveis em sistemas modernos

Este projeto propõe uma **API RESTful** que automatiza a execução de métodos MCDA e permite **agregar preferências de múltiplos decisores**.

---

## 🧠 Métodos Implementados

### PROMETHEE II

O método **PROMETHEE II (Preference Ranking Organization Method for Enrichment Evaluation)** é um método de superação (outranking) que gera um **ranking completo das alternativas**.

Ele calcula:

- Fluxo positivo (ϕ⁺)
- Fluxo negativo (ϕ⁻)
- Fluxo líquido (ϕ)

O ranking final é obtido ordenando as alternativas pelo fluxo líquido.

---

### ELECTRE II

O método **ELECTRE II (ELimination Et Choix Traduisant la REalité)** utiliza relações de sobreclassificação para comparar alternativas.

Ele utiliza:

- Índice de concordância
- Índice de discordância
- Grafos de sobreclassificação

O resultado é um **ranking baseado em relações fortes e fracas de preferência**.

---

## 👥 Agregação de Decisão em Grupo

O principal diferencial desta API é o modelo de **agregação de múltiplos avaliadores**.

O processo ocorre em duas etapas:

### Etapa 1 – Avaliação Individual

Cada avaliador executa um método MCDA separadamente sobre suas avaliações.

ranking_j = MCDA(dataset_j, weights_j)

### Etapa 2 – Agregação Coletiva

Os scores individuais são organizados em uma nova matriz de decisão:

Alternativas × Avaliadores

O método MCDA é executado novamente utilizando **pesos dos avaliadores**, produzindo um **ranking final consolidado**.

---

## 🏗 Arquitetura

A aplicação segue o modelo:

**Decision-as-a-Service**

A lógica de decisão é exposta via API REST e pode ser consumida por:

- Aplicações web
- Aplicativos móveis
- Scripts de análise
- Sistemas de apoio à decisão

---

## 📡 Endpoints

### 1️⃣ Execução individual

`POST /run-mcda`

Executa um método MCDA para um único avaliador.

**Entrada:**
```
{
  "dataset": [[...]],
  "weights": [...],
  "method": "promethee"
}
```

### 2️⃣ Decisão em grupo

`POST /aggregate-mcda`

Executa agregação de múltiplos avaliadores.

**Entrada:**
```
{
  "evaluations": [...],
  "evaluator_weights": [...],
  "method": "electre"
}
```

---

## ⚙️ Tecnologias Utilizadas

- Python 3
- FastAPI
- NumPy
- pyDecision
- Pydantic
- Uvicorn

---

## 🚀 Como executar

### 1️⃣ Clonar o projeto

```sh
git clone https://github.com/seuusuario/mcda-api

cd mcda-api
```

### 2️⃣ Criar ambiente virtual
```sh
python -m venv venv
```

### 3️⃣ Ativar ambiente

Windows
```sh
venv\Scripts\activate
```
Linux / Mac
```sh
source venv/bin/activate
```

### 4️⃣ Instalar dependências

```sh
pip install -r requirements.txt
```

### 5️⃣ Rodar a API

```sh
cd app 

uvicorn app.main:app --reload
```
Depois acesse:
```sh
 http://localhost:8000/docs
```
Para visualizar a **documentação interativa da API**

---
### 6️⃣ Executar testes ou exemplos
Abra outro terminal e ative o ambiente virtual novamente.

Executar testes:
```sh 
cd tests 
python run tests.py
```
Executar exemplos:
```sh 
cd Examples
python run example.py
```


---

## 📚 Aplicações

A API pode ser utilizada em diversos cenários:

- Seleção de projetos
- Priorização de investimentos
- Planejamento urbano
- Seleção de fornecedores
- Apoio à decisão em políticas públicas

---

## 🔬 Base Científica

Este projeto foi desenvolvido no contexto de pesquisa sobre **Análise de Decisão Multicritério em Grupo**.

Ele integra métodos clássicos da família Outranking:

- PROMETHEE II
- ELECTRE II

com uma arquitetura moderna baseada em microserviços RESTful.

---

## 📄 Licença

MIT License

---

## 📬 Contato

Para dúvidas, sugestões ou contribuições, entre em contato ou abra uma issue no repositório.


**Desenvolvido com 💙 para apoiar tomadas de decisão mais estruturadas e transparentes.**

