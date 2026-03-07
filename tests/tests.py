import requests
import json

API_BASE_URL = "http://127.0.0.1:8000" 

common_alternatives = ["Projeto A", "Projeto B", "Projeto C"]

# Dados para agregação
aggregation_payload_base = {
    "evaluator_results": [
        {
            "evaluator_name": "Técnico",
            "dataset": [[10, 500, 8], [8, 600, 7], [12, 450, 9]],
            "weights": [0.5, 0.3, 0.2]
        },
        {
            "evaluator_name": "Financeiro",
            "dataset": [[11, 480, 7], [9, 550, 8], [10, 500, 8]],
            "weights": [0.2, 0.6, 0.2]
        }
    ],
    "evaluator_weights": [0.6, 0.4],
    "alternatives": common_alternatives
}

def run_test(name, url, payload):
    print(f"--- Rodando Teste: {name} ---")
    try:
        response = requests.post(url, data=json.dumps(payload))
        response.raise_for_status() 
        data = response.json()
        
        print("Status Code:", response.status_code)
        print("Resultado:", data)
        assert data.get("success"), "API retornou falha!"
        
        ranking_key = "ranking" if "ranking" in data else "final_ranking"
        assert ranking_key in data and len(data[ranking_key]) > 0, "Ranking está vazio ou ausente!"
        
        print(f" Teste '{name}' passou com sucesso!\n")
        return True
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO em '{name}': {e}\n")
        return False
    except Exception as e:
        print(f"FALHA no teste '{name}': {e}\n")
        print("Resposta recebida:", response.text)
        return False

def main():
    # Teste 1: Cálculo simples com PROMETHEE II
    payload_simple_promethee = {
        "dataset": [[10, 500, 8], [8, 600, 7], [12, 450, 9]],
        "weights": [0.5, 0.3, 0.2],
        "algorithm": "promethee_ii",
        "alternatives": common_alternatives
    }
    run_test("Cálculo Simples PROMETHEE II", f"{API_BASE_URL}/run-mcda/", payload_simple_promethee)

    # Teste 2: Cálculo simples com ELECTRE II
    payload_simple_electre = {
        "dataset": [[10, 500, 8], [8, 600, 7], [12, 450, 9]],
        "weights": [0.5, 0.3, 0.2],
        "algorithm": "electre_ii",
        "alternatives": common_alternatives
    }
    run_test("Cálculo Simples ELECTRE II", f"{API_BASE_URL}/run-mcda/", payload_simple_electre)

    # Teste 3: Agregação com PROMETHEE II
    payload_agg_promethee = aggregation_payload_base.copy()
    payload_agg_promethee["algorithm"] = "promethee_ii"
    run_test("Agregação PROMETHEE II", f"{API_BASE_URL}/aggregate-mcda/", payload_agg_promethee)
    
    # Teste 4: Agregação com ELECTRE II
    payload_agg_electre = aggregation_payload_base.copy()
    payload_agg_electre["algorithm"] = "electre_ii"
    run_test("Agregação ELECTRE II", f"{API_BASE_URL}/aggregate-mcda/", payload_agg_electre)

if __name__ == "__main__":
    main()