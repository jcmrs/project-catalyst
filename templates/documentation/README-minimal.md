---
id: readme-minimal
version: 1.0.0
category: documentation
description: Minimal README for quick project setup
language: markdown
dependencies: []
variables:
  - name: PROJECT_NAME
    description: Name of the project
    required: true
  - name: DESCRIPTION
    description: Brief project description
    required: true
  - name: AUTHOR
    description: Project author
    required: false
    default: ""
---

# ${PROJECT_NAME}

${DESCRIPTION}

## Installation

\`\`\`bash
npm install ${PROJECT_NAME}
\`\`\`

## Usage

\`\`\`bash
${PROJECT_NAME} --help
\`\`\`

## License

MIT - See [LICENSE](./LICENSE)

## Author

${AUTHOR}
