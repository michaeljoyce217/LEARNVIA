# Implementation Notes for XML Configuration System

## Overview
This document provides technical guidance for implementing the XML-based configuration system for Learnvia's multi-agent review architecture.

## Directory Structure
```
/config/
├── rubrics/                    # Individual competency rubric definitions
│   ├── authoring_*.xml         # Authoring competency rubrics (5 files)
│   └── style_*.xml            # Style competency rubrics (5 files)
├── templates/                  # Agent system prompt templates
│   ├── rubric_focused_agent_template.xml
│   ├── generalist_agent_template.xml
│   └── IMPLEMENTATION_NOTES.md (this file)
└── agent_configuration.xml     # Master configuration file
```

## Loading and Using XML Templates

### 1. XML Parser Setup (Python Example)
```python
import xml.etree.ElementTree as ET
from pathlib import Path
import json

class LearnviaConfigLoader:
    def __init__(self, config_path="/config"):
        self.config_path = Path(config_path)
        self.rubrics = {}
        self.templates = {}
        self.master_config = None

    def load_rubric(self, competency_name):
        """Load a specific competency rubric"""
        filename = competency_name.lower().replace(" ", "_").replace("&", "and")
        rubric_path = self.config_path / "rubrics" / f"{filename}.xml"

        tree = ET.parse(rubric_path)
        root = tree.getroot()

        return self._parse_rubric(root)

    def _parse_rubric(self, root):
        """Parse rubric XML into usable dictionary"""
        rubric = {
            'metadata': {},
            'criteria': {},
            'diagnostic_questions': [],
            'patterns': {}
        }

        # Parse metadata
        for elem in root.find('metadata'):
            rubric['metadata'][elem.tag] = elem.text

        # Parse evaluation criteria by severity
        for severity in root.find('evaluation_criteria'):
            level = severity.get('level')
            rubric['criteria'][level] = {
                'label': severity.get('label'),
                'criteria': [c.text for c in severity.find('criteria')],
                'examples': [e.text for e in severity.find('examples')]
            }

        return rubric
```

### 2. Variable Substitution System

The templates use placeholder variables that need to be replaced when instantiating agents:

| Placeholder | Description | Source |
|-------------|-------------|---------|
| `{{COMPETENCY_NAME}}` | The specific competency name | Agent assignment from master config |
| `{{RUBRIC_XML_CONTENT}}` | Complete rubric XML for the competency | Loaded from `/config/rubrics/` |
| `{{FULL_AUTHORING_GUIDE}}` | Complete authoring guidelines | From existing guidelines doc |
| `{{FULL_STYLE_GUIDE}}` | Complete style guidelines | From existing style guide |
| `[TO_BE_FILLED]` | Runtime configuration values | Agent instantiation parameters |

### 3. Agent Instantiation Process

```python
class AgentFactory:
    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.authoring_guide = self._load_authoring_guide()
        self.style_guide = self._load_style_guide()

    def create_rubric_focused_agent(self, competency_name, category):
        """Create a rubric-focused agent for a specific competency"""

        # Load the template
        template = self._load_template('rubric_focused_agent_template.xml')

        # Load the specific rubric
        rubric = self.config_loader.load_rubric(f"{category}_{competency_name}")

        # Perform substitutions
        prompt = template.replace('{{COMPETENCY_NAME}}', competency_name)
        prompt = prompt.replace('{{RUBRIC_XML_CONTENT}}', ET.tostring(rubric))
        prompt = prompt.replace('{{FULL_AUTHORING_GUIDE}}', self.authoring_guide)
        prompt = prompt.replace('{{FULL_STYLE_GUIDE}}', self.style_guide)
        prompt = prompt.replace('[TO_BE_FILLED]', competency_name)

        return {
            'type': 'rubric_focused',
            'competency': competency_name,
            'system_prompt': prompt,
            'attention_weight': 0.8
        }

    def create_generalist_agent(self):
        """Create a generalist agent"""

        template = self._load_template('generalist_agent_template.xml')

        # Generalists don't have competency-specific content
        prompt = template.replace('{{FULL_AUTHORING_GUIDE}}', self.authoring_guide)
        prompt = prompt.replace('{{FULL_STYLE_GUIDE}}', self.style_guide)

        return {
            'type': 'generalist',
            'system_prompt': prompt,
            'evaluation_mode': 'holistic'
        }
```

## Integration with Existing Python Code

