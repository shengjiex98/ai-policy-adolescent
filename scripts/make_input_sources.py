# /// script
# requires-python = ">=3.11"
# ///
"""Generate data/input_sources.csv seeded with official sources for
Anthropic, OpenAI, and Google DeepMind (V1 scope)."""

import csv
from pathlib import Path

COLUMNS = [
    "source_name",
    "source_url",
    "enabled",
    "company_hint",
    "platform_hint",
    "source_tier",
    "source_type_hint",
    "date_filter_start",
    "scrape_depth",
    "notes",
]

SOURCES = [
    # --- OpenAI / ChatGPT ---
    ("ChatGPT Release Notes", "https://help.openai.com/en/articles/6825453-chatgpt-release-notes",
     "TRUE", "OpenAI", "ChatGPT", "official", "release_notes", "2023-01-01", "single_page",
     "Scan for safety, teen, parental control, memory, and crisis-related entries"),
    ("OpenAI Usage Policies", "https://openai.com/policies/usage-policies",
     "TRUE", "OpenAI", "ChatGPT", "official", "usage_policy", "2023-01-01", "single_page",
     "Current policy baseline; note update dates if stated"),
    ("OpenAI Parental Controls FAQ", "https://help.openai.com/en/articles/12315553-parental-controls-faq",
     "TRUE", "OpenAI", "ChatGPT", "official", "help_center", "2023-01-01", "single_page", ""),
    ("OpenAI Teen Safety Blog Post", "https://openai.com/index/teen-safety-freedom-and-privacy/",
     "TRUE", "OpenAI", "ChatGPT", "official", "blog_post", "2023-01-01", "single_page", ""),
    ("OpenAI Introducing Parental Controls", "https://openai.com/index/introducing-parental-controls/",
     "TRUE", "OpenAI", "ChatGPT", "official", "blog_post", "2023-01-01", "single_page", ""),
    ("OpenAI Age Prediction Help", "https://help.openai.com/en/articles/12652064-age-prediction-in-chatgpt",
     "TRUE", "OpenAI", "ChatGPT", "official", "help_center", "2023-01-01", "single_page", ""),
    # --- Anthropic / Claude ---
    ("Anthropic News", "https://www.anthropic.com/news",
     "TRUE", "Anthropic", "Claude", "official", "blog_post", "2023-01-01", "follow_same_domain_links",
     "Follow links only for safety-, teen-, privacy-, or wellbeing-relevant posts"),
    ("Anthropic Usage Policy", "https://www.anthropic.com/legal/aup",
     "TRUE", "Anthropic", "Claude", "official", "usage_policy", "2023-01-01", "single_page",
     "Minimum age and mental-health-related use restrictions"),
    ("Anthropic Protecting User Wellbeing", "https://www.anthropic.com/news/protecting-well-being-of-users",
     "TRUE", "Anthropic", "Claude", "official", "blog_post", "2023-01-01", "single_page", ""),
    ("Anthropic Privacy Policy", "https://www.anthropic.com/legal/privacy",
     "TRUE", "Anthropic", "Claude", "official", "privacy_policy", "2023-01-01", "single_page",
     "Retention, training data use, minors"),
    # --- Google DeepMind / Gemini ---
    ("Google Gemini Blog", "https://blog.google/products/gemini/",
     "TRUE", "Google", "Gemini", "official", "blog_post", "2023-01-01", "follow_same_domain_links",
     "Follow links only for teen-, safety-, or privacy-relevant posts"),
    ("Gemini Apps Privacy Hub", "https://support.google.com/gemini/answer/13594961",
     "TRUE", "Google", "Gemini", "official", "privacy_policy", "2023-01-01", "single_page",
     "Retention, human review, training data use"),
    ("Gemini for Children Guide (Family Link)", "https://support.google.com/gemini/answer/16109150",
     "TRUE", "Google", "Gemini", "official", "help_center", "2023-01-01", "single_page",
     "Supervised under-13 access via Family Link"),
    ("Google Bard for Teens Blog Post", "https://blog.google/products/gemini/google-bard-expansion-teens/",
     "TRUE", "Google", "Gemini", "official", "blog_post", "2023-01-01", "single_page",
     "2023 teen expansion of Bard (Gemini predecessor)"),
    ("Google Built-in Protections for Kids and Teens", "https://blog.google/technology/families/google-new-built-in-protections-kids-teens/",
     "TRUE", "Google", "Gemini", "official", "blog_post", "2023-01-01", "single_page", ""),
]


def main() -> None:
    out_path = Path(__file__).resolve().parent.parent / "data" / "input_sources.csv"
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(SOURCES)
    print(f"Wrote {len(SOURCES)} sources to {out_path}")


if __name__ == "__main__":
    main()
