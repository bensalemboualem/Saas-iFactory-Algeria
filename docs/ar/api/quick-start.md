# البدء السريع - واجهة برمجة التطبيقات

واجهة برمجة تطبيقات LLM متوافقة مع OpenAI لدمج الذكاء الاصطناعي بسهولة في تطبيقاتك.

➡️ **[احصل على مفتاح API والاعتمادات الخاصة بك](https://dashboard.iafactory-algeria.com/api)**

## الاعتمادات المضمنة

جميع المشتركين في IAFactory الجزائر لديهم اعتمادات مضمنة.

| الخطة | المبتدئ | القياسي | الخبير |
|------|---------|---------|--------|
| **الاعتمادات الشهرية** | $2 | $4 | $10 |

يمكنك أيضاً الاشتراك على أساس الدفع حسب الاستخدام مباشرة من إعدادات API.

## مع IAFactory API مباشرة

يولد استجابة إكمال الدردشة بناءً على مطالبتك.

### Python

```python
import requests

url = "https://api.iafactory-algeria.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4.1",
    "messages": [
        {
            "role": "user",
            "content": "اشرح أساسيات التعلم الآلي"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### JavaScript

```javascript
const url = "https://api.iafactory-algeria.com/v1/chat/completions";
const headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
};
const data = {
    model: "gpt-4.1",
    messages: [
        {
            role: "user",
            content: "اشرح أساسيات التعلم الآلي"
        }
    ]
};

fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL

```bash
curl https://api.iafactory-algeria.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "user",
        "content": "اشرح أساسيات التعلم الآلي"
      }
    ]
  }'
```

## مع مكتبة OpenAI

```python
import openai

# تكوين العميل لاستخدام IAFactory الجزائر
openai.api_base = "https://api.iafactory-algeria.com/v1"
openai.api_key = "YOUR_API_KEY"

response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": "ما هي فوائد الطاقة المتجددة؟"}
    ]
)

print(response.choices[0].message.content)
```

## تنسيق الاستجابة

### استجابة ناجحة

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "مرحباً! أنا بخير، شكراً لسؤالك. كيف يمكنني مساعدتك اليوم؟"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 19,
    "total_tokens": 31
  }
}
```

### استجابة البث المباشر

عندما يتم تعيين `stream: true`، يتم إرجاع الاستجابات كأحداث أرسلها الخادم:

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-4.1","choices":[{"index":0,"delta":{"content":"مرحباً"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-4.1","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: [DONE]
```

## الخطوات التالية

- [النماذج والأسعار](./models-pricing.md)
- [رموز الأخطاء](./error-codes.md)
- [المعاملات المتقدمة](./parameters.md)
- [الترحيل من OpenAI](./migration-openai.md)

---

➡️ **[احصل على مفتاح API والاعتمادات الخاصة بك](https://dashboard.iafactory-algeria.com/api)**
