import numpy as np
import single_evaluator as single_mcda
from typing import List, Dict, Any, Tuple, Optional

def aggregate_with_promethee(
    evaluator_results: List[Dict],
    evaluator_weights: List[float],
    alternatives: List[str]
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    
    aggregation_matrix_list = []
    for eval_result in evaluator_results:
        ranking, error = single_mcda.run_mcda_calculation(
            algorithm='promethee_ii',
            dataset=np.array(eval_result['dataset']),
            weights=eval_result['weights'],
            alternative_names_ordered=alternatives
        )
        if error:
            return [], f"Erro no avaliador '{eval_result['evaluator_name']}': {error}"
        
        scores = np.zeros(len(alternatives))
        for item in ranking:
            scores[alternatives.index(item['alternative_name'])] = item['phi_score']
        aggregation_matrix_list.append(scores)
        
    aggregation_matrix = np.array(aggregation_matrix_list).T
    
    return single_mcda.run_mcda_calculation(
        algorithm='promethee_ii',
        dataset=aggregation_matrix,
        weights=evaluator_weights,
        alternative_names_ordered=alternatives
    )

def aggregate_with_electre(
    evaluator_results: List[Dict],
    evaluator_weights: List[float],
    alternatives: List[str]
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    
    aggregation_matrix_list = []
    for eval_result in evaluator_results:
        scores, error = single_mcda.run_mcda_calculation(
            algorithm='electre_ii',
            dataset=np.array(eval_result['dataset']),
            weights=eval_result['weights'],
            alternative_names_ordered=alternatives,
            return_internal_scores=True
        )
        if error:
            return [], f"Erro no avaliador '{eval_result['evaluator_name']}': {error}"
        aggregation_matrix_list.append(scores)
        
    aggregation_matrix = np.array(aggregation_matrix_list).T

    return single_mcda.run_mcda_calculation(
        algorithm='electre_ii',
        dataset=aggregation_matrix,
        weights=evaluator_weights,
        alternative_names_ordered=alternatives
    )