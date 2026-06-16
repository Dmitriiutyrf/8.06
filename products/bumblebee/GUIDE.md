# Bumblebee: AI Security Scanner

### Purpose
Bumblebee is a read-only security scanner designed for developers in the AI era. It audits your local environment for malicious packages, suspicious MCP servers, and compromised browser/editor extensions.

### Pain Points
- **MCP Supply Chain Risks:** Installing MCP servers from unverified sources (Discord, GitHub) can expose your machine to data theft.
- **Hidden Dependencies:** AI coding tools often install packages that developers don't audit manually.
- **Extension Bloat:** Malicious VS Code or browser extensions can access sensitive project data.

### Setup
Bumblebee is a single static binary written in Go.
1. **Requirements:** Go 1.25 or higher.
2. **Installation:**
   ```bash
   go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest
   ```
3. **Smoke Test:**
   ```bash
   bumblebee selftest
   ```

### Usage
- **Baseline Scan (Global/User roots):**
  ```bash
  bumblebee scan --profile baseline
  ```
- **Project Scan (Current directory):**
  ```bash
  bumblebee scan --profile project --root .
  ```

### Monetization Strategy
- **B2B Efficiency:** Sell as a "Compliance & Security Pack" for companies transitioning to AI-first development.
- **Service Model:** Offer "AI Security Audits" for startups, using Bumblebee to generate exposure reports.
- **Mini-Franchise:** Bundle with other AI-dev tools as a "Pro Security Upgrade".
