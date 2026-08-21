# 🌙✨ StorySpark AI

### An Autonomous AI Bedtime-Story Agent Built on AWS

> **A brand-new bedtime story, created and delivered automatically every evening — no prompt, button, or manual action required.**

**StorySpark AI** is an autonomous generative-AI application built for the **AWS Builder Center Weekend Creative Agent Challenge**.

Every evening, StorySpark wakes up automatically, creates a fresh creative direction, generates an original children's bedtime story, transforms it into a polished storybook-style email, and delivers it directly to the user's inbox.

---

## ✨ The Experience

Imagine opening your inbox at night and finding a completely new bedtime story already waiting for you.

No prompt.

No button.

No manual interaction.

StorySpark handles the entire creative workflow automatically.

```text
🌙 Scheduled Time Arrives
        ↓
🎨 StorySpark Creates a Daily Creative Seed
        ↓
🤖 Gemini Generates an Original Story
        ↓
⚙️ AWS Lambda Validates & Formats It
        ↓
📧 Amazon SES Delivers the Story
        ↓
✨ A New Bedtime Adventure Is Waiting
```

---

## 📖 Example Story Experience

Each StorySpark generation can include:

- 🌟 Original story title and subtitle
- 🧒 Child-friendly original characters
- 📚 Complete bedtime story
- 💛 Meaningful moral lesson
- 💬 Parent-child discussion question
- 🤝 Next-day kindness challenge
- 🎨 Illustration prompt
- 🌙 Bedtime thought
- ✉️ Beautiful storybook-style HTML email

---

## 🏗️ Architecture

![StorySpark AI AWS Architecture](docs/architecture/storyspark-aws-flow.png)

```text
Amazon EventBridge Scheduler
            │
            ▼
      AWS Lambda
   StorySpark Orchestrator
            │
            ├── Creates Daily Creative Seed
            ├── Builds Structured AI Prompt
            │
            ▼
   Gemini 3.5 Flash-Lite
            │
            ▼
      AWS Lambda
   Validate JSON + Build HTML
            │
            ▼
       Amazon SES
            │
            ▼
        📬 Inbox
```

### ☁️ AWS Services

| Service | Purpose |
|---|---|
| **Amazon EventBridge Scheduler** | Automatically starts StorySpark each evening |
| **AWS Lambda** | Orchestrates the complete story-generation workflow |
| **Amazon SES** | Delivers the finished storybook email |
| **Amazon CloudWatch** | Provides execution logs and operational evidence |

### 🤖 AI Service

**Gemini 3.5 Flash-Lite** generates the original story content using the creative prompt constructed by StorySpark.

> Gemini is used as an external AI generation service; orchestration, scheduling, validation, formatting, delivery, and monitoring are handled by the StorySpark application and AWS services.

---

# 🚀 How StorySpark Works

## 1️⃣ EventBridge Wakes Up StorySpark

Amazon EventBridge Scheduler automatically invokes the Lambda function at the configured time.

Example:

```text
Schedule: Daily
Time: 10:00 PM
Time zone: America/Denver
Target: AWS Lambda
Payload: {}
```

No user prompt is required.

---

## 2️⃣ StorySpark Creates Its Own Creative Direction

Instead of waiting for a user to provide a story idea, StorySpark generates its own daily creative seed.

The seed can contain:

```text
Theme
Setting
Hero Inspiration
Date
Weekday
```

This creates a new creative starting point for every execution.

---

## 3️⃣ Lambda Builds the AI Prompt

AWS Lambda converts the creative seed into a structured story-generation prompt.

The prompt asks Gemini to return structured JSON containing elements such as:

```text
Title
Characters
Story
Moral
Discussion Question
Kindness Challenge
Illustration Prompt
Bedtime Thought
```

---

## 4️⃣ Gemini Creates the Story

StorySpark sends the prompt to:

```text
Gemini 3.5 Flash-Lite
```

Gemini generates the original bedtime story and returns structured JSON.

---

## 5️⃣ Lambda Validates & Transforms the Response

The generated JSON is parsed and validated.

Lambda then transforms the content into a polished **HTML storybook email**.

---

## 6️⃣ Amazon SES Delivers the Story

Amazon SES sends the finished story to the configured recipient.

The result:

> 🌙 A fresh bedtime story is already waiting when the user returns in the evening.

---

# 🖼️ Proof of Execution

## ⏰ EventBridge Scheduler

![EventBridge Scheduler](docs/screenshots/02-eventbridge-schedule.png)

Demonstrates the recurring schedule, timezone, Lambda target, and scheduler state.

---

## ✅ Successful Lambda Execution

![Lambda Success](docs/screenshots/03-lambda-success-log.png)

CloudWatch execution evidence demonstrates that the StorySpark workflow completed successfully.

---

## 📧 Amazon SES

![SES Verified Identity](docs/screenshots/04-ses-verified-identity.png)

Shows the verified sender identity used by StorySpark.

---

## 🌙 Final StorySpark Email

![StorySpark Email](docs/screenshots/05-storyspark-email-output.png)

### The Final Result

A completely generated bedtime-story experience delivered automatically to the user's inbox.

---

# 💡 Why I Built StorySpark AI

Most generative-AI applications begin with the same interaction:

> A user types a prompt and presses a button.

I wanted StorySpark to work differently.

StorySpark has its **own recurring creative workflow**.

It wakes up on schedule, determines a creative direction, constructs its own AI-generation request, processes the response, creates the final experience, and delivers it automatically.

The result is not simply another chatbot response.

It is a small autonomous creative experience that is already complete when the user arrives.

---

# 🧠 What Makes StorySpark Autonomous?

StorySpark does more than call an AI model.

It independently performs a complete workflow:

```text
Schedule
   ↓
Create Creative Context
   ↓
Construct Prompt
   ↓
Generate Content
   ↓
Validate Structured Output
   ↓
Transform Content
   ↓
Deliver Result
   ↓
Record Execution Evidence
```

The user does not need to initiate each generation.

---

# 🛡️ Responsible Story Generation

The StorySpark prompt is designed to avoid:

- Copyrighted franchise characters
- Recognizable film or television characters
- Brand-based characters
- Graphic violence
- Frightening horror
- Adult themes
- Political content
- Religious persuasion

The goal is to create original, child-friendly bedtime stories suitable for family use.

---

# 📂 Project Structure

```text
StorySpark-AI/
│
├── README.md
├── lambda_function.py
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── docs/
│   ├── architecture/
│   │   └── storyspark-aws-flow.png
│   │
│   ├── screenshots/
│   │   ├── 01-lambda-function.png
│   │   ├── 02-eventbridge-schedule.png
│   │   ├── 03-lambda-success-log.png
│   │   ├── 04-ses-verified-identity.png
│   │   └── 05-storyspark-email-output.png
│   │
│   └── evidence/
│       ├── sample-execution-log.txt
│       └── sample-output.json
│
└── examples/
    └── sample-story.md
```

---

# ⚙️ Configuration

StorySpark uses environment variables for configuration.

Example:

```text
M9=<Gemini API key>
SENDER_EMAIL=<verified SES sender email>
RECIPIENT_EMAIL=<recipient email>
SES_REGION=us-east-1
TIMEZONE_NAME=America/Denver
```

The current implementation uses `M9` as the Gemini API-key environment-variable name.

A future cleanup could rename it to:

```text
GEMINI_API_KEY
```

---

# 🔐 Security

### Never commit real credentials to GitHub.

Do **not** upload:

```text
Gemini API keys
AWS access keys
AWS secret access keys
AWS session tokens
Passwords
.env files containing credentials
```

Recommended `.gitignore`:

```gitignore
.env
*.env
__pycache__/
*.pyc
.DS_Store
```

---

