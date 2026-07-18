"""Example usage of the Research Paper Analyzer."""

from src import ResearchPaperAnalyzer, IEEETemplate
import json


def main():
    """Main example function."""
    
    # Initialize the analyzer
    analyzer = ResearchPaperAnalyzer()
    
    # Example 1: Analyze paper structure
    print("=" * 60)
    print("Example 1: Validate Paper Structure")
    print("=" * 60)
    
    # This would work with an actual paper file
    # validation = analyzer.validate_structure("path/to/paper.pdf")
    # print(json.dumps(validation, indent=2))
    
    print("To analyze a paper, use:")
    print("  validation = analyzer.validate_structure('paper.pdf')")
    print()
    
    # Example 2: Full analysis with report
    print("=" * 60)
    print("Example 2: Full Analysis with Report")
    print("=" * 60)
    
    # This would work with an actual paper file
    # result = analyzer.analyze_paper("path/to/paper.pdf")
    # print(result["report"])
    
    print("To generate a full analysis report, use:")
    print("  result = analyzer.analyze_paper('paper.pdf')")
    print("  print(result['report'])")
    print()
    
    # Example 3: Claude-powered analysis
    print("=" * 60)
    print("Example 3: AI-Powered Analysis with Claude")
    print("=" * 60)
    
    # This would work with an actual paper file and API key
    # result = analyzer.analyze_with_claude("path/to/paper.pdf")
    # print("Sections Analysis:")
    # print(result["sections_analysis"])
    # print("\nCompliance Analysis:")
    # print(result["compliance_analysis"])
    # print("\nRecommendations:")
    # print(result["recommendations"])
    
    print("To use Claude for deeper analysis, use:")
    print("  result = analyzer.analyze_with_claude('paper.pdf')")
    print()
    
    # Example 4: IEEE Template Information
    print("=" * 60)
    print("Example 4: IEEE Template Information")
    print("=" * 60)
    
    template = IEEETemplate()
    print(f"Required sections: {len(template.required_sections)}")
    print(f"Optional sections: {len(template.get_optional_missing([]))}")
    print()
    
    print("Required sections are:")
    for i, section_key in enumerate(template.required_sections, 1):
        section = template.get_section(section_key)
        print(f"  {i}. {section.name}")
    print()
    
    # Example 5: Working with extracted text
    print("=" * 60)
    print("Example 5: Extract and Identify Sections")
    print("=" * 60)
    
    # from src.extractor import PaperExtractor
    # extractor = PaperExtractor()
    # text = extractor.extract_from_file("paper.pdf")
    # sections = extractor.identify_sections(text)
    # print(f"Found {len(sections)} sections")
    
    print("To extract text from a paper:")
    print("  from src.extractor import PaperExtractor")
    print("  extractor = PaperExtractor()")
    print("  text = extractor.extract_from_file('paper.pdf')")
    print("  sections = extractor.identify_sections(text)")
    print()
    

if __name__ == "__main__":
    main()
