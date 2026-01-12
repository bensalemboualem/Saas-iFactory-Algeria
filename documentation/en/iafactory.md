# IAFactory – Multi‑model Platform Algeria/CH

## Introduction
IAFactory centralizes access to several AI models (GPT, Claude, Gemini, Mistral, DeepSeek, etc.) in a single web interface.
The goal is to reduce friction: one space to chat, search, generate content, and manage your AI projects without switching tools each time.
The platform is designed for small businesses, freelancers, students, and schools in Algeria and Switzerland.
Supported languages: French, Arabic (darija, amazigh), and English (to be specified according to actual implementation).

## Getting Started

### 1. Create an Account
- Go to the IAFactory Algeria website and click on “Create an account” or equivalent.
- Enter your email, password, and complete the registration (exact process to be specified if SSO or SMS is used).
- Access your IAFactory space with the main dashboard (chat, assistants, possibly applications).

### 2. Ask Your First Question
- Open the chat area from the dashboard.
- Type your question as text, or add files if the interface allows (PDF, images, etc.).
- Let IAFactory choose a default model or manually select one (GPT, Claude, Gemini, Mistral, DeepSeek, etc.) from the available list.

### 3. Read and Refine the Answer
- Read the generated answer in your preferred language (if language detection and selection are enabled in the UI).
- If needed, ask a follow-up question for clarification or request a simpler, shorter, or more technical reformulation.
- Use copy, export, or save options if available in the interface (to be specified for V1).

## Reprompt & Multi‑models

### Principle
- Reprompting allows you to send the same question to another model without rewriting it.
- IAFactory provides a “Reprompt” button or action to send the last message to a different model (e.g., from GPT to Claude or DeepSeek).
- This lets you compare response styles, factual accuracy, or code quality.

### Tax Example
- Ask a question like: “Explain VAT for a small LLC in Algeria.”
- Get a first answer with the default model.
- Click “Reprompt” and choose another model (e.g., Claude or DeepSeek).
- Compare the answers, keep the clearest one, or combine useful elements from several models.

### Code/Technical Example
- Ask: “Write a Python function to calculate VAT from an amount excluding tax and a rate.”
- Analyze the first version from a model (code quality, clarity of comments).
- Use reprompt to send the same request to another model more specialized in code, if available.

## IAFactory Assistants

### Concept
- An IAFactory assistant is an AI “profile” specialized in a theme (SME taxation, law, school help, religion, development, etc.).
- Each assistant has its own context, instructions, main language, and possibly knowledge sources (internal documents, RAG).
- You can create several assistants and organize them by project, client, or business domain.

### Creating an Assistant
- Open the “Assistants” section in the IAFactory interface.
- Click “Create an assistant” and give it a name (e.g., “SME Taxation Algeria”).
- Add clear instructions: target audience, language level (simple, expert), scope (type of accepted questions).
- Choose the default language (FR, darija, amazigh, EN) according to the intended users.

### Models and Sources
- Select the preferred model(s) for this assistant (e.g., model X for writing, model Y for analysis).
- (Optional) Connect internal documents: sample invoices, contracts, course materials, FAQs, etc., via your RAG engine if already integrated.
- Check that the assistant responds as expected by asking 2–3 test questions.

## Best Practices & Limitations

### Human Verification
- Always review answers for sensitive topics: taxation, law, health, HR, financial decisions.
- In case of doubt, use reprompt to query another model and compare answers.
- For critical cases, have the final answer validated by a human expert (accountant, lawyer, doctor, etc.).

### Personal Data and Confidentiality
- Avoid pasting highly sensitive data (credit card numbers, passwords, very detailed medical information) in the chat.
- Limit attachments to documents strictly necessary for the request (contracts, invoices, courses), anonymizing them if possible.
- Refer to IAFactory’s privacy policy and commitments regarding data management (to be specified with your legal text).

### Using Multiple Models Wisely
- For marketing texts: test at least 2 models to compare tone and creativity.
- For code: prefer models known for code quality, then reprompt to another model for review or optimization.
- For document summaries: use a model reliable in understanding long texts, then check critical points with a second model.

### Role of IAFactory Assistants
- IAFactory assistants are smart aids but do not replace a human expert or professional consultation.
- They help save time, clarify concepts, generate drafts, and prepare discussions with specialists.
- In case of regulatory or legal changes, update the instructions and documents linked to the relevant assistants.