# 📧 Amazon SES Setup

The sender email address must be verified in Amazon SES.

```text
Amazon SES
    ↓
Verified identities
    ↓
Create identity
    ↓
Email address
    ↓
Verify email
```

For accounts still operating in the SES sandbox, recipient verification may also be required.

Successful status:

```text
Verified
```

---

# ⏰ EventBridge Scheduler Setup

Example configuration:

```text
Schedule type: Cron-based
Time zone: America/Denver
Time: 10:00 PM
Target: AWS Lambda
Lambda function: M9
Payload: {}
Flexible time window: Off
```

Cron expression:

```text
cron(0 22 * * ? *)
```

Because the scheduler timezone is configured as `America/Denver`, EventBridge can execute the workflow using Mountain Time.

---

# 🧪 Example Execution

```text
EventBridge triggers StorySpark
              ↓
Lambda creates today's creative seed
              ↓
Lambda constructs the AI prompt
              ↓
Gemini generates structured story JSON
              ↓
Lambda validates the response
              ↓
Lambda builds the HTML storybook
              ↓
Amazon SES sends the email
              ↓
🌙 A new bedtime story arrives
```

---

# 🧩 Challenges & Lessons Learned

Building StorySpark involved much more than connecting an application to a generative-AI model.

### Model Availability

An earlier Gemini model returned an availability error, requiring the application to be updated to a supported model.

### Lambda Execution Time

AI-generation requests can take longer than short default Lambda execution limits, so the Lambda timeout needed appropriate configuration.

### Amazon SES Permissions

Successful delivery required:

- Correct IAM permissions
- Verified SES identity
- Correct application configuration

### The Bigger Lesson

Autonomous AI is not only about generation.

A reliable AI workflow also requires:

**Scheduling + orchestration + structured output + validation + delivery + security + observability.**

---

# 🔮 Future Improvements

Future versions of StorySpark could include:

- 🎨 AI-generated story illustrations
- 🧠 Story history and memory
- 🧒 Personalized recurring characters
- 👨‍👩‍👧 Parent-controlled themes
- 🎂 Adjustable age ranges
- 🌍 Multi-language generation
- 🪣 Amazon S3 story storage
- 🗄️ DynamoDB story history
- 🌐 Web interface for previous stories
- 🚨 Advanced monitoring and failure notifications

---

# 🛠️ Built With

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Lambda](https://img.shields.io/badge/AWS-Lambda-orange)
![EventBridge](https://img.shields.io/badge/AWS-EventBridge-purple)
![SES](https://img.shields.io/badge/AWS-SES-red)
![Gemini](https://img.shields.io/badge/AI-Gemini-blue)

**Core technologies**

- AWS Lambda
- Amazon EventBridge Scheduler
- Amazon Simple Email Service
- Amazon CloudWatch
- Python
- Gemini 3.5 Flash-Lite API

---

# 🏆 AWS Builder Center Weekend Creative Agent Challenge

StorySpark AI was created for the:

### **AWS Builder Center Weekend Creative Agent Challenge**

Article:

```text
Weekend Creative Agent Challenge: StorySpark AI
```

Challenge tag:

```text
#agents
```

---

# ✅ Submission Evidence Checklist

Before final submission, verify that the repository contains:

- [ ] Working `lambda_function.py`
- [ ] Complete `README.md`
- [ ] Architecture diagram
- [ ] EventBridge Scheduler screenshot
- [ ] Successful Lambda execution evidence
- [ ] SES verified-identity screenshot
- [ ] Final StorySpark email screenshot
- [ ] Example generated story
- [ ] Sanitized JSON/output example
- [ ] No API keys or AWS credentials

---

# 👨‍💻 Author

**Lakshmanaprakash Murugesan**

---

## 🌙 StorySpark AI

### *A new story. A new adventure. Waiting every night.*

Built with ☁️ AWS + 🤖 Generative AI + ✨ a little bedtime magic.