"""Compare paper structure with IEEE template."""

from typing import Dict, List
from .template import IEEETemplate, SectionType


class StructureComparator:
    """Compares extracted paper structure with IEEE template."""

    def compare(self, found_sections: Dict[str, str], template: IEEETemplate) -> Dict:
        """Compare found sections with template requirements."""
        section_keys = list(found_sections.keys())
        
        # Find missing required sections
        missing_required = template.get_missing_sections(section_keys)
        
        # Find missing optional sections
        missing_optional = template.get_optional_missing(section_keys)
        
        # Check section order
        order_valid = template.validate_section_order(section_keys)
        
        # Analyze each found section
        section_analysis = {}
        for section_key in section_keys:
            definition = template.get_section(section_key)
            content = found_sections[section_key]
            
            if definition:
                section_analysis[section_key] = self._analyze_section(
                    definition, content
                )
        
        return {
            "found_sections": section_keys,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "section_order_valid": order_valid,
            "section_details": section_analysis,
            "compliance_percentage": self._calculate_compliance(
                section_keys, missing_required, missing_optional, order_valid, template
            )
        }

    @staticmethod
    def _analyze_section(definition, content: str) -> Dict:
        """Analyze individual section."""
        word_count = len(content.split())
        
        analysis = {
            "name": definition.name,
            "type": definition.section_type.value,
            "word_count": word_count,
            "meets_minimum": word_count >= definition.min_length if definition.min_length else True,
            "meets_maximum": True,
            "description": definition.description
        }
        
        if definition.max_length:
            analysis["meets_maximum"] = word_count <= definition.max_length
        
        if definition.subsections:
            analysis["expected_subsections"] = definition.subsections
        
        return analysis

    @staticmethod
    def _calculate_compliance(
        found: List[str],
        missing_required: List[str],
        missing_optional: List[str],
        order_valid: bool,
        template: IEEETemplate
    ) -> float:
        """Calculate compliance percentage."""
        total_required = len(template.required_sections)
        found_required = len([s for s in found if s in template.required_sections])
        
        compliance = (found_required / total_required * 100) if total_required > 0 else 0
        
        # Adjust for order
        if not order_valid:
            compliance *= 0.95
        
        return round(compliance, 2)
