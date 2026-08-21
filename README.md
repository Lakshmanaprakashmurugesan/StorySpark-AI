<div align="center">

# 🌙✨ StorySpark AI

### Autonomous AI Bedtime Stories — Created & Delivered Every Night

<br>

### Imagine • Create • Inspire

<br>

<img src="https://img.shields.io/badge/AWS-Cloud-232F3E?logo=amazonaws&logoColor=white" alt="AWS">
<img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/AWS-Lambda-FF9900?logo=awslambda&logoColor=white" alt="AWS Lambda">
<img src="https://img.shields.io/badge/AWS-EventBridge-8A2BE2?logo=amazonaws&logoColor=white" alt="Amazon EventBridge">
<img src="https://img.shields.io/badge/AWS-SES-DD344C?logo=amazonaws&logoColor=white" alt="Amazon SES">
<img src="https://img.shields.io/badge/Gemini-3.5_Flash--Lite-4285F4?logo=googlegemini&logoColor=white" alt="Gemini">

<br><br>

**A serverless creative AI agent that wakes up every evening, creates an original children's bedtime story, formats it as a storybook-style email, and delivers it automatically to the inbox.**

<br>

🏆 **AWS Builder Center Weekend Creative Agent Challenge**

</div>

---

## ✨ What Is StorySpark AI?

**StorySpark AI** is an autonomous bedtime-story generator built on AWS.

Every evening, the system automatically:

- 🎨 Creates a fresh creative seed
- 🤖 Generates an original children’s bedtime story
- ✅ Validates structured AI output
- 📖 Formats the story as a polished HTML storybook email
- 📧 Delivers it automatically to the recipient’s inbox

No button press.  
No manually entered prompt.  
No repeated user interaction.

The goal is simple:

> **When the user returns in the evening, a brand-new bedtime story is already waiting.**

---

## 🌙 Imagine • Create • Inspire

StorySpark is designed around three simple ideas:

### 💭 Imagine
Create a new creative direction every day using a theme, setting, date, weekday, and hero inspiration.

### ✨ Create
Generate an original, structured, child-friendly bedtime story using generative AI.

### 💛 Inspire
End each story with a meaningful moral, discussion question, kindness challenge, and bedtime thought.

---

## 🎬 StorySpark in Action

The final output is a complete storybook-style email delivered directly to the user.

![StorySpark Email](docs/screenshots/05-storyspark-email-output.png)

---

## 🚀 Autonomous Workflow

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
            ├── Generates Structured Story JSON
            ▼
      AWS Lambda
   Validate JSON + Build HTML
            │
            ▼
       Amazon SES
            │
            ▼
        📬 User Inbox
```

The workflow runs automatically on a recurring schedule.

### Example Schedule

```text
Time: 10:00 PM
Time zone: America/Denver
Target: AWS Lambda
EventBridge payload: {}
```

---

## 🏗️ AWS Architecture

![StorySpark AI AWS Architecture](docs/architecture/storyspark-aws-flow.png)

### AWS Services Used

| Service | Role |
|---|---|
| **Amazon EventBridge Scheduler** | Automatically triggers StorySpark every evening |
| **AWS Lambda** | Orchestrates story generation, validation, formatting, and delivery |
| **Amazon Simple Email Service (SES)** | Sends the finished storybook email |
| **Amazon CloudWatch Logs** | Provides execution logs for monitoring and troubleshooting |

### External AI Service

**Gemini 3.5 Flash-Lite** generates the original bedtime-story content from the creative prompt constructed by StorySpark AI.

> Gemini is an external AI service. Scheduling, orchestration, validation, formatting, delivery, and monitoring are handled by the StorySpark application and AWS services.

---

## 📖 What Each Story Can Include

Every generated story can contain:

- 🌟 Original story title and subtitle
- 🧒 Original child-friendly characters
- 📚 Complete bedtime story
- 💛 Meaningful moral lesson
- 💬 Parent-child discussion question
- 🤝 Next-day kindness challenge
- 🎨 Illustration prompt
- 🌙 Short bedtime thought
- ✉️ Storybook-style HTML formatting

The generation prompt is designed to avoid copyrighted franchise characters, recognizable movie or television characters, brands, graphic violence, frightening horror, adult themes, political content, and religious persuasion.

---

## ⚙️ How StorySpark Works

### 1️⃣ EventBridge Scheduler Starts the Workflow

Amazon EventBridge Scheduler automatically triggers the Lambda function at the configured time.

The EventBridge payload can simply be:

```json
{}
```

StorySpark does not depend on a manually entered theme because it creates its own daily creative seed.

---

### 2️⃣ Lambda Creates the Daily Creative Seed

The application selects values such as:

```text
Theme
Setting
Hero inspiration
Date
Weekday
```

These values give each run a different creative direction.

---

### 3️⃣ Lambda Builds the AI Prompt

Lambda transforms the daily creative seed into a structured story-generation prompt.

The prompt asks Gemini to return valid JSON containing elements such as:

```text
Title
Subtitle
Characters
Story paragraphs
Moral lesson
Discussion question
Kindness challenge
Illustration prompt
Bedtime thought
```

---

### 4️⃣ Gemini Generates the Story

The prompt is sent to:

```text
Gemini 3.5 Flash-Lite
```

Gemini generates the original bedtime story and returns structured JSON.

---

### 5️⃣ Lambda Validates and Formats the Result

AWS Lambda parses and validates the AI response.

It then transforms the content into a polished HTML storybook email.

---

### 6️⃣ Amazon SES Delivers the Story

Amazon SES sends the finished StorySpark email to the configured recipient.

The result:

> 🌙 **A fresh bedtime story is already waiting in the inbox.**

---

## 🧪 Live Deployment Evidence

### ⏰ EventBridge Scheduler

![EventBridge Scheduler](docs/screenshots/02-eventbridge-schedule.png)

**✓ Demonstrates the recurring schedule, timezone, Lambda target, and scheduler state.**

---

### ✅ Successful Lambda Execution

![Lambda Success](docs/screenshots/03-lambda-success-log.png)

**✓ CloudWatch execution evidence demonstrates that the StorySpark workflow completed successfully.**

---

### 📧 Amazon SES

![SES Verified Identity](docs/screenshots/04-ses-verified-identity.png)

**✓ Shows the verified sender identity used by StorySpark.**

---

### 🌙 Final StorySpark Email

![StorySpark Email](docs/screenshots/05-storyspark-email-output.png)

**✓ Demonstrates the final AI-generated bedtime story delivered to the recipient’s inbox.**

---

## 💡 Why I Built StorySpark AI

Many generative-AI applications wait for a user to type a prompt and press a button.

I wanted StorySpark to work differently.

Instead of waiting for a request, StorySpark has its own recurring creative workflow. It wakes up on schedule, creates a new creative direction for the day, generates the story, validates the structured output, formats the result, and delivers it automatically.

The result is not simply another chatbot response.

It is a small autonomous creative experience that is already complete when the user returns.

---

## 🤖 What Makes StorySpark Autonomous?

StorySpark independently performs an end-to-end workflow:

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

The user does not need to manually initiate each generation.

---

## 📂 Project Structure

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

## 🔧 Environment Variables

StorySpark uses environment variables for configuration.

Example:

```text
M9=<Gemini API key>
SENDER_EMAIL=<verified SES sender email>
RECIPIENT_EMAIL=<recipient email>
SES_REGION=us-east-1
TIMEZONE_NAME=America/Denver
```

In the current implementation, `M9` is the environment-variable name used for the Gemini API key.

A future cleanup can optionally rename it to:

```text
GEMINI_API_KEY
```

---

## 🔐 Security

### Never commit real secrets to GitHub.

Do **not** upload:

```text
Gemini API keys
AWS access keys
AWS secret access keys
AWS session tokens
Passwords
.env files containing real credentials
```

Recommended `.gitignore` entries:

```gitignore
.env
*.env
__pycache__/
*.pyc
.DS_Store
```

---

## 📧 Amazon SES Setup

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
Verify email from inbox
```

For testing in the SES sandbox, recipient verification may also be required.

Successful identity status:

```text
Verified
```

---

## ⏰ EventBridge Scheduler Setup

Example configuration:

```text
Schedule type: Cron-based schedule
Time zone: America/Denver
Time: 10:00 PM
Target: AWS Lambda
Lambda function: M9
Payload: {}
Flexible time window: Off
```

Example daily cron expression:

```text
cron(0 22 * * ? *)
```

Because the scheduler time zone is configured as `America/Denver`, EventBridge can apply the schedule using Mountain Time.

---

## 🔄 Example Execution Flow

```text
EventBridge automatically triggers StorySpark
                ↓
Lambda creates today's creative seed
                ↓
Lambda builds the story prompt
                ↓
Gemini generates structured story JSON
                ↓
Lambda validates the response
                ↓
Lambda builds the HTML storybook email
                ↓
Amazon SES sends the email
                ↓
🌙 A new bedtime story is waiting in the inbox
```

---

## 🧩 Challenges & Lessons Learned

Building StorySpark involved much more than calling a generative-AI model.

### Model Availability

An earlier Gemini model returned an availability error, so the application was updated to use Gemini 3.5 Flash-Lite.

### Lambda Execution Time

AI-generation requests can take longer than a short default Lambda timeout, so the Lambda timeout needed to be configured appropriately.

### Amazon SES Permissions

Successful email delivery required the correct IAM permissions and a verified SES identity.

### Key Lesson

The biggest lesson from the project was that autonomous AI is not only about generation.

A reliable autonomous workflow also requires:

**Scheduling + orchestration + structured output + validation + delivery + security + observability**

---

## 🔮 Future Improvements

Future versions of StorySpark could add:

- 🎨 AI-generated illustrations for each story
- 🧠 Story history and memory
- 🧒 Personalized recurring characters
- 👨‍👩‍👧 Parent-controlled themes
- 🎂 Adjustable age ranges
- 🌍 Multi-language stories
- 🪣 Amazon S3 story storage
- 🗄️ DynamoDB story history
- 🌐 Web interface for browsing previous stories
- 🚨 Advanced monitoring and failure notifications

---

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| **AWS Lambda** | Application orchestration |
| **Amazon EventBridge Scheduler** | Autonomous scheduling |
| **Amazon SES** | Email delivery |
| **Amazon CloudWatch** | Monitoring and logs |
| **Python** | Application logic |
| **Gemini 3.5 Flash-Lite** | Story generation |

---

## 🏆 AWS Builder Center Weekend Creative Agent Challenge

This project was created for the:

### **AWS Builder Center Weekend Creative Agent Challenge**

**Article title**

```text
Weekend Creative Agent Challenge: StorySpark AI
```

**Challenge tag**

```text
#agents
```

---

## 👨‍💻 Author

**Lakshmanaprakash Murugesan**

---

<div align="center">

## 🌙 StorySpark AI

### A new story. A new adventure. Waiting every night.

**Built with ☁️ AWS + 🤖 Generative AI + ✨ a little bedtime magic.**

</div>
