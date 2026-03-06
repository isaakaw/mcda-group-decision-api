<p align="right">
  <a href="README.md">🇺🇸 English</a> | 
  <a href="README-pt.md">🇧🇷 Português</a>
</p>

# MCDA Decision API

RESTful API for **Multi-Criteria Decision Analysis (MCDA)** with support for **PROMETHEE II** and **ELECTRE II**, including **multi-evaluator aggregation** for group decision support.

This project implements a **Decision-as-a-Service** model, allowing external systems to perform multi-criteria analysis through HTTP requests.

---

## 📌 Motivation

Real-world decision-making often involves multiple conflicting criteria, such as:

- Cost
- Environmental impact
- Social benefit
- Execution time

**Multi-Criteria Decision Analysis (MCDA)** methods help in this process, but many existing tools:

- Are complex
- Don't support multiple evaluators
- Aren't easily integrated into modern systems

This project proposes a **RESTful API** that automates the execution of MCDA methods and allows **aggregating preferences from multiple decision-makers**.

---

## 🧠 Implemented Methods

### PROMETHEE II

The **PROMETHEE II (Preference Ranking Organization Method for Enrichment Evaluation)** method is an outranking method that generates a **complete ranking of alternatives**.

It calculates:

- Positive flow (ϕ⁺)
- Negative flow (ϕ⁻)
- Net flow (ϕ)

The final ranking is obtained by ordering alternatives by their net flow.

---

### ELECTRE II

The **ELECTRE II (ELimination Et Choix Traduisant la REalité)** method uses outranking relations to compare alternatives.

It uses:

- Concordance index
- Discordance index
- Outranking graphs

The result is a **ranking based on strong and weak preference relations**.

---

## 👥 Group Decision Aggregation

The main differentiator of this API is the **multi-evaluator aggregation** model.

The process occurs in two stages:

### Stage 1 – Individual Evaluation

Each evaluator runs an MCDA method separately on their assessments.

ranking_j = MCDA(dataset_j, weights_j)

### Stage 2 – Collective Aggregation

Individual scores are organized into a new decision matrix:

Alternatives × Evaluators

The MCDA method is run again using **evaluator weights**, producing a **consolidated final ranking**.

---

## 🏗 Architecture

The application follows the:

**Decision-as-a-Service** model

Decision logic is exposed via REST API and can be consumed by:

- Web applications
- Mobile apps
- Analysis scripts
- Decision support systems

---

## 📡 Endpoints

### 1️⃣ Individual execution

`POST /run-mcda`

Executes an MCDA method for a single evaluator.

**Input:**
```
{
  "dataset": [[...]],
  "weights": [...],
  "method": "promethee"
}
```

### 2️⃣ Group decision

`POST /aggregate-mcda`

Executes aggregation of multiple evaluators.

**Input:**
```
{
  "evaluations": [...],
  "evaluator_weights": [...],
  "method": "electre"
}
```

---

## ⚙️ Technologies Used

- Python 3
- FastAPI
- NumPy
- pyDecision
- Pydantic
- Uvicorn

---

## 🚀 How to Run

### 1️⃣ Clone the project

```sh
git clone https://github.com/yourusername/mcda-api

cd mcda-api
```

### 2️⃣ Create virtual environment

```sh
python -m venv venv
```

### 3️⃣ Activate environment
```sh
Windows:

venv\Scripts\activate

Linux / Mac:

source venv/bin/activate
```

### 4️⃣ Install dependencies
```sh
pip install -r requirements.txt
```
### 5️⃣ Run the API

```sh
cd app

uvicorn app.main:app --reload

Access the interactive documentation at: http://localhost:8000/docs
```

---

## 📚 Applications

The API can be used in various scenarios:

- Project selection
- Investment prioritization
- Urban planning
- Supplier selection
- Public policy decision support

---

## 🔬 Scientific Basis

This project was developed in the research context of **Group Multi-Criteria Decision Analysis**.

It integrates classic methods from the Outranking family:

- PROMETHEE II
- ELECTRE II

with a modern architecture based on RESTful microservices.

---

## 📄 License

MIT License

---

## 📬 Contact

For questions, suggestions or contributions, please get in touch or open an issue in the repository.


**Developed with 💙 to support more structured and transparent decision-making.**
