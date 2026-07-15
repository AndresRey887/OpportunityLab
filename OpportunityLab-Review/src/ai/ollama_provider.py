"""
Ollama AI Provider

Provides local, quota-free AI tasks for OpportunityLab.
"""

import re

import requests

from src.ai.ai_provider import AIProvider


class OllamaProvider(AIProvider):

    def __init__(
        self,
        model="qwen3:4b",
        base_url="http://localhost:11434",
        timeout=120
    ):

        super().__init__("Ollama")

        self.model = str(model).strip()
        self.base_url = str(base_url).rstrip("/")
        self.timeout = timeout

        self.available = False
        self.installed_models = []
        self.last_error = ""

    def is_available(self):

        self.refresh_status()

        return self.available

    def refresh_status(self):

        self.available = False
        self.installed_models = []
        self.last_error = ""

        try:

            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            models = data.get("models", [])

            self.installed_models = [
                str(model.get("name", "")).strip()
                for model in models
                if model.get("name")
            ]

            self.available = self._model_is_installed()

        except requests.RequestException as error:

            self.last_error = str(error)

        except (TypeError, ValueError) as error:

            self.last_error = str(error)

        return self.available

    def get_installed_models(self):

        self.refresh_status()

        return list(self.installed_models)

    def get_status_message(self):

        self.refresh_status()

        if self.available:

            return (
                f"Ollama is available using {self.model}."
            )

        if self.installed_models:

            return (
                f"Ollama is running, but {self.model} "
                "is not installed."
            )

        if self.last_error:

            return (
                "Ollama could not be reached. "
                "Confirm that Ollama is running."
            )

        return "No Ollama models are installed."

    def suggest_related_searches(
        self,
        context,
        limit=6
    ):

        query = self._extract_text(context)

        try:
            limit = int(limit)

        except (TypeError, ValueError):
            limit = 6

        limit = max(1, min(limit, 10))

        prompt = f"""
You are the local Related Search Scout inside OpportunityLab.

Current search:
{query}

Create exactly {limit} useful web-search phrases that explore
nearby opportunities.

Focus on combinations involving:

- Product testing
- Beta programs
- Manufacturers
- Suppliers and distributors
- Brand ambassador programs
- Dealer or affiliate programs
- Trade shows
- Research studies
- Innovation challenges
- Australian opportunities where relevant

Rules:

- Keep each suggestion concise.
- Make every suggestion meaningfully different.
- Do not repeat the original search unchanged.
- Do not explain your choices.
- Do not number the suggestions.
- Return one search phrase per line only.
- Do not include introductory or concluding text.
"""

        response = self._chat(
            prompt,
            temperature=0.4
        )

        response = self._remove_thinking(
            response
        )

        suggestions = []

        for line in response.splitlines():

            text = self._clean_suggestion_line(
                line
            )

            if not text:
                continue

            if text.lower() == query.lower():
                continue

            if text.lower() not in {
                item.lower()
                for item in suggestions
            }:

                suggestions.append(text)

        return suggestions[:limit]

    def draft_email(
        self,
        context,
        tone="professional and friendly"
    ):

        opportunity_text = self._format_opportunity(
            context
        )

        prompt = f"""
You are the local writing assistant inside OpportunityLab.

Draft a concise enquiry email about the opportunity below.

Tone:
{tone}

Opportunity:
{opportunity_text}

Requirements:

- Do not invent the recipient's name.
- Do not claim experience or qualifications not supplied.
- Ask clearly about participation, eligibility and next steps.
- Include a useful subject line.
- Keep the email under 250 words.
"""

        return self._chat(prompt)

    def draft_application(
        self,
        context,
        user_notes=""
    ):

        opportunity_text = self._format_opportunity(
            context
        )

        prompt = f"""
You are the local application-writing assistant inside OpportunityLab.

Prepare a first-draft application statement.

Opportunity:
{opportunity_text}

User notes:
{user_notes or "No additional user notes supplied."}

Requirements:

- Do not invent personal experience or qualifications.
- Mark missing personal information with square-bracket placeholders.
- Explain genuine interest in the opportunity.
- Keep the draft clear and practical.
- Keep it under 400 words.
"""

        return self._chat(prompt)

    def create_checklist(
        self,
        context
    ):

        opportunity_text = self._format_opportunity(
            context
        )

        prompt = f"""
You are the local task assistant inside OpportunityLab.

Create a practical checklist for investigating and acting on
this opportunity.

Opportunity:
{opportunity_text}

Requirements:

- Return one task per line.
- Prefix every task with [ ].
- Include verification, eligibility and follow-up steps.
- Do not invent deadlines or requirements.
- Return no more than 10 tasks.
"""

        return self._chat(prompt)

    def rewrite_text(
        self,
        context,
        instruction="Make the text clear and professional."
    ):

        text = self._extract_text(context)

        prompt = f"""
Rewrite the following text.

Instruction:
{instruction}

Text:
{text}

Return only the rewritten text.
"""

        return self._chat(prompt)

    def _chat(
        self,
        prompt,
        temperature=0.3
    ):

        if not self.is_available():

            raise RuntimeError(
                self.get_status_message()
            )

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            },
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        message = data.get("message", {})

        content = str(
            message.get("content", "")
        ).strip()

        if not content:

            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return content

    def _remove_thinking(self, text):

        cleaned = re.sub(
            r"<think>.*?</think>",
            "",
            str(text),
            flags=re.DOTALL | re.IGNORECASE
        )

        return cleaned.strip()

    def _clean_suggestion_line(self, line):

        text = str(line).strip()

        text = re.sub(
            r"^\s*\d+[\.\)\-:]\s*",
            "",
            text
        )

        text = text.lstrip("-•* ").strip()

        text = text.strip("\"'")

        if not text:
            return ""

        if text.lower().startswith(
            (
                "here are",
                "related searches",
                "suggestions:",
                "search ideas:"
            )
        ):
            return ""

        return text

    def _model_is_installed(self):

        selected = self.model.lower()

        for installed_model in self.installed_models:

            installed = installed_model.lower()

            if installed == selected:
                return True

            if installed.split(":")[0] == selected:
                return True

        return False

    def _extract_text(self, context):

        if context is None:
            return ""

        if isinstance(context, str):
            return context.strip()

        query = getattr(
            context,
            "query",
            None
        )

        if query:
            return str(query).strip()

        return self._format_opportunity(
            context
        )

    def _format_opportunity(
        self,
        opportunity
    ):

        if opportunity is None:
            return "No opportunity supplied."

        analysis = getattr(
            opportunity,
            "ai_analysis",
            None
        )

        lines = [
            f"Title: {getattr(opportunity, 'title', '')}",
            f"URL: {getattr(opportunity, 'url', '')}",
            f"Snippet: {getattr(opportunity, 'snippet', '')}",
            f"Rule Score: {getattr(opportunity, 'score', 0)}"
        ]

        if analysis is not None:

            lines.extend(
                [
                    (
                        "Category: "
                        f"{getattr(analysis, 'category', '')}"
                    ),
                    (
                        "Summary: "
                        f"{getattr(analysis, 'summary', '')}"
                    ),
                    (
                        "Recommended Action: "
                        f"{getattr(analysis, 'recommended_action', '')}"
                    )
                ]
            )

        return "\n".join(lines)