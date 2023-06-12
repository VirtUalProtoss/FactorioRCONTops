
def get_tops(client):
    categories = client.send_command("/top")
    metrics_data = []
    for cat in categories.split("\n")[1:]:
        top = cat.\
            split(" - ")[0].\
            replace("[font=heading-1]", "").\
            replace("[/font]", "").\
            split(". ")
        data = client.send_command(f"/top {top[0]}")
        if data != "No data for this category.":
            top_data = []
            top_rows = data.split("\n")
            metric_name = top_rows[0].split(".")[1]
            if len(top_rows) == 1:
                continue
            for el in top_rows[1:]:
                place_data = {
                    "place": el.split(". ")[0],
                    "nickname": el.split(". ")[1].split(" - ")[0],
                    "value": el.split(". ")[1].split(" - ")[1],
                }
                top_data.append(place_data)
            metrics_data.append({
                "description": top[1],
                "data": top_data,
                "name": "factorio_top_" + metric_name,
            })
    return metrics_data
