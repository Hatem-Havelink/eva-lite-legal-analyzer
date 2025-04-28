def build_prompt(contract_text: str) -> str:
    return f"""
You are a legal assistant specializing in contract analysis.

Analyze the following contract and provide:
- A concise summary.
- The list of key obligations.
- Identification and explanation of risks (minor and major).
- Extraction of any sensitive clauses with commentary.

CONTRACT TEXT:
{contract_text}
"""
