# # core/evaluator.py
# from typing import List, Dict
# import numpy as np
# from rouge_score import rouge_scorer

# class ResponseEvaluator:
#     def __init__(self):
#         self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
#     def evaluate_relevance(self, query: str, context: List[Dict]) -> float:
#         """Evaluate relevance of retrieved documents."""
#         scores = []
#         for doc in context:
#             rouge_scores = self.rouge_scorer.score(query, doc['text'])
#             scores.append(rouge_scores['rougeL'].fmeasure)
#         return np.mean(scores)
    
#     def evaluate_response(self, response: str, context: List[Dict]) -> Dict[str, float]:
#         """Evaluate generated response against context."""
#         context_text = " ".join([doc['text'] for doc in context])
#         rouge_scores = self.rouge_scorer.score(context_text, response)
        
#         return {
#             'relevance': rouge_scores['rougeL'].fmeasure,
#             'factuality': rouge_scores['rouge2'].fmeasure
#         }