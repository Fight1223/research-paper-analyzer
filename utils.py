"""Utility functions for the research paper analyzer."""

import json
from typing import Dict, Any, List


def pretty_print_json(data: Dict[str, Any]) -> str:
    """Pretty print JSON data."""
    return json.dumps(data, indent=2)


def save_report(report: str, output_path: str) -> None:
    """Save analysis report to file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)


def load_paper_list(file_path: str) -> List[str]:
    """Load list of paper paths from file."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def summarize_results(results: List[Dict]) -> Dict:
    """Summarize multiple analysis results."""
    if not results:
        return {"total": 0, "average_compliance": 0}
    
    total = len(results)
    avg_compliance = sum(
        r.get('comparison', {}).get('compliance_percentage', 0)
        for r in results
    ) / total
    
    return {
        "total_papers": total,
        "average_compliance": round(avg_compliance, 2),
        "results": results
    }
