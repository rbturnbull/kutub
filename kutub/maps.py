import pydeck as pdk
from django_pandas.io import read_frame

def repositories_map(repositories):
    data = read_frame(repositories)

    icon_data = {
        "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
        "width": 128,
        "height":128,
        "anchorY": 128
    }
    data['icon_data']= None
    for i in data.index:
        data['icon_data'][i] = icon_data


    view_state = pdk.ViewState(
        longitude=data['longitude'].mean(),
        latitude=data['latitude'].mean(),
        zoom=5,
        pitch=10,
    )

    icon_layer = pdk.Layer(
        type='IconLayer',
        data=data,
        get_icon='icon_data',
        get_size=4,
        pickable=True,
        size_scale=15,
        get_position=['longitude', 'latitude'],
    )
    tooltip = {
        "html": "<b>Name:</b> {identifier} <br/> <b>Settlement:</b> {settlement}<br/> <b>URL:</b> {url}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip=tooltip, map_style=pdk.map_styles.LIGHT)
    return r