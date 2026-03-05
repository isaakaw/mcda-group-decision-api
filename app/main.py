from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import numpy as np
import aggregation_methods as aggregation_methods
import single_evaluator as single_evaluator

app = FastAPI(title="MCDA API - v1.0")

# --- Modelos de Requisição ---

class MCDARequest(BaseModel):
    dataset: List[List[float]]
    weights: List[float]
    algorithm: str
    alternatives: List[str]

class EvaluatorResult(BaseModel):
    evaluator_name: str
    dataset: List[List[float]]
    weights: List[float]

class AggregationRequest(BaseModel):
    evaluator_results: List[EvaluatorResult]
    evaluator_weights: List[float]
    algorithm: str = Field(..., description="Use 'promethee_ii' ou 'electre_ii'")
    alternatives: List[str]

# --- Endpoints ---

@app.post("/run-mcda/", summary="Executa um cálculo MCDA simples")
def run_mcda(request: MCDARequest):
    dataset_np = np.array(request.dataset)
    
    ranking, error = single_evaluator.run_mcda_calculation(
        algorithm=request.algorithm,
        dataset=dataset_np,
        weights=request.weights,
        alternative_names_ordered=request.alternatives
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"success": True, "ranking": ranking}


@app.post("/aggregate-mcda/", summary="Agrega resultados de múltiplos avaliadores")
def aggregate_mcda(request: AggregationRequest):
    evaluator_data_dict = [er.dict() for er in request.evaluator_results]
    
    if request.algorithm == 'promethee_ii':
        ranking, error = aggregation_methods.aggregate_with_promethee(
            evaluator_results=evaluator_data_dict,
            evaluator_weights=request.evaluator_weights,
            alternatives=request.alternatives
        )
    elif request.algorithm == 'electre_ii':
        ranking, error = aggregation_methods.aggregate_with_electre(
            evaluator_results=evaluator_data_dict,
            evaluator_weights=request.evaluator_weights,
            alternatives=request.alternatives
        )
    else:
        raise HTTPException(status_code=400, detail="Algoritmo não suportado.")

    if error:
        raise HTTPException(status_code=400, detail=error)

    return {"success": True, "final_ranking": ranking}