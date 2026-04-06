import requests
import json

# --- Configuração ---
API_URL = "http://127.0.0.1:8000/aggregate-mcda/"

# --- Cenário: Planejamento Urbano para uma Cidade Inteligente ---

# 1. As Alternativas (Projetos em consideração)
alternatives = [
    "Projeto A: Rede de Ciclovias",
    "Projeto B: Coleta de Lixo Inteligente",
    "Projeto C: Iluminação Pública com LED"
]

# 2. Os Critérios de Avaliação
# Para que os algoritmos MCDA funcionem corretamente, todos os critérios
# devem seguir a mesma lógica: "quanto maior o valor, melhor".
# Portanto, para critérios de CUSTO (onde menor é melhor), nós os transformamos.
# Uma forma simples é usar 1/valor.
#
# Critérios (COLUNAS do dataset):
# - C1: Custo (INVERTIDO) -> [Original: 5M, 2M, 8M] -> [1/5, 1/2, 1/8] = [0.20, 0.50, 0.125]
# - C2: Impacto Ambiental (nota 0-10, maior é melhor) -> [9, 7, 10]
# - C3: Benefício Social (nota 0-10, maior é melhor) -> [8, 6, 7]
# - C4: Tempo de Implementação em meses (INVERTIDO) -> [Original: 24, 6, 18] -> [1/24, 1/6, 1/18] = [0.04, 0.16, 0.05]

dataset_cidade = [
    # C1,   C2,  C3,   C4    (Projeto A: Ciclovias)
    [0.20, 9.0, 8.0, 0.04],
    # C1,   C2,  C3,   C4    (Projeto B: Lixo Inteligente)
    [0.50, 7.0, 6.0, 0.16],
    # C1,   C2,  C3,   C4    (Projeto C: Iluminação LED)
    [0.125, 10.0, 7.0, 0.05]
]

# 3. Os Avaliadores (Secretarias da Prefeitura com diferentes prioridades)

# Avaliador 1: Secretaria de Finanças
# Prioridade máxima em CUSTO e TEMPO.
weights_financas = [
    0.5,  # Peso para Custo
    0.1,  # Peso para Impacto Ambiental
    0.1,  # Peso para Benefício Social
    0.3   # Peso para Tempo de Implementação
]

# Avaliador 2: Secretaria do Meio Ambiente e Social
# Prioridade máxima em IMPACTO AMBIENTAL e BENEFÍCIO SOCIAL.
weights_social_ambiental = [
    0.1,  # Peso para Custo
    0.5,  # Peso para Impacto Ambiental
    0.4,  # Peso para Benefício Social
    0.0   # Peso para Tempo de Implementação
]

# 4. Peso dos Avaliadores na Decisão Final
# O prefeito considera a opinião da Secretaria de Finanças um pouco mais importante.
evaluator_weights = [0.6, 0.4] # 60% para Finanças, 40% para Social/Ambiental

# --- Montagem do Payload para a API ---
payload = {
    "evaluator_results": [
        {
            "evaluator_name": "Secretaria de Finanças",
            "dataset": dataset_cidade,
            "weights": weights_financas
        },
        {
            "evaluator_name": "Secretaria do Meio Ambiente e Social",
            "dataset": dataset_cidade,
            "weights": weights_social_ambiental
        }
    ],
    "evaluator_weights": evaluator_weights,
    "algorithm": "promethee_ii", # Usando PROMETHEE 
    "alternatives": alternatives
}

print("--- TESTE DE CENÁRIO: CIDADE INTELIGENTE ---")
print(f"Enviando requisição para: {API_URL}")

try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status() 

    data = response.json()

    print("\n--- RESPOSTA DA API ---")
    print("Status Code:", response.status_code)
    print("Sucesso:", data.get("success"))

    if data.get("success"):
        print("\n--- RANKING FINAL CONSOLIDADO ---")
        for item in data.get("final_ranking", []):
            print(
                f"  Posição: {item['rank_position']} | "
                f"Alternativa: {item['alternative_name']} | "
                f"Score (Phi): {item['phi_score']:.4f}"
            )

        print("\nTeste de cenário concluído com sucesso!")
        print("\n--- Análise do Resultado ---")
        print("O ranking acima representa a melhor decisão de compromisso,")
        print("considerando as prioridades conflitantes das diferentes secretarias.")
        print("O projeto em 1º lugar é a recomendação do sistema para implementação.")

except requests.exceptions.RequestException as e:
    print(f"\n ERRO: Não foi possível conectar à API. Verifique se o servidor está rodando.")
    print(f"Detalhe do erro: {e}")
except Exception as e:
    print(f"\n FALHA INESPERADA: {e}")
    if 'response' in locals():
      print("Resposta recebida do servidor:", response.text)