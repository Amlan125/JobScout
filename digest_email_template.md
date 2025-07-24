# 🧠 Your Daily Job Digest

Hi! Here are today's top jobs for **{{ keywords }}**:

{% for job in jobs %}
---

### {{ job['title'] }} at {{ job['company'] }}
📍 {{ job['location'] }}  
🔗 [View job posting]({{ job['url'] }})

**Summary:**
{{ job['summary'] }}

{% endfor %}

Have a great day!