### 1. Minimal Changes to Current System
```python
# Old system
agent_prompt = load_prompt_from_string(PROMPT_TEXT)

# New system
agent_prompt = agent_factory.create_agent(competency, type).get('system_prompt')
```

### 2. Backward Compatibility Bridge
```python
class LegacyCompatibilityAdapter:
    """Adapter to maintain compatibility with existing code"""

    def __init__(self, xml_config_system):
        self.xml_system = xml_config_system

    def get_agent_prompt(self, agent_type, **kwargs):
        """Legacy interface that returns prompt string"""
        if agent_type == 'specialist':
            agent = self.xml_system.create_rubric_focused_agent(
                kwargs.get('competency'),
                kwargs.get('category', 'authoring')
            )
        else:
            agent = self.xml_system.create_generalist_agent()

        return agent['system_prompt']
```

## Migration Path from Current System

### Phase 1: Parallel Implementation (Recommended)
1. Implement XML loading system alongside existing code
2. Create comparison tests to ensure identical behavior
3. Gradually migrate agent creation to XML-based system
4. Keep existing prompts as fallback

### Phase 2: Full Migration
1. Replace hardcoded prompts with XML template loading
2. Update agent instantiation code
3. Implement configuration hot-reloading for development
4. Archive old prompt strings

### Migration Checklist
- [ ] Implement XML parser for rubrics
- [ ] Implement template loader with substitution
- [ ] Create agent factory using XML configs
- [ ] Add compatibility adapter for existing code
- [ ] Write comprehensive tests for XML loading
- [ ] Validate output equivalence with current system
- [ ] Performance test XML parsing overhead
- [ ] Document configuration update process
- [ ] Train team on XML configuration system
- [ ] Implement configuration validation tools

## Configuration Management Best Practices

### 1. Version Control
- Track all XML files in git
- Use semantic versioning in metadata
- Tag releases when updating rubrics

### 2. Validation
```python
def validate_rubric(rubric_path):
    """Validate rubric XML against schema"""
    # Check required elements exist
    # Validate severity levels 1-5
    # Ensure all cross-references are valid
    pass

def validate_configuration():
    """Validate entire configuration system"""
    # Check all referenced competencies have rubrics
    # Validate agent counts match configuration
    # Ensure all templates have required placeholders
    pass
```

### 3. Hot Reloading for Development
```python
class DevelopmentConfigLoader(LearnviaConfigLoader):
    """Auto-reload configurations when files change"""

    def __init__(self, config_path, watch=True):
        super().__init__(config_path)
        if watch:
            self._setup_file_watcher()

    def _setup_file_watcher(self):
        # Implement file system watcher
        # Reload affected configurations on change
        pass
```

## Testing Recommendations

### 1. Unit Tests for XML Parsing
- Test each rubric loads correctly
- Verify template substitution works
- Validate error handling for malformed XML

### 2. Integration Tests
- Test full agent creation pipeline
- Verify consensus rules work correctly
- Test configuration updates don't break system

### 3. Regression Tests
- Compare XML-based output to current system
- Ensure no degradation in review quality
- Performance benchmarks for XML parsing

## Performance Considerations

1. **Caching**: Cache parsed XML in memory after first load
2. **Lazy Loading**: Only load rubrics when needed
3. **Pre-compilation**: Pre-process templates for production
4. **Parallel Loading**: Load multiple rubrics concurrently

## Future Enhancements

1. **Schema Validation**: Add XSD schemas for strict validation
2. **Web UI**: Configuration editor interface
3. **A/B Testing**: Support multiple configuration versions
4. **Analytics**: Track which rubric criteria trigger most often
5. **Dynamic Weighting**: Adjust weights based on content type
6. **Custom Rubrics**: Allow subject-specific rubric extensions

## Troubleshooting

### Common Issues

1. **XML Parse Errors**
   - Check for unescaped special characters (&, <, >)
   - Validate XML syntax with linter
   - Ensure UTF-8 encoding

2. **Missing Substitutions**
   - Verify all placeholders are replaced
   - Check for typos in placeholder names
   - Ensure source data is available

3. **Performance Issues**
   - Implement caching for parsed XML
   - Use streaming parser for large files
   - Profile to identify bottlenecks

## Contact and Support

For questions about implementation:
- Review this documentation first
- Check the example code in `/config/examples/`
- Consult the XML schema definitions
- Contact the platform architecture team

Last Updated: 2024
Version: 1.0