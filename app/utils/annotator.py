from typing import List, Dict

def annotate_contract(text: str, sensitive_clauses: List[Dict[str, str]]) -> str:
    """
    Annotate the original contract text by highlighting sensitive clauses.
    """
    annotated_text = text

    for clause_info in sensitive_clauses:
        clause_title = clause_info.get("clause")
        if clause_title:
            # On souligne toutes les occurrences du titre de clause dans le texte (simple)
            annotated_text = annotated_text.replace(
                clause_title,
                f"**[CLAUSE IMPORTANTE : {clause_title}]**"
            )
    
    return annotated_text
