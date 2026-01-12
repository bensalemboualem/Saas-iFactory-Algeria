# IAFactory CLI Integration

## Introduction
The IAFactory CLI allows you to interact with the IAFactory API directly from your terminal. This page explains how to install, configure, and use the CLI to automate your AI tasks.

## Prerequisites
- An IAFactory account with a valid API key
- Node.js or Python installed on your machine

## Installation
### Via npm (Node.js)
```bash
npm install -g iafactory-cli
```
### Via pip (Python)
```bash
pip install iafactory-cli
```

## Quick Start
1. Set your API key:
```bash
iafactory config set api_key YOUR_API_KEY
```
2. Run a simple request:
```bash
iafactory chat "Explain the benefits of AI automation"
```

## Main Commands
- `iafactory chat <message>`: Generate an AI response
- `iafactory models`: List available models
- `iafactory quota`: Show your usage quota

## Usage Tips
- Use clear prompts for precise answers
- Check the documentation for advanced options

## Useful Resources
- [IAFactory CLI Documentation](https://iafactory.com/docs/cli)
- IAFactory Support: support@iafactory.com