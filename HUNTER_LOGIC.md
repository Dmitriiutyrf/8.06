# Jules' Hunter Engine: Filtering Logic (v1.0)

## 1. Discovery Phase
- **GitHub Trending:** Filter for repositories with >300 stars gained today.
- **Product Hunt:** Check top 10 daily launches in 'AI' and 'Software' categories.
- **Hacker News:** Search for "Show HN" with AI tags.
- **Gitee:** Look for trending AI/Short-video projects in China.

## 2. Evaluation Score (1-10)
Projects must score >7 to be packaged.

### A. MVP Speed (Weight: 40%)
- **Score 10:** Pure prompt-based, single file, or simple Streamlit/Python script.
- **Score 5:** Requires 1-2 external dependencies (API keys, basic pip install).
- **Score 1:** Complex Docker setups, local LLM requirements (>16GB VRAM), or non-portable code.

### B. Monetization Potential (Weight: 40%)
- **B2B Efficiency:** Can this save a company 10+ hours/week?
- **Mini-Franchise:** Can a freelancer use this to fulfill orders (Fiverr/Upwork)?
- **Content/Course:** Can this be sold as a "Secret Method" or "Upgrade Pack"?

### C. "Dmitry Standard" Fit (Weight: 20%)
- Can it be controlled via `start.bat`?
- Can it be explained in a 1-page Russian `GUIDE.md`?
- Is the license Permissive (MIT/Apache)?

## 3. Rejection Policy
- **Old news:** Project is >6 months old without recent updates.
- **SaaS Only:** No open-source engine to package.
- **High Risk:** Tools that violate TOS of major platforms (risky for the Digital Factory).

## 4. Output
- Create `reports/hunter_YYYY_MM_DD.md` with "Take", "Watch", and "Trash" sections.
- Package the single best "Take" project.
