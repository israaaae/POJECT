# tests/test_ragas_eval.py
import pytest
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from datasets import Dataset

@pytest.mark.evaluation
def test_rag_pipeline_eval():

    data = {
    "question": [
        "Quels sont les signes cliniques typiques d’un acrosyndrome vasculaire de type Raynaud ?",
        "Quels sont les symptômes d’une algie vasculaire de la face (cluster headache) ?",
        "Quels sont les diagnostics différentiels d’un amaigrissement isolé chez un patient jeune ?"
    ],
    "contexts": [
        ["Phénomène de Raynaud : déclenché par le froid, phase syncopale (pâleur d’un ou plusieurs doigts), suivie d’une cyanose et douleurs pulsatiles."],
        ["Algie vasculaire de la face : douleurs unilatérales orbito-temporales intenses, durée 30 sec à 2h, 1 à 8 crises/jour, avec larmoiement, rhinorrhée, syndrome de Claude Bernard-Horner."],
        ["Amaigrissement isolé : causes fréquentes = anorexie mentale, hyperthyroïdie, diabète, tuberculose, VIH, malabsorption, cancers."]
    ],
    "answer": [
        "Le phénomène de Raynaud associe une pâleur des doigts déclenchée par le froid, suivie d’une cyanose et de douleurs pulsatiles.",
        "Une algie vasculaire de la face provoque des douleurs unilatérales orbito-temporales intenses, brèves mais répétitives, associées à des signes oculaires et nasaux.",
        "Un amaigrissement isolé peut être dû à des troubles alimentaires (anorexie mentale), une hyperthyroïdie, un diabète, des infections comme la tuberculose ou le VIH, des malabsorptions ou encore des cancers."
    ],
    "ground_truth": [
        "Phénomène de Raynaud : alternance de pâleur, cyanose et douleurs digitales déclenchées par le froid.",
        "Cluster headache : douleur orbitaire unilatérale, courte, très intense, accompagnée de larmoiement, congestion nasale et parfois syndrome de Claude Bernard-Horner.",
        "Amaigrissement isolé : diagnostic différentiel inclut anorexie mentale, hyperthyroïdie, diabète, VIH, tuberculose, malabsorptions, cancers."
    ]
}
    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy]
    )

    df = result.to_pandas()
    df.to_csv('score.csv', index=False)

