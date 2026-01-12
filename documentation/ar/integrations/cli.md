# تكامل CLI مع IAFactory

## المقدمة
تتيح لك CLI الخاصة بـ IAFactory التفاعل مع واجهة IAFactory API مباشرة من الطرفية. تشرح هذه الصفحة كيفية تثبيت، إعداد واستخدام CLI لأتمتة مهام الذكاء الاصطناعي.

## المتطلبات
- حساب IAFactory مع مفتاح API صالح
- تثبيت Node.js أو Python على جهازك

## التثبيت
### عبر npm (Node.js)
```bash
npm install -g iafactory-cli
```
### عبر pip (Python)
```bash
pip install iafactory-cli
```

## البدء السريع
1. إعداد مفتاح API الخاص بك:
```bash
iafactory config set api_key مفتاح_API_الخاص_بك
```
2. تنفيذ طلب بسيط:
```bash
iafactory chat "اشرح فوائد أتمتة الذكاء الاصطناعي"
```

## الأوامر الرئيسية
- `iafactory chat <message>`: توليد رد ذكاء اصطناعي
- `iafactory models`: عرض النماذج المتاحة
- `iafactory quota`: عرض الحصة المستخدمة

## نصائح الاستخدام
- استخدم مطالبات واضحة للحصول على إجابات دقيقة
- راجع التوثيق للخيارات المتقدمة

## موارد مفيدة
- [توثيق CLI IAFactory](https://iafactory.com/docs/cli)
- دعم IAFactory: support@iafactory.com