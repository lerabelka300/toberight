#!/usr/bin/env python3
# Telegram morning notification — читает задачи из Supabase, шлёт в Telegram
import urllib.request, json, datetime, ssl

# Fix SSL certificates on macOS Python 3.13
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BOT_TOKEN     = "8878666561:AAFrp12Dk1rhHF59nKGJclvlQ8uAPdy4Uuo"
CHAT_ID       = "224413724"
SUPABASE_URL  = "https://hzebqnsuxgcajvkmqejn.supabase.co"
SUPABASE_ANON = "sb_publishable_4dJd4LLzKL0Lc0bADVFbCA_sS_3Vl9k"

def fetch_tasks():
    url = f"{SUPABASE_URL}/rest/v1/tasks?order=position"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_ANON,
        "Authorization": f"Bearer {SUPABASE_ANON}",
    })
    with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as r:
        return json.loads(r.read())

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as r:
        return json.loads(r.read())

def main():
    today   = datetime.date.today().isoformat()
    days_ru = ["понедельник","вторник","среду","четверг","пятницу","субботу","воскресенье"]
    weekday = days_ru[datetime.date.today().weekday()]

    try:
        tasks = fetch_tasks()
    except Exception as e:
        send_telegram(f"☀️ <b>Доброе утро!</b>\n\n⚠️ Не удалось загрузить задачи: {e}")
        return

    today_tasks = [t for t in tasks if t.get("status") in ("backlog","inprogress") and (not t.get("date") or str(t.get("date",""))[:10] == today)]
    future_tasks = [t for t in tasks if t.get("status") in ("backlog","inprogress") and str(t.get("date",""))[:10] > today]

    lines = [f"☀️ <b>Доброе утро, Лера!</b>", f"Сегодня {weekday}, {today}\n"]

    if today_tasks:
        lines.append("📋 <b>Задачи на сегодня:</b>")
        for t in today_tasks[:10]:
            icon = "▶️" if t.get("status") == "inprogress" else "•"
            lines.append(f"  {icon} {t['title']}")
    elif tasks:
        lines.append("📋 <b>Активные задачи:</b>")
        for t in tasks[:8]:
            lines.append(f"  • {t['title']}")
    else:
        lines.append("✨ Активных задач нет — хороший день для новых планов!")

    if future_tasks:
        lines.append(f"\n📅 Ещё {len(future_tasks)} задач запланировано")

    lines.append("\n💪 Продуктивного дня!")
    send_telegram("\n".join(lines))

if __name__ == "__main__":
    main()
