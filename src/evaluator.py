"""Evaluate research paper quality."""

from typing import Dict, List
from .template import IEEETemplate


class QualityEvaluator:
    """Evaluates the quality of research paper content."""

    def evaluate(
        self, 
        text: str, 
        sections: Dict[str, str], 
        template: IEEETemplate
    ) -> Dict:
        """Evaluate paper quality across multiple dimensions."""
        
        return {
            "readability": self._evaluate_readability(text),
            "completeness": self._evaluate_completeness(sections, template),
            "structure": self._evaluate_structure(sections),
            "content_quality": self._evaluate_content_quality(text),
            "overall_score": self._calculate_overall_score(
                self._evaluate_readability(text),
                self._evaluate_completeness(sections, template),
                self._evaluate_structure(sections),
                self._evaluate_content_quality(text)
            )
        }

    @staticmethod
    def _evaluate_readability(text: str) -> Dict:
        """Evaluate document readability."""
        words = text.split()
        sentences = text.split('.')
        paragraphs = text.split('\n\n')
        
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        avg_words_per_paragraph = len(words) / len(paragraphs) if paragraphs else 0
        
        score = 100
        if avg_words_per_sentence > 25:  # Too long sentences
            score -= 15
        if avg_words_per_paragraph > 300:  # Too long paragraphs
            score -= 10
        
        return {
            "score": max(0, score),
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "avg_words_per_paragraph": round(avg_words_per_paragraph, 2)
        }

    @staticmethod
    def _evaluate_completeness(sections: Dict[str, str], template: IEEETemplate) -> Dict:
        """Evaluate content completeness."""
        section_keys = list(sections.keys())
        required = template.required_sections
        found_required = len([s for s in section_keys if s in required])
        
        completeness_score = (found_required / len(required) * 100) if required else 0
        
        return {
            "score": round(completeness_score, 2),
            "required_sections_found": found_required,
            "required_sections_total": len(required),
            "missing_sections": template.get_missing_sections(section_keys)
        }

    @staticmethod
    def _evaluate_structure(sections: Dict[str, str]) -> Dict:
        """Evaluate document structure."""
        section_count = len(sections)
        avg_section_length = sum(len(s.split()) for s in sections.values()) / section_count if section_count > 0 else 0
        
        score = 100
        if section_count < 5:
            score -= 20
        elif section_count > 20:
            score -= 10
        
        if avg_section_length < 100:
            score -= 15
        
        return {
            "score": max(0, score),
            "section_count": section_count,
            "avg_section_length": round(avg_section_length, 2)
        }

    @staticmethod
    def _evaluate_content_quality(text: str) -> Dict:
        """Evaluate content quality heuristics."""
        words = text.split()
        total_words = len(words)
        
        # Count technical terms (simplistic approach)
        technical_indicators = ['abstract', 'methodology', 'implementation', 'conclusion']
        tech_count = sum(text.lower().count(term) for term in technical_indicators)
        
        # Check for citations
        citation_indicators = ['[', ']', 'et al', 'et. al']
        citation_count = sum(text.count(indicator) for indicator in citation_indicators)
        
        score = 100
        if total_words < 2000:
            score -= 30
        if tech_count == 0:
            score -= 20
        if citation_count == 0:
            score -= 10
        
        return {
            "score": max(0, score),
            "total_words": total_words,
            "technical_indicators_found": tech_count,
            "citations_found": citation_count
        }

    @staticmethod
    def _calculate_overall_score(
        readability: Dict,
        completeness: Dict,
        structure: Dict,
        content: Dict
    ) -> float:
        """Calculate overall quality score."""
        weights = {
            "readability": 0.15,
            "completeness": 0.40,
            "structure": 0.20,
            "content": 0.25
        }
        
        overall = (
            readability["score"] * weights["readability"] +
            completeness["score"] * weights["completeness"] +
            structure["score"] * weights["structure"] +
            content["score"] * weights["content"]
        )
        
        return round(overall, 2)
