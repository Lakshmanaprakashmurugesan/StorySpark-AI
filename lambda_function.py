import os
import json
import urllib.request
import urllib.error
import boto3
import html
from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# STORYSPARK AI CONFIGURATION
# ============================================================

# Gemini API key stored in Lambda environment variable "M9"
GEMINI_API_KEY = os.environ["M9"].strip()

# Amazon SES emails
SENDER_EMAIL = os.environ["SENDER_EMAIL"].strip()
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"].strip()

# AWS Region
SES_REGION = os.environ.get(
    "SES_REGION",
    "us-east-1"
).strip()

# Local timezone
TIMEZONE_NAME = os.environ.get(
    "TIMEZONE_NAME",
    "America/Denver"
).strip()

LOCAL_TZ = ZoneInfo(TIMEZONE_NAME)

# Gemini model
GEMINI_MODEL = "gemini-3.5-flash-lite"

# Amazon SES client
ses = boto3.client(
    "ses",
    region_name=SES_REGION
)


# ============================================================
# DAILY STORY VARIETY
# ============================================================

THEMES = [
    "kindness",
    "courage",
    "patience",
    "honesty",
    "friendship",
    "empathy",
    "curiosity",
    "teamwork",
    "gratitude",
    "responsibility",
    "perseverance",
    "sharing"
]

SETTINGS = [
    "a moonlit forest",
    "a floating island above the clouds",
    "a tiny seaside village",
    "a magical garden",
    "a quiet mountain valley",
    "a colorful town of inventors",
    "a hidden woodland library",
    "a lighthouse beside a sparkling ocean",
    "a village beneath the stars",
    "a whimsical train traveling through dreamland",
    "a peaceful farm surrounded by fireflies",
    "a secret valley filled with glowing flowers"
]

HERO_TYPES = [
    "a curious little fox",
    "a gentle young elephant",
    "a brave little rabbit",
    "a thoughtful young owl",
    "a playful red panda",
    "a tiny adventurous turtle",
    "a kind little bear",
    "a curious young squirrel",
    "a cheerful little penguin",
    "a shy young deer",
    "a clever little hedgehog",
    "a friendly young otter"
]


def get_story_seed():

    now = datetime.now(LOCAL_TZ)

    day_number = now.timetuple().tm_yday

    theme = THEMES[
        day_number % len(THEMES)
    ]

    setting = SETTINGS[
        (day_number * 3) % len(SETTINGS)
    ]

    hero = HERO_TYPES[
        (day_number * 5) % len(HERO_TYPES)
    ]

    return {
        "date": now.strftime("%B %d, %Y"),
        "weekday": now.strftime("%A"),
        "theme": theme,
        "setting": setting,
        "hero": hero
    }


# ============================================================
# BUILD GEMINI STORY PROMPT
# ============================================================

def build_story_prompt(seed):

    return f"""
You are StorySpark AI.

You are an autonomous children's bedtime-story creator.

Every evening, your job is to create a completely NEW,
warm, imaginative children's story that teaches a meaningful
life lesson without sounding preachy.

Today's date:
{seed["date"]}

Today is:
{seed["weekday"]}

TODAY'S CREATIVE SEED

Moral theme:
{seed["theme"]}

Suggested setting:
{seed["setting"]}

Suggested hero inspiration:
{seed["hero"]}


TARGET AUDIENCE

Children approximately 5 to 9 years old.


STORY REQUIREMENTS

Create an ORIGINAL bedtime story approximately 650 to 850 words.

The story should:

1. Have an original title.
2. Introduce memorable original characters.
3. Begin with an engaging opening.
4. Include a gentle problem, mystery, challenge, or adventure.
5. Allow the main character to make meaningful choices.
6. Include emotional warmth.
7. Include imagination and wonder.
8. Resolve the challenge naturally.
9. Demonstrate today's moral theme through the story.
10. End in a comforting bedtime-friendly way.

The moral should come from what happens in the story.

Do NOT make the story feel like a lecture.


SAFETY AND ORIGINALITY RULES

- Create completely original characters.
- Do not use copyrighted franchise characters.
- Do not imitate famous children's books.
- Do not use recognizable movie or television characters.
- Do not mention brands.
- Do not include graphic violence.
- Do not include frightening horror.
- Do not include adult themes.
- Do not include political content.
- Do not include religious persuasion.
- Keep conflict gentle and child-appropriate.
- Make the ending hopeful and emotionally satisfying.
- Never say that you are an AI.
- Never mention this prompt.
- Never mention these instructions.


AFTER THE STORY CREATE:

1. A short moral lesson.
2. One parent-child discussion question.
3. One small kindness/action challenge for tomorrow.
4. One detailed illustration prompt describing a beautiful
   children's-book scene from the story.
5. One gentle bedtime thought.


OUTPUT FORMAT

Return ONLY valid JSON.

Do NOT use Markdown code fences.

Use exactly this structure:

{{
  "title": "Story title",
  "subtitle": "Short magical subtitle",
  "age_range": "5-9",
  "reading_time": "5-7 minutes",
  "theme": "{seed["theme"]}",
  "hero_emoji": "one appropriate emoji",
  "characters": [
    {{
      "name": "Character name",
      "description": "Short child-friendly description"
    }}
  ],
  "story_paragraphs": [
    "Paragraph 1",
    "Paragraph 2",
    "Paragraph 3"
  ],
  "moral_title": "Short name for tonight's lesson",
  "moral": "Clear but warm moral lesson",
  "discussion_question": "One thoughtful parent-child question",
  "kindness_challenge": "One small action the child can try tomorrow",
  "illustration_prompt": "Detailed children's-book illustration prompt",
  "bedtime_thought": "One short comforting bedtime thought"
}}

IMPORTANT:

The story_paragraphs list should contain approximately
10 to 14 natural paragraphs.

Make tonight's story feel special, imaginative,
emotionally warm, and different from a generic AI story.
"""


# ============================================================
# CALL GEMINI API
# ============================================================

def call_gemini(prompt):

    endpoint = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent"
    )

    print(
        f"Using Gemini model: {GEMINI_MODEL}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 3000
        }
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(
            payload
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:

        error_message = (
            error.read().decode("utf-8")
        )

        print(
            "==================================="
        )

        print(
            "GEMINI API ERROR"
        )

        print(
            f"HTTP Status: {error.code}"
        )

        print(
            error_message
        )

        print(
            "==================================="
        )

        raise Exception(
            f"Gemini API HTTP "
            f"{error.code}: {error_message}"
        )

    except urllib.error.URLError as error:

        raise Exception(
            f"Could not connect to Gemini: {error}"
        )

    candidates = result.get(
        "candidates",
        []
    )

    if not candidates:

        raise Exception(
            "Gemini returned no candidates. "
            f"Response: {json.dumps(result)}"
        )

    parts = (
        candidates[0]
        .get("content", {})
        .get("parts", [])
    )

    generated_text = "\n".join(
        part.get("text", "")
        for part in parts
        if part.get("text")
    ).strip()

    if not generated_text:

        raise Exception(
            "Gemini returned no story text."
        )

    return generated_text


# ============================================================
# PARSE GEMINI JSON
# ============================================================

def parse_story_json(raw_text):

    cleaned = raw_text.strip()

    # Remove Markdown fences if Gemini accidentally uses them
    if cleaned.startswith("```"):

        first_newline = cleaned.find("\n")

        if first_newline != -1:
            cleaned = cleaned[
                first_newline + 1:
            ]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

    # Extract first JSON object if extra text appears
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace == -1 or last_brace == -1:

        raise Exception(
            "Gemini did not return valid JSON."
        )

    cleaned = cleaned[
        first_brace:
        last_brace + 1
    ]

    try:

        story = json.loads(
            cleaned
        )

    except json.JSONDecodeError as error:

        print(
            "RAW GEMINI RESPONSE:"
        )

        print(
            raw_text
        )

        raise Exception(
            f"Could not parse Gemini story JSON: {error}"
        )

    required_fields = [
        "title",
        "subtitle",
        "theme",
        "story_paragraphs",
        "moral",
        "discussion_question",
        "kindness_challenge",
        "illustration_prompt",
        "bedtime_thought"
    ]

    for field in required_fields:

        if field not in story:

            raise Exception(
                f"Story JSON missing field: {field}"
            )

    # Normalize story paragraphs
    if isinstance(
        story["story_paragraphs"],
        str
    ):

        story["story_paragraphs"] = [
            paragraph.strip()
            for paragraph in
            story["story_paragraphs"].split("\n\n")
            if paragraph.strip()
        ]

    # Normalize characters
    if not isinstance(
        story.get("characters", []),
        list
    ):

        story["characters"] = []

    story.setdefault(
        "hero_emoji",
        "✨"
    )

    story.setdefault(
        "age_range",
        "5-9"
    )

    story.setdefault(
        "reading_time",
        "5-7 minutes"
    )

    story.setdefault(
        "moral_title",
        "Tonight's Lesson"
    )

    return story


# ============================================================
# HTML HELPERS
# ============================================================

def safe(value):

    return html.escape(
        str(value)
    )


def build_character_cards(characters):

    if not characters:

        return ""

    cards = ""

    for character in characters:

        if isinstance(
            character,
            dict
        ):

            name = safe(
                character.get(
                    "name",
                    "Story Friend"
                )
            )

            description = safe(
                character.get(
                    "description",
                    ""
                )
            )

        else:

            name = safe(
                character
            )

            description = ""

        cards += f"""
        <tr>
            <td style="
                padding:0 0 10px 0;
            ">
                <table
                    role="presentation"
                    width="100%"
                    cellpadding="0"
                    cellspacing="0"
                >
                    <tr>
                        <td style="
                            background:#fff7ed;
                            border:1px solid #fed7aa;
                            border-radius:14px;
                            padding:14px 16px;
                        ">
                            <div style="
                                font-family:Arial,Helvetica,sans-serif;
                                color:#9a3412;
                                font-size:15px;
                                font-weight:800;
                                margin-bottom:4px;
                            ">
                                ⭐ {name}
                            </div>

                            <div style="
                                font-family:Arial,Helvetica,sans-serif;
                                color:#7c2d12;
                                font-size:13px;
                                line-height:1.6;
                            ">
                                {description}
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        """

    return cards


def build_story_paragraphs(paragraphs):

    result = ""

    for index, paragraph in enumerate(
        paragraphs,
        start=1
    ):

        text = safe(
            paragraph
        )

        # Add decorative separator every few paragraphs
        if index > 1 and index % 4 == 0:

            result += """
            <div style="
                text-align:center;
                color:#c4b5fd;
                font-size:18px;
                letter-spacing:8px;
                padding:5px 0 12px 0;
            ">
                ✦ ✦ ✦
            </div>
            """

        result += f"""
        <p style="
            margin:0 0 18px 0;
            font-family:Georgia,'Times New Roman',serif;
            color:#334155;
            font-size:17px;
            line-height:1.85;
        ">
            {text}
        </p>
        """

    return result


# ============================================================
# BUILD PREMIUM STORYBOOK HTML EMAIL
# ============================================================

def build_html_email(
    story,
    seed
):

    title = safe(
        story["title"]
    )

    subtitle = safe(
        story["subtitle"]
    )

    theme = safe(
        story["theme"]
    )

    hero_emoji = safe(
        story.get(
            "hero_emoji",
            "✨"
        )
    )

    age_range = safe(
        story.get(
            "age_range",
            "5-9"
        )
    )

    reading_time = safe(
        story.get(
            "reading_time",
            "5-7 minutes"
        )
    )

    moral_title = safe(
        story.get(
            "moral_title",
            "Tonight's Lesson"
        )
    )

    moral = safe(
        story["moral"]
    )

    discussion_question = safe(
        story["discussion_question"]
    )

    kindness_challenge = safe(
        story["kindness_challenge"]
    )

    illustration_prompt = safe(
        story["illustration_prompt"]
    )

    bedtime_thought = safe(
        story["bedtime_thought"]
    )

    characters_html = (
        build_character_cards(
            story.get(
                "characters",
                []
            )
        )
    )

    paragraphs_html = (
        build_story_paragraphs(
            story["story_paragraphs"]
        )
    )

    date_text = safe(
        seed["date"]
    )

    weekday = safe(
        seed["weekday"]
    )

    html_email = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
{title}
</title>

</head>


<body
    style="
        margin:0;
        padding:0;
        background:#090b1a;
    "
>


<!-- Hidden email preview text -->

<div
    style="
        display:none;
        max-height:0;
        overflow:hidden;
        opacity:0;
        color:transparent;
    "
>
Tonight's StorySpark adventure:
{title}
</div>


<table
    role="presentation"
    width="100%"
    cellpadding="0"
    cellspacing="0"
    bgcolor="#090b1a"
    style="
        width:100%;
        background:#090b1a;
    "
>

<tr>

<td
    align="center"
    style="
        padding:30px 12px;
    "
>


<table
    role="presentation"
    width="100%"
    cellpadding="0"
    cellspacing="0"
    style="
        max-width:680px;
    "
>


<!-- ====================================================== -->
<!-- NIGHT SKY HEADER -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#312e81"
    style="
        background:
            linear-gradient(
                145deg,
                #172554 0%,
                #312e81 36%,
                #6d28d9 72%,
                #9333ea 100%
            );
        border-radius:28px;
        padding:36px 30px 38px 30px;
        text-align:center;
        color:#ffffff;
    "
>

<div style="
    font-size:21px;
    letter-spacing:10px;
    color:#fde68a;
    margin-bottom:15px;
">
    ✦ ⭐ ✦ 🌙 ✦ ⭐ ✦
</div>


<div style="
    display:inline-block;
    background:rgba(255,255,255,0.14);
    border:1px solid rgba(255,255,255,0.25);
    border-radius:30px;
    padding:8px 14px;
    font-family:Arial,Helvetica,sans-serif;
    color:#ffffff;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.5px;
    margin-bottom:19px;
">
    🌙 YOUR AUTONOMOUS BEDTIME STORY
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#ddd6fe;
    font-size:15px;
    font-weight:700;
    margin-bottom:8px;
">
    StorySpark AI presents
</div>


<div style="
    font-size:58px;
    line-height:1;
    margin-bottom:13px;
">
    {hero_emoji}
</div>


<div style="
    font-family:Georgia,'Times New Roman',serif;
    color:#ffffff;
    font-size:35px;
    line-height:1.2;
    font-weight:800;
    margin-bottom:10px;
">
    {title}
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#ede9fe;
    font-size:16px;
    line-height:1.6;
    font-style:italic;
">
    {subtitle}
</div>


<div style="
    margin-top:22px;
    font-family:Arial,Helvetica,sans-serif;
    color:#ddd6fe;
    font-size:11px;
    font-weight:700;
    letter-spacing:0.7px;
">
    {weekday.upper()} • {date_text}
</div>

</td>

</tr>


<tr>
<td height="18"></td>
</tr>


<!-- ====================================================== -->
<!-- STORY INFO -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#ffffff"
    style="
        background:#ffffff;
        border-radius:18px;
        padding:20px;
    "
>

<table
    role="presentation"
    width="100%"
    cellpadding="0"
    cellspacing="0"
>

<tr>

<td
    align="center"
    style="
        width:33%;
        padding:8px;
    "
>

<div style="
    font-size:22px;
">
    👧
</div>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#64748b;
    font-size:10px;
    font-weight:800;
    letter-spacing:1px;
">
    AGES
</div>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#111827;
    font-size:14px;
    font-weight:800;
">
    {age_range}
</div>

</td>


<td
    align="center"
    style="
        width:33%;
        padding:8px;
        border-left:1px solid #e2e8f0;
        border-right:1px solid #e2e8f0;
    "
>

<div style="
    font-size:22px;
">
    ⏱️
</div>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#64748b;
    font-size:10px;
    font-weight:800;
    letter-spacing:1px;
">
    READING TIME
</div>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#111827;
    font-size:14px;
    font-weight:800;
">
    {reading_time}
</div>

</td>


<td
    align="center"
    style="
        width:33%;
        padding:8px;
    "
>

<div style="
    font-size:22px;
">
    ❤️
</div>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#64748b;
    font-size:10px;
    font-weight:800;
    letter-spacing:1px;
">
    TONIGHT'S THEME
</div>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#111827;
    font-size:14px;
    font-weight:800;
    text-transform:capitalize;
">
    {theme}
</div>

</td>

</tr>

</table>

</td>

</tr>


<tr>
<td height="18"></td>
</tr>


<!-- ====================================================== -->
<!-- MEET THE CHARACTERS -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#fef3c7"
    style="
        background:#fef3c7;
        border-radius:18px;
        padding:23px;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#92400e;
    font-size:12px;
    font-weight:900;
    letter-spacing:1.4px;
    margin-bottom:14px;
">
    ✨ MEET TONIGHT'S STORY FRIENDS
</div>


<table
    role="presentation"
    width="100%"
    cellpadding="0"
    cellspacing="0"
>

{characters_html}

</table>

</td>

</tr>


<tr>
<td height="18"></td>
</tr>


<!-- ====================================================== -->
<!-- STORY -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#fffdf8"
    style="
        background:#fffdf8;
        border-radius:22px;
        padding:32px 28px;
        border:1px solid #f1e9dc;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#7c3aed;
    font-size:11px;
    font-weight:900;
    letter-spacing:1.5px;
    text-align:center;
    margin-bottom:8px;
">
    📖 TONIGHT'S ADVENTURE
</div>


<div style="
    text-align:center;
    font-family:Georgia,'Times New Roman',serif;
    color:#1e293b;
    font-size:27px;
    font-weight:800;
    margin-bottom:26px;
">
    {title}
</div>


{paragraphs_html}


<div style="
    text-align:center;
    font-size:22px;
    letter-spacing:8px;
    color:#c4b5fd;
    padding-top:4px;
">
    ✦ 🌙 ✦
</div>

</td>

</tr>


<tr>
<td height="18"></td>
</tr>


<!-- ====================================================== -->
<!-- MORAL -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#ecfdf5"
    style="
        background:#ecfdf5;
        border-left:5px solid #10b981;
        border-radius:18px;
        padding:24px;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#047857;
    font-size:11px;
    font-weight:900;
    letter-spacing:1.3px;
    margin-bottom:8px;
">
    ❤️ TONIGHT'S LITTLE LESSON
</div>


<div style="
    font-family:Georgia,'Times New Roman',serif;
    color:#064e3b;
    font-size:21px;
    font-weight:800;
    margin-bottom:10px;
">
    {moral_title}
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#065f46;
    font-size:15px;
    line-height:1.75;
">
    {moral}
</div>

</td>

</tr>


<tr>
<td height="16"></td>
</tr>


<!-- ====================================================== -->
<!-- TALK ABOUT IT -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#eff6ff"
    style="
        background:#eff6ff;
        border-left:5px solid #3b82f6;
        border-radius:18px;
        padding:24px;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#1d4ed8;
    font-size:11px;
    font-weight:900;
    letter-spacing:1.3px;
    margin-bottom:10px;
">
    💬 TALK ABOUT IT TOGETHER
</div>


<div style="
    font-family:Georgia,'Times New Roman',serif;
    color:#1e3a8a;
    font-size:19px;
    line-height:1.6;
    font-style:italic;
">
    “{discussion_question}”
</div>

</td>

</tr>


<tr>
<td height="16"></td>
</tr>


<!-- ====================================================== -->
<!-- TOMORROW CHALLENGE -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#fff7ed"
    style="
        background:#fff7ed;
        border-left:5px solid #f97316;
        border-radius:18px;
        padding:24px;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#c2410c;
    font-size:11px;
    font-weight:900;
    letter-spacing:1.3px;
    margin-bottom:10px;
">
    🌞 TOMORROW'S LITTLE CHALLENGE
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#9a3412;
    font-size:15px;
    line-height:1.75;
">
    {kindness_challenge}
</div>

</td>

</tr>


<tr>
<td height="16"></td>
</tr>


<!-- ====================================================== -->
<!-- PICTURE THIS -->
<!-- ====================================================== -->

<tr>

<td
    style="
        background:
            linear-gradient(
                135deg,
                #fdf4ff,
                #fae8ff,
                #ede9fe
            );
        border-radius:18px;
        padding:25px;
    "
>

<div style="
    text-align:center;
    font-size:37px;
    margin-bottom:8px;
">
    🎨✨
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#7e22ce;
    font-size:11px;
    font-weight:900;
    letter-spacing:1.3px;
    text-align:center;
    margin-bottom:12px;
">
    PICTURE TONIGHT'S MAGICAL SCENE
</div>


<div style="
    font-family:Georgia,'Times New Roman',serif;
    color:#581c87;
    font-size:16px;
    line-height:1.75;
    text-align:center;
    font-style:italic;
">
    {illustration_prompt}
</div>

</td>

</tr>


<tr>
<td height="18"></td>
</tr>


<!-- ====================================================== -->
<!-- BEDTIME THOUGHT -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#172554"
    style="
        background:#172554;
        border-radius:20px;
        padding:28px;
        text-align:center;
    "
>

<div style="
    color:#fde68a;
    font-size:24px;
    margin-bottom:10px;
">
    🌙 ✦ ⭐
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#a5b4fc;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.5px;
    margin-bottom:10px;
">
    ONE LAST THOUGHT BEFORE SLEEP
</div>


<div style="
    font-family:Georgia,'Times New Roman',serif;
    color:#ffffff;
    font-size:19px;
    line-height:1.7;
    font-style:italic;
">
    “{bedtime_thought}”
</div>

</td>

</tr>


<tr>
<td height="18"></td>
</tr>


<!-- ====================================================== -->
<!-- AUTONOMY / COMPETITION PROOF -->
<!-- ====================================================== -->

<tr>

<td
    bgcolor="#111827"
    style="
        background:#111827;
        border:1px solid #293548;
        border-radius:18px;
        padding:22px;
        text-align:center;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#c4b5fd;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.5px;
    margin-bottom:9px;
">
    ⚡ CREATED AUTONOMOUSLY
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#ffffff;
    font-size:14px;
    font-weight:700;
    line-height:1.7;
">
    Schedule
    &nbsp; → &nbsp;
    StorySpark AI
    &nbsp; → &nbsp;
    New Story
    &nbsp; → &nbsp;
    Your Inbox
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#64748b;
    font-size:11px;
    line-height:1.6;
    margin-top:8px;
">
    No button press required.
    A new story is created while you're away.
</div>

</td>

</tr>


<!-- ====================================================== -->
<!-- FOOTER -->
<!-- ====================================================== -->

<tr>

<td
    style="
        padding:34px 20px 12px 20px;
        text-align:center;
    "
>

<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#ffffff;
    font-size:22px;
    font-weight:900;
    margin-bottom:8px;
">
    🌙 StorySpark AI
</div>


<div style="
    font-family:Arial,Helvetica,sans-serif;
    color:#94a3b8;
    font-size:12px;
    line-height:1.8;
">
    A new little adventure,
    ready when you return.

    <br>

    Built with AWS Lambda + Gemini + Amazon SES

    <br>

    ✨ Sweet dreams ✨
</div>

</td>

</tr>


</table>

</td>

</tr>

</table>


</body>

</html>
"""

    return html_email


# ============================================================
# BUILD PLAIN TEXT FALLBACK
# ============================================================

def build_plain_text(
    story,
    seed
):

    character_lines = []

    for character in story.get(
        "characters",
        []
    ):

        if isinstance(
            character,
            dict
        ):

            character_lines.append(
                f"- {character.get('name', '')}: "
                f"{character.get('description', '')}"
            )

    story_text = "\n\n".join(
        story["story_paragraphs"]
    )

    return f"""
🌙 STORYSPARK AI

{seed["date"]}

{story["hero_emoji"]} {story["title"]}

{story["subtitle"]}

Theme: {story["theme"]}
Ages: {story["age_range"]}
Reading Time: {story["reading_time"]}


✨ CHARACTERS

{chr(10).join(character_lines)}


📖 TONIGHT'S STORY

{story_text}


❤️ TONIGHT'S LESSON

{story["moral_title"]}

{story["moral"]}


💬 TALK ABOUT IT

{story["discussion_question"]}


🌞 TOMORROW'S LITTLE CHALLENGE

{story["kindness_challenge"]}


🎨 PICTURE THIS

{story["illustration_prompt"]}


🌙 BEDTIME THOUGHT

{story["bedtime_thought"]}


StorySpark AI
Generated autonomously with
AWS Lambda + Gemini + Amazon SES.
""".strip()


# ============================================================
# SEND STORY THROUGH AMAZON SES
# ============================================================

def send_story_email(
    story,
    seed
):

    subject = (
        f"🌙 Tonight's StorySpark | "
        f"{story['title']}"
    )

    html_body = build_html_email(
        story,
        seed
    )

    plain_text = build_plain_text(
        story,
        seed
    )

    print(
        f"Sending StorySpark from: "
        f"{SENDER_EMAIL}"
    )

    print(
        f"Sending StorySpark to: "
        f"{RECIPIENT_EMAIL}"
    )

    response = ses.send_email(

        Source=SENDER_EMAIL,

        Destination={
            "ToAddresses": [
                RECIPIENT_EMAIL
            ]
        },

        Message={

            "Subject": {
                "Data": subject,
                "Charset": "UTF-8"
            },

            "Body": {

                "Text": {
                    "Data": plain_text,
                    "Charset": "UTF-8"
                },

                "Html": {
                    "Data": html_body,
                    "Charset": "UTF-8"
                }

            }

        }

    )

    return response[
        "MessageId"
    ]


# ============================================================
# AWS LAMBDA ENTRY POINT
# ============================================================

def lambda_handler(
    event,
    context
):

    try:

        print("")
        print(
            "======================================"
        )
        print(
            "StorySpark AI execution started"
        )
        print(
            "======================================"
        )

        # ----------------------------------------------------
        # STEP 1
        # Build today's creative seed
        # ----------------------------------------------------

        print("")
        print(
            "Step 1: Creating today's story seed..."
        )

        seed = get_story_seed()

        print(
            f"Date: {seed['date']}"
        )

        print(
            f"Theme: {seed['theme']}"
        )

        print(
            f"Setting: {seed['setting']}"
        )

        print(
            f"Hero inspiration: {seed['hero']}"
        )

        # ----------------------------------------------------
        # STEP 2
        # Build Gemini prompt
        # ----------------------------------------------------

        print("")
        print(
            "Step 2: Building bedtime-story prompt..."
        )

        prompt = build_story_prompt(
            seed
        )

        print(
            "Story prompt created."
        )

        # ----------------------------------------------------
        # STEP 3
        # Generate story
        # ----------------------------------------------------

        print("")
        print(
            "Step 3: Asking Gemini to create tonight's story..."
        )

        raw_story = call_gemini(
            prompt
        )

        print(
            "Gemini story generated."
        )

        # ----------------------------------------------------
        # STEP 4
        # Parse structured story
        # ----------------------------------------------------

        print("")
        print(
            "Step 4: Parsing StorySpark output..."
        )

        story = parse_story_json(
            raw_story
        )

        print(
            f"Story title: {story['title']}"
        )

        print(
            f"Story theme: {story['theme']}"
        )

        # ----------------------------------------------------
        # SHOW ACTUAL STORY IN LOGS
        # ----------------------------------------------------

        print("")
        print(
            "======================================"
        )
        print(
            "ACTUAL STORYSPARK OUTPUT"
        )
        print(
            "======================================"
        )

        print(
            json.dumps(
                story,
                ensure_ascii=False,
                indent=2
            )
        )

        print(
            "======================================"
        )
        print(
            "END STORYSPARK OUTPUT"
        )
        print(
            "======================================"
        )

        # ----------------------------------------------------
        # STEP 5
        # Send premium bedtime-story email
        # ----------------------------------------------------

        print("")
        print(
            "Step 5: Sending storybook email through SES..."
        )

        message_id = send_story_email(
            story,
            seed
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print("")
        print(
            "======================================"
        )
        print(
            "STORYSPARK SUCCESS!"
        )
        print(
            "======================================"
        )

        print(
            f"Story: {story['title']}"
        )

        print(
            f"SES Message ID: {message_id}"
        )

        print(
            f"Email sent to: {RECIPIENT_EMAIL}"
        )

        print(
            "======================================"
        )

        return {

            "statusCode": 200,

            "body": json.dumps(
                {

                    "message":
                        "StorySpark generated and "
                        "emailed successfully.",

                    "story_title":
                        story["title"],

                    "theme":
                        story["theme"],

                    "gemini_model":
                        GEMINI_MODEL,

                    "ses_message_id":
                        message_id,

                    "actual_story":
                        story

                },

                ensure_ascii=False
            )
        }

    except Exception as error:

        print("")
        print(
            "======================================"
        )
        print(
            "STORYSPARK EXECUTION FAILED"
        )
        print(
            "======================================"
        )

        print(
            str(error)
        )

        print(
            "======================================"
        )

        return {

            "statusCode": 500,

            "body": json.dumps(
                {

                    "message":
                        "StorySpark failed.",

                    "error":
                        str(error)

                },

                ensure_ascii=False
            )
        }