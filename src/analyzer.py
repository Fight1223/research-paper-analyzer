"""Main research paper analyzer."""

from typing import Dict, List, Optional
from pathlib import Path
import json

from anthropic import Anthropic

from .extractor import PaperExtractor
from .template import IEEETemplate
from .comparator import StructureComparator
from .evaluator import QualityEvaluator
from .reporter import ReportGenerator


class ResearchPaperAnalyzer:
    """Analyzes research papers against IEEE template structure."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize analyzer with API key."""
        self.client = Anthropic()
        self.template = IEEETemplate()
        self.extractor = PaperExtractor()
        self.comparator = StructureComparator()
        self.evaluator = QualityEvaluator()
        self.reporter = ReportGenerator()

    def analyze_paper(self, file_path: str) -> Dict:
        """Analyze a research paper file."""
        # Extract text
        text = self.extractor.extract_from_file(file_path)
        
        # Identify sections
        sections = self.extractor.identify_sections(text)
        
        # Compare with IEEE template
        comparison = self.comparator.compare(sections, self.template)
        
        # Evaluate quality
        evaluation = self.evaluator.evaluate(text, sections, self.template)
        
        # Generate report
        report = self.reporter.generate_report(
            file_path=file_path,
            sections=sections,
            comparison=comparison,
            evaluation=evaluation,
            template=self.template
        )
        
        return {
            "file": file_path,
            "extracted_sections": list(sections.keys()),
            "comparison": comparison,
            "evaluation": evaluation,
            "report": report
        }

    def analyze_with_claude(self, file_path: str) -> Dict:
        """Analyze paper using Claude for deeper insights."""
        text = self.extractor.extract_from_file(file_path)
        
        conversation_history = []
        
        # First turn: Ask Claude to identify sections
        conversation_history.append({
            "role": "user",
            "content": f"""Please analyze this research paper and identify all major sections and chapters. 
List them in order with their approximate content length.

Paper content:
{text[:5000]}...
"""
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=conversation_history
        )
        
        sections_analysis = response.content[0].text
        conversation_history.append({
            "role": "assistant",
            "content": sections_analysis
        })
        
        # Second turn: Ask about compliance
        conversation_history.append({
            "role": "user",
            "content": """Based on your analysis, how well does this paper comply with IEEE standards? 
What sections are missing or need improvement?"""
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=conversation_history
        )
        
        compliance_analysis = response.content[0].text
        conversation_history.append({
            "role": "assistant",
            "content": compliance_analysis
        })
        
        # Third turn: Get recommendations
        conversation_history.append({
            "role": "user",
            "content": """Please provide specific, actionable recommendations for improving this paper 
to meet IEEE standards."""
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=conversation_history
        )
        
        recommendations = response.content[0].text
        
        return {
            "file": file_path,
            "sections_analysis": sections_analysis,
            "compliance_analysis": compliance_analysis,
            "recommendations": recommendations,
            "conversation_history": conversation_history
        }

    def validate_structure(self, file_path: str) -> Dict:
        """Validate paper structure against template."""
        text = self.extractor.extract_from_file(file_path)
        sections = self.extractor.identify_sections(text)
        
        missing = self.template.get_missing_sections(list(sections.keys()))
        optional_missing = self.template.get_optional_missing(list(sections.keys()))
        order_valid = self.template.validate_section_order(list(sections.keys()))
        
        return {
            "found_sections": list(sections.keys()),
            "missing_required": missing,
            "missing_optional": optional_missing,
            "section_order_valid": order_valid,
            "compliance_score": self._calculate_compliance_score(
                missing, optional_missing, order_valid
            )
        }

    @staticmethod
    def _calculate_compliance_score(
        missing_required: List[str],
        missing_optional: List[str],
        order_valid: bool
    ) -> float:
        """Calculate compliance score (0-100)."""
        score = 100.0
        
        # Deduct for missing required sections
        score -= len(missing_required) * 10
        
        # Deduct for missing optional sections
        score -= len(missing_optional) * 2
        
        # Deduct for wrong order
        if not order_valid:
            score -= 5
        
        return max(0, min(100, score))
