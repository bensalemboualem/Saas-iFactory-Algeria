# Make Integration

## Introduction
Make is an automation tool that lets you integrate the IAFactory API into your workflows without code. This page explains how to connect IAFactory to Make, configure your scenarios, and automate your AI tasks.

## Prerequisites
- An IAFactory account with a valid API key
- A Make account

## Quick Start
1. Log in to Make and create a new scenario.
2. Add an HTTP module.
3. Set the URL: `https://api.iafactory.com/v1/chat/completions`
4. Add the headers:
    - `Authorization: Bearer YOUR_API_KEY`
    - `Content-Type: application/json`
5. Example payload:
```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "Generate a summary of the IAFactory project"}
  ]
}
```
6. Run the scenario and retrieve the AI response.

## Automation Examples
- Automatic report generation
- Bulk text analysis
- Sending AI responses to Slack, Email, etc.

## Optimization Tips
- Use the `temperature` parameter to adjust response creativity
- Manage errors and quotas via Make modules

## Useful Resources
- [IAFactory API Documentation](https://iafactory.com/docs)
- [Official Make Tutorial](https://www.make.com/en/help)
- IAFactory Support: support@iafactory.com