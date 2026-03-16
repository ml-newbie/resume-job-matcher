import os
from datetime import datetime

class OutputManager:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_all_formats(self, report_data):
        """Saves the Pydantic report to JSON and Markdown."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        # Sanitize name for filename
        safe_name = report_data.candidate_name.replace(" ", "_").lower()
        base_path = os.path.join(self.output_dir, f"{safe_name}_{timestamp}")

        self._save_json(report_data, f"{base_path}.json")
        self._save_markdown(report_data, f"{base_path}.md")
        
        print(f"✅ Reports saved to {self.output_dir}/")
        return base_path

    def _save_json(self, data, path):
        with open(path, "w") as f:
            f.write(data.model_dump_json(indent=4))

    def _save_markdown(self, data, path):
        md_content = f"""# 📄 Candidate Analysis: {data.candidate_name}
**Role:** {data.job_title} | **Match Score:** {data.overall_fit_score}/10
**Generated on:** {datetime.now().strftime("%B %d, %Y")}

---

## 🎯 Executive Summary
{data.executive_summary}

## 🛠️ Skills Gap Analysis
* **Matching Skills:** {", ".join(data.skills_match.matching_skills) if data.skills_match.matching_skills else "None detected"}
* **Missing Skills:** {", ".join(data.skills_match.missing_skills) if data.skills_match.missing_skills else "None"}
* **Critical Gaps:** {", ".join(data.skills_match.critical_gaps) if data.skills_match.critical_gaps else "No major gaps found"}

## 🚩 Recruiter Insights
{chr(10).join([f"- [!] {flag}" for flag in data.insights.potential_red_flags])}

## ❓ Suggested Interview Questions
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(data.insights.suggested_interview_questions)])}
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md_content)