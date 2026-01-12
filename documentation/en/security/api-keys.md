# API Key Management

Securing your API keys is essential to protect access to your IAFactory services.

## Generate an API Key
- Log in to your IAFactory user account
- Go to the “API Keys” section
- Click “Generate a new key”
- Copy and store the key in a safe place

## Best Practices
- Never share your API key publicly
- Do not store the key in a public git repository or accessible source code
- Use environment variables to inject the key on the server side
- Immediately revoke any compromised key

## Key Rotation
- Regularly change your API keys
- Delete unused old keys

## Usage Example
```bash
export API_KEY=YOUR_API_KEY
curl -H "Authorization: Bearer $API_KEY" https://api.iafactory.dz/v1/endpoint
```

For any security questions or issues, contact support@iafactory.dz
