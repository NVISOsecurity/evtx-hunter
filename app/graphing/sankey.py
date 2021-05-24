import os

import plotly.graph_objects as go
import json
import vars
import jsonlines


def create_sankey(source_field, target_field):
    usernames = list()
    sources = list()
    targets = list()
    values = list()

    links = list()

    for filename in os.listdir(vars.TMP_DIR):
        f = os.path.join(vars.TMP_DIR, filename)
        with jsonlines.open(f) as reader:
            for item in reader:
                if "EventData" in item["Event"].keys():
                    event_data = item["Event"]["EventData"]
                    if event_data and source_field in event_data.keys():
                        if target_field in event_data.keys():
                            if event_data[source_field] == "-" or event_data[target_field] == "-":
                                continue

                            if event_data[source_field] not in usernames:
                                usernames.append(event_data[source_field])

                            if event_data[target_field] not in usernames:
                                usernames.append(event_data[target_field])

                            links.append((usernames.index(event_data[source_field]),
                                          usernames.index(event_data[target_field])))

    links_processed = list()

    for link in links:
        if link in links_processed:
            continue

        num_link_occurs = links.count(link)
        sources.append(link[0])
        targets.append(link[1])
        values.append(num_link_occurs)
        links_processed.append(link)

    fig = go.Figure(data=[go.Sankey(
        valueformat=".0f",
        valuesuffix="TWh",
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label= usernames,
            color="blue"
        ),
        link=dict(
            source=sources,  # [0, 1, 0, 2, 3, 3],  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=targets,  # [2, 3, 3, 4, 4, 5],
            value=values  # [8, 4, 2, 8, 4, 2]
        ))])
    fig.update_layout(title_text="Interacting computers", font_size=10)

    return fig
