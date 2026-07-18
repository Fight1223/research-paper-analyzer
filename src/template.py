"""IEEE Research Paper Template Definition."""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class SectionType(Enum):
    """Types of sections in a research paper."""
    REQUIRED = "required"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"


@dataclass
class SectionDefinition:
    """Definition of a paper section."""
    name: str
    section_type: SectionType
    min_length: int = 100
    max_length: Optional[int] = None
    subsections: List[str] = None
    description: str = ""
    examples: List[str] = None

    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []
        if self.examples is None:
            self.examples = []


class IEEETemplate:
    """IEEE Research Paper Template Structure.
    
    Based on the provided template from University of Saba Region.
    Defines the required sections, their order, and validation rules.
    """

    def __init__(self):
        self.sections = self._define_sections()
        self.required_sections = self._get_required_sections()
        self.section_order = self._define_order()

    def _define_sections(self) -> Dict[str, SectionDefinition]:
        return {
            "title": SectionDefinition(
                name="Title",
                section_type=SectionType.REQUIRED,
                min_length=5,
                max_length=20,
                description="Project title - should be concise and descriptive"
            ),
            "author_info": SectionDefinition(
                name="Author Information",
                section_type=SectionType.REQUIRED,
                description="Student name, ID, program, and university",
                subsections=["Student Name", "ID Number", "Program Name", "University"]
            ),
            "abstract": SectionDefinition(
                name="Abstract",
                section_type=SectionType.REQUIRED,
                min_length=300,
                max_length=350,
                description="Summary of the entire paper (300-350 words)"
            ),
            "contents": SectionDefinition(
                name="Contents/Table of Contents",
                section_type=SectionType.REQUIRED,
                description="Complete list of all chapters, sections, and subsections"
            ),
            "list_of_figures": SectionDefinition(
                name="List of Figures",
                section_type=SectionType.REQUIRED,
                description="All figures used in the paper with titles and page numbers"
            ),
            "list_of_tables": SectionDefinition(
                name="List of Tables",
                section_type=SectionType.REQUIRED,
                description="All tables used in the paper with titles and page numbers"
            ),
            "list_of_appendix": SectionDefinition(
                name="List of Appendix",
                section_type=SectionType.OPTIONAL,
                description="List of appendices (if applicable)"
            ),
            "chapter_1_introduction": SectionDefinition(
                name="Chapter 1: Introduction",
                section_type=SectionType.REQUIRED,
                min_length=500,
                subsections=[
                    "1.1 Project Background",
                    "1.2 Problem Statement",
                    "1.3 Objective",
                    "1.4 Scope",
                    "1.5 Expected Result",
                    "1.6 Project Significance",
                    "1.7 Chapter Summary",
                    "1.8 Report Organization"
                ]
            ),
            "chapter_2_literature_review": SectionDefinition(
                name="Chapter 2: Literature Review",
                section_type=SectionType.REQUIRED,
                min_length=1000,
                subsections=[
                    "2.1-2.4 Related Concepts",
                    "2.5 Study of Current Process",
                    "2.6 Study of Existing Systems",
                    "2.7 Comparison with Existing Systems",
                    "2.8 Chapter Summary"
                ]
            ),
            "chapter_3_methodology": SectionDefinition(
                name="Chapter 3: Methodology",
                section_type=SectionType.REQUIRED,
                min_length=500,
                subsections=[
                    "3.1 Prototyping Model",
                    "3.2 System Development Workflow",
                    "3.3 Chapter Summary"
                ]
            ),
            "chapter_4_analysis_design": SectionDefinition(
                name="Chapter 4: Analysis and Design",
                section_type=SectionType.REQUIRED,
                min_length=1000,
                subsections=[
                    "4.1 System Requirement Analysis",
                    "4.2 Design",
                    "4.3 Chapter Summary"
                ]
            ),
            "chapter_5_implementation_testing": SectionDefinition(
                name="Chapter 5: Implementation and Testing",
                section_type=SectionType.REQUIRED,
                min_length=800,
                subsections=[
                    "5.1 Implementation",
                    "5.2 Testing",
                    "5.3 Chapter Summary"
                ]
            ),
            "chapter_6_conclusion": SectionDefinition(
                name="Chapter 6: Conclusion",
                section_type=SectionType.REQUIRED,
                min_length=300,
                subsections=[
                    "6.1 System Advantages",
                    "6.2 System Disadvantages",
                    "6.3 Recommendations",
                    "6.4 Summary"
                ]
            ),
            "references": SectionDefinition(
                name="References",
                section_type=SectionType.REQUIRED,
                min_length=50,
                description="All cited references in proper format"
            ),
            "appendix": SectionDefinition(
                name="Appendix",
                section_type=SectionType.OPTIONAL,
                description="Additional supporting materials (if applicable)"
            )
        }

    def _get_required_sections(self) -> List[str]:
        return [
            key for key, section in self.sections.items()
            if section.section_type == SectionType.REQUIRED
        ]

    def _define_order(self) -> List[str]:
        return [
            "title",
            "author_info",
            "abstract",
            "contents",
            "list_of_figures",
            "list_of_tables",
            "list_of_appendix",
            "chapter_1_introduction",
            "chapter_2_literature_review",
            "chapter_3_methodology",
            "chapter_4_analysis_design",
            "chapter_5_implementation_testing",
            "chapter_6_conclusion",
            "references",
            "appendix"
        ]

    def get_section(self, section_key: str) -> Optional[SectionDefinition]:
        return self.sections.get(section_key)

    def get_all_sections(self) -> Dict[str, SectionDefinition]:
        return self.sections

    def validate_section_order(self, found_sections: List[str]) -> bool:
        indices = []
        for section in found_sections:
            if section in self.section_order:
                indices.append(self.section_order.index(section))
        return indices == sorted(indices)

    def get_missing_sections(self, found_sections: List[str]) -> List[str]:
        return [
            section for section in self.required_sections
            if section not in found_sections
        ]

    def get_optional_missing(self, found_sections: List[str]) -> List[str]:
        optional = [
            key for key, section in self.sections.items()
            if section.section_type == SectionType.OPTIONAL
        ]
        return [section for section in optional if section not in found_sections]

