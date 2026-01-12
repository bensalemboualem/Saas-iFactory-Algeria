# تكامل Make

## المقدمة
Make هو أداة أتمتة تتيح لك دمج واجهة IAFactory API في سير العمل الخاص بك بدون كود. تشرح هذه الصفحة كيفية ربط IAFactory بـ Make، إعداد السيناريوهات، وأتمتة مهام الذكاء الاصطناعي.

## المتطلبات
- حساب IAFactory مع مفتاح API صالح
- حساب Make

## البدء السريع
1. سجل الدخول إلى Make وأنشئ سيناريو جديد.
2. أضف وحدة HTTP.
3. ضع عنوان URL: `https://api.iafactory.com/v1/chat/completions`
4. أضف رؤوس الطلب:
    - `Authorization: Bearer مفتاح_API_الخاص_بك`
    - `Content-Type: application/json`
5. مثال على الحمولة:
```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "أنشئ ملخصًا لمشروع IAFactory"}
  ]
}
```
6. نفذ السيناريو واسترجع استجابة الذكاء الاصطناعي.

## أمثلة الأتمتة
- إنشاء تقارير تلقائية
- تحليل نصوص جماعي
- إرسال ردود الذكاء الاصطناعي إلى Slack، البريد الإلكتروني، إلخ.

## نصائح التحسين
- استخدم معامل `temperature` لضبط إبداع الردود
- إدارة الأخطاء والحصص عبر وحدات Make

## موارد مفيدة
- [توثيق واجهة IAFactory API](https://iafactory.com/docs)
- [دليل Make الرسمي](https://www.make.com/en/help)
- دعم IAFactory: support@iafactory.com