def generate_digest(jobs):
    html = """
<html>
<head>
<style>
    body { font-family: Arial, sans-serif; line-height: 1.5; }
    h1 { color: #2E86C1; }
    h3 { color: #2874A6; }
    .job { border-bottom: 1px solid #ddd; padding: 10px 0; }
    .location { color: #555; }
    .summary { margin-top: 5px; }
    a { color: #1B4F72; text-decoration: none; }
    a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>🧠 Your Daily Job Digest</h1>
"""
    for job in jobs:
        html += f"""
<div class="job">
    <h3>{job['title']} at {job['company']}</h3>
    <div class="location">📍 {job['location']}</div>
    <div class="summary">{job.get('summary', 'No summary available')}</div>
    <div><a href="{job['url']}" target="_blank">View job posting</a></div>
</div>
"""
    html += """
</body>
</html>
"""
    return html
