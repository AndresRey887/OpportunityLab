"""
Gemini AI Provider

Uses Gemini as OpportunityLab's structured Opportunity Scout.
"""

import json

from google import genai
from google.genai import types

from config.secrets import GEMINI_API_KEY
from src.ai.ai_provider import AIProvider
from src.ai.opportunity_analysis import OpportunityAnalysis


class GeminiProvider(AIProvider):

    def __init__(
        self,
        api_key=None,
        model="gemini-3.5-flash"
    ):

        super().__init__("Gemini")

        self.api_key = (
            api_key
            if api_key is not None
            else GEMINI_API_KEY
        )

        self.api_key = str(self.api_key).strip()
        self.model = model

        self.available = bool(self.api_key)
        self.client = None

        if self.available:

            self.client = genai.Client(
                api_key=self.api_key
            )

    def analyze(self, opportunity):

        if not self.is_available() or self.client is None:

            return OpportunityAnalysis(
                summary="Gemini is not configured.",
                category="Provider unavailable",
                confidence=0,
                opportunity_value=0,
                recommended_action=(
                    "Add a valid Gemini API key to "
                    "config/secrets.py."
                ),
                provider=self.name,
                model=self.model
            )

        prompt = self._build_prompt(opportunity)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=1800,
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string"
                        },
                        "category": {
                            "type": "string"
                        },
                        "confidence": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "opportunity_value": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "difficulty": {
                            "type": "string"
                        },
                        "time_sensitivity": {
                            "type": "string"
                        },
                        "estimated_effort": {
                            "type": "string"
                        },
                        "recommended_action": {
                            "type": "string"
                        },
                        "positives": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "negatives": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "tags": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "warnings": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [
                        "summary",
                        "category",
                        "confidence",
                        "opportunity_value",
                        "difficulty",
                        "time_sensitivity",
                        "estimated_effort",
                        "recommended_action",
                        "positives",
                        "negatives",
                        "tags",
                        "warnings"
                    ]
                }
            )
        )

        if not response.text:

            return OpportunityAnalysis(
                summary="Gemini returned an empty response.",
                category="Analysis unavailable",
                confidence=0,
                opportunity_value=0,
                recommended_action=(
                    "Try analysing the opportunity again."
                ),
                provider=self.name,
                model=self.model
            )

        data = json.loads(response.text)

        return self._create_analysis(data)

    def _build_prompt(self, opportunity):

        rule_breakdown = self._format_rule_breakdown(
            getattr(opportunity, "rule_results", [])
        )

        return f"""
You are Opportunity Scout AI working exclusively inside OpportunityLab.

Your purpose is to identify genuine opportunities and help the user
decide whether each result deserves their time.

You are not merely summarising a webpage.

Act as a cautious professional opportunity researcher looking for:

- Product testing and review programs
- Beta testing and early-access programs
- Free samples and trial programs
- Manufacturers and wholesale suppliers
- Dealer, distributor and affiliate programs
- Trade shows and industry events
- Grants, competitions and innovation challenges
- Startup and research programs
- Licensing and partnership opportunities
- New products, technologies and commercial trends
- Business opportunities suitable for small operators
- Opportunities relevant to hobbyists, inventors and creators

Important rules:

- Base the analysis only on the information supplied below.
- Never invent eligibility, prices, deadlines, locations or benefits.
- Clearly identify missing or uncertain information.
- Distinguish a real opportunity from advertising, news or general content.
- The confidence score means how certain you are about your analysis.
- The opportunity value score means how worthwhile this result appears.
- Do not simply copy the existing rule score.
- Use the existing rule score as one input and apply independent judgement.
- Keep all output concise, practical and useful.

Allowed difficulty values:

- Easy
- Moderate
- Difficult
- Unknown

Allowed time-sensitivity values:

- Urgent
- Soon
- Not time sensitive
- Unknown

Opportunity information:

Title:
{getattr(opportunity, "title", "")}

URL:
{getattr(opportunity, "url", "")}

Domain:
{getattr(opportunity, "domain", "")}

Source:
{getattr(opportunity, "source", "")}

Search snippet:
{getattr(opportunity, "snippet", "")}

OpportunityLab rule score:
{getattr(opportunity, "score", 0)} out of 100

Rule breakdown:
{rule_breakdown}

Return structured information containing:

- A concise summary
- A short category
- Confidence from 0 to 100
- Opportunity value from 0 to 100
- Difficulty
- Time sensitivity
- Estimated effort, such as "10-20 minutes", "Several hours" or "Unknown"
- Up to four positive factors
- Up to four drawbacks or uncertainties
- Up to six useful tags
- Up to four clear warnings
- One specific recommended next action

The recommended action should be practical.

Examples:

- Visit the official application page and verify Australian eligibility.
- Check the closing date before preparing an application.
- Find the company's product-testing page before making contact.
- Ignore this result because it appears to be general advertising.
"""

    def _format_rule_breakdown(self, rule_results):

        if not isinstance(rule_results, list):
            return "No rule breakdown available."

        lines = []

        for result in rule_results:

            if not isinstance(result, dict):
                continue

            rule_name = str(
                result.get("rule", "Unknown rule")
            ).strip()

            points = result.get("points", 0)

            lines.append(
                f"- {rule_name}: {points:+} points"
            )

        if not lines:
            return "No rule breakdown available."

        return "\n".join(lines)

    def _create_analysis(self, data):

        confidence = self._clean_score(
            data.get("confidence", 0)
        )

        opportunity_value = self._clean_score(
            data.get("opportunity_value", 0)
        )

        difficulty = self._clean_choice(
            data.get("difficulty", "Unknown"),
            {
                "easy",
                "moderate",
                "difficult",
                "unknown"
            },
            "Unknown"
        )

        time_sensitivity = self._clean_choice(
            data.get("time_sensitivity", "Unknown"),
            {
                "urgent",
                "soon",
                "not time sensitive",
                "unknown"
            },
            "Unknown"
        )

        return OpportunityAnalysis(
            summary=str(
                data.get("summary", "")
            ).strip(),
            category=str(
                data.get("category", "")
            ).strip(),
            confidence=confidence,
            opportunity_value=opportunity_value,
            difficulty=difficulty,
            time_sensitivity=time_sensitivity,
            estimated_effort=str(
                data.get("estimated_effort", "Unknown")
            ).strip() or "Unknown",
            recommended_action=str(
                data.get("recommended_action", "")
            ).strip(),
            positives=self._clean_list(
                data.get("positives", []),
                limit=4
            ),
            negatives=self._clean_list(
                data.get("negatives", []),
                limit=4
            ),
            tags=self._clean_list(
                data.get("tags", []),
                limit=6
            ),
            warnings=self._clean_list(
                data.get("warnings", []),
                limit=4
            ),
            provider=self.name,
            model=self.model
        )

    def _clean_score(self, value):

        try:
            value = int(value)

        except (TypeError, ValueError):
            value = 0

        return max(0, min(value, 100))

    def _clean_choice(
        self,
        value,
        allowed_values,
        default
    ):

        text = str(value).strip()

        if text.lower() not in allowed_values:
            return default

        if text.lower() == "not time sensitive":
            return "Not time sensitive"

        return text.capitalize()

    def _clean_list(self, values, limit=4):

        if not isinstance(values, list):
            return []

        cleaned = []

        for value in values:

            text = str(value).strip()

            if text and text not in cleaned:
                cleaned.append(text)

        return cleaned[:limit]