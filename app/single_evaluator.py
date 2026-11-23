import numpy as np
from pyDecision.algorithm import electre_ii, promethee_ii
from typing import List, Dict, Any, Tuple, Optional
import traceback

def calculate_dynamic_promethee_params(dataset: np.ndarray):
    Q, P, S, F = [], [], [], []
    for j in range(dataset.shape[1]):
        col = dataset[:, j]
        col_range = np.ptp(col) if len(np.unique(col)) > 1 else 1.0
        q = 0.1 * col_range
        p = max(0.3 * col_range, q)
        Q.append(float(q)); P.append(float(p)); S.append(0.0); F.append("t5")
    return Q, P, S, F

#Por enquanto deixei de lado esses cáculos pra posteriormente fazer mais testes com ele
def calculate_dynamic_electre_params(dataset: np.ndarray) -> Dict[str, float]:
    std_devs = [np.std(dataset[:, j]) for j in range(dataset.shape[1])]
    valid = [s for s in std_devs if s > 0]
    avg_std = np.mean(valid) if valid else 0.0
    epsilon = 1e-6
    if avg_std < epsilon:
        avg_std = epsilon
    return {
        "c_minus": 0.1 * avg_std, "c_zero": 0.1 * avg_std, "c_plus": 0.3 * avg_std,
        "d_minus": 0.2 * avg_std, "d_plus": 0.3 * avg_std
    }

def run_mcda_calculation(
    algorithm: str,
    dataset: np.ndarray,
    weights: List[float],
    alternative_names_ordered: List[str],
    return_internal_scores: bool = False
) -> Tuple[Any, Optional[str]]:

    if len(alternative_names_ordered) != dataset.shape[0]:
        return [], "Número de alternativas não bate com o dataset."

    weights_np = np.array(weights)

    try:
        if algorithm == "promethee_ii":
            params = calculate_dynamic_promethee_params(dataset)
            Q, P, S, F = params
            result_raw = promethee_ii(dataset, W=weights_np, Q=Q, S=S, P=P, F=F, sort=True, topn=dataset.shape[0], graph=False)
            results = [{
                "rank_position": i + 1,
                "alternative_name": alternative_names_ordered[int(idx) - 1],
                "phi_score": float(score)
            } for i, (idx, score) in enumerate(result_raw)]
            return results, None

        elif algorithm == "electre_ii":
            params = {
                "c_minus": 0.65,
                "c_zero": 0.75,
                "c_plus": 0.85,
                "d_minus": 0.25,
                "d_plus": 0.50
            }
            
            #params = calculate_dynamic_electre_params(dataset)

            _, _, _, _, rank_D, rank_A, _, _ = electre_ii(dataset, W=weights_np, **params, graph=False)
            

            if return_internal_scores:
                num_alt = dataset.shape[0]
                ranks_v1, ranks_v2 = np.zeros(num_alt), np.zeros(num_alt)
                
                # rank_D é a pré-ordem descendente (v1)
                for rank, alternatives_in_rank in enumerate(rank_D, 1):
                    for alt_name in alternatives_in_rank:
                        idx = int(alt_name[1:]) - 1
                        ranks_v1[idx] = rank
                
                # rank_A é a pré-ordem ascendente (v2)
                for rank, alternatives_in_rank in enumerate(rank_A, 1):
                    for alt_name in alternatives_in_rank:
                        idx = int(alt_name[1:]) - 1
                        ranks_v2[idx] = rank
                        
                #Transformação E2        
                internal_scores = (
                    num_alt - ((ranks_v1 + ranks_v2) / 2)
                )
                return internal_scores, None
            
            # Para o ranking final, considera o rank_D como o principal.
            results = []
            for i, group in enumerate(rank_D, 1):
                original_names = [alternative_names_ordered[int(alt_name[1:]) - 1] for alt_name in group]
                results.append({"rank_position": i, "alternative_name": " / ".join(original_names)})
            
            return results, None

        else:
            return [], "Algoritmo não suportado."

    except Exception as e:
        print("--- OCORREU UM ERRO INTERNO ---")
        traceback.print_exc()
        print("-------------------------------")
        return [], f"Erro ao executar MCDA: {str(e)}"
