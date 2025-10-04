from utils.req import req

template = (
    "📊 API SUMMARY\n\n"
    "new users this month: {{new_users}}\n"
    "total orders this month: {{total_orders}}\n"
    "total paid this month: {{total_paid}}\n\n"
    "TOP USER (this month): {{top_user}}\n\n"
    "TOP ITEMS (this month):\n{{top_items}}\n\n"
    "TOP USERS OVERALL:\n{{top_users_overall}}"
)

async def handler(message):
    res, _ = await req('/stats/summary', message)
    if(res == None):
        return
    
    txt = format_stats(res['data'])
    await message.answer(txt)

def format_stats(data):
    top_user = "None"
    if data["topUser"]:
        u = data["topUser"]["user"]
        top_user = f"{u['name']} ({data['topUser']['orders']} orders, {data['topUser']['totalSpent']} paid)"

    top_items = "\n".join(
        [f"- {i['item']['name']} ({i['count']} sold)" for i in data["topItems"]]
    ) or "None"

    top_users_overall = "\n".join(
        [f"{u['user']['name']} ({u['orders']} orders, {u['totalSpent']} paid)" for u in data["topUsersOverall"]]
    ) or "None"

    return (
        template
        .replace("{{new_users}}", str(data["newUsersThisMonth"]))
        .replace("{{total_orders}}", str(data["totalOrdersThisMonth"]))
        .replace("{{total_paid}}", str(data["totalPaidThisMonth"]))
        .replace("{{top_user}}", top_user)
        .replace("{{top_items}}", top_items)
        .replace("{{top_users_overall}}", top_users_overall)
    )




