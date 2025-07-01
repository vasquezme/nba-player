import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle
from dash import Dash, dcc, html, Input, Output
import seaborn as sns
import plotly.express as px




# def draw_court(ax=None, color='black', lw=2):
#     if ax is None:
#         ax = plt.gca()
#     # Court elements
#     floor = Rectangle((-250, -47.5), 500, 470+47.5, color= '#f5deb3', zorder=0)
#     ax.add_patch(floor)
#     hoop = Circle((0, 0), radius=0.75, linewidth=lw, color=color, fill=False, zorder=2)
#     backboard = Rectangle((-3, -0.75), 6, -0.1, linewidth=lw, color=color, zorder=2)
#     outer_box = Rectangle((-8, -47.5), 16, 19, linewidth=lw, color=color, fill=False, zorder=2)
#     inner_box = Rectangle((-6, -47.5), 12, 19, linewidth=lw, color=color, fill=False, zorder=2)
#     free_throw = Circle((0, -28), 6, linewidth=lw, color=color, fill=False, zorder=2)
#     corner_three_a = plt.Line2D((-22, -22), (-47.5, -14), linewidth=lw, color=color, zorder=2)
#     corner_three_b = plt.Line2D((22, 22), (-47.5, -14), linewidth=lw, color=color, zorder=2)
#     arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color, zorder=2)

#     court_elements = [hoop, backboard, outer_box, inner_box, free_throw,
#                       corner_three_a, corner_three_b, arc]
# 
#     for element in court_elements:
#         if isinstance(element, (Circle, Rectangle, Arc)):
#             ax.add_patch(element)
#         else:
#             ax.add_line(element)
#     return ax

# Example CSV should have columns: LOC_X, LOC_Y, SHOT_MADE_FLAG
df1 = pd.read_csv('curry_2425.csv')  # Replace with your file
df1['Player'] = 'Stephen Curry'

df2 = pd.read_csv('nikola_jokic_2425.csv')
df2['Player'] = 'Nikola Jokic'

df3 = pd.read_csv('mv_2425.csv')
df3['Player'] = 'Big Papi'

df4 = pd.read_csv('mason_2425.csv')
df4['Player'] = 'Mase Dwagg'

df = pd.concat([df1, df2, df3, df4], ignore_index=True)


df['LOC_X'] = pd.to_numeric(df['LOC_X'], errors='coerce')
df['LOC_Y'] = pd.to_numeric(df['LOC_Y'], errors='coerce')


# Filter out shots beyond half court
df = df[(df['LOC_X'].between(-250, 250)) & (df['LOC_Y'].between(-50, 500))]

app = Dash(__name__)

app.layout = html.Div([
    html.H1("NBA Player Shot Chart"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label':p, 'value':p} for p in df['Player'].unique()],
        value='Stephen Curry'
    ),
    dcc.Graph(id='shot-chart')
])

@app.callback(
    Output('shot-chart', 'figure'),
    Input('player-dropdown', 'value')
)

#def update_chart(selected_player):
#    filtered = df[df['Player'] == selected_player]
#    fig = px.scatter(
#        filtered, x='LOC_X', y='LOC_Y',
#        color='SHOT_MADE_FLAG',
#        color_discrete_map={1: 'green', 0: 'red'},
#        title=f"{selected_player} Shot Chart",
#        labels={'LOC_X': 'Court X', 'LOC_Y': 'Court Y'}
#    )
#    fig.update_yaxes(scaleanchor="x", scaleratio=1)
#    fig.update_layout(yaxis=dict(range=[-50, 470]), xaxis=dict(range=[-250, 250]))
#    return 

def update_chart(selected_player):
    filtered = df[df['Player'] == selected_player].copy()
    filtered['SHOT_MADE_FLAG'] = filtered['SHOT_MADE_FLAG'].astype(str)

    fig = px.scatter(
        filtered, x='LOC_X', y='LOC_Y',
        color='SHOT_MADE_FLAG',
        color_discrete_map={1: 'green', 0: 'red'},
        title=f"{selected_player} Shot Chart",
        labels={'LOC_X': 'Court X', 'LOC_Y': 'Court Y'}
    )
    fig.update_traces(showlegend=False, marker_showscale=False)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_layout(yaxis=dict(range=[-50, 470]), xaxis=dict(range=[-250, 250]), showlegend=False)

    # Add hoop
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=-7.5, y0=-7.5, x1=7.5, y1=7.5,
                  line_color="black")
    # Add backboard
    fig.add_shape(type="rect",
                  x0=-30, y0=-7.5, x1=30, y1=-6,
                  line_color="black")
    # Add paint (outer box)
    fig.add_shape(type="rect",
                  x0=-80, y0=-47.5, x1=80, y1=142.5,
                  line_color="black")
    # Add free throw circle
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=-60, y0=82.5, x1=60, y1=202.5,
                  line_color="black")
    # Add 3pt arc (approximate)
    fig.add_shape(type="path",
        path="M -220 92.5 Q 0 237.5 220 92.5",
        line_color="black"
    )
    # Add corner threes
    fig.add_shape(type="line", x0=-220, y0=-47.5, x1=-220, y1=92.5, line_color="black")
    fig.add_shape(type="line", x0=220, y0=-47.5, x1=220, y1=92.5, line_color="black")

    return fig


if __name__ == '__main__':
    app.run(debug=True)



# plt.figure(figsize=(12, 11))
# ax = plt.gca()
# draw_court(ax)

# sns.scatterplot(data=df, x='LOC_X', y='LOC_Y', hue='Player', style='SHOT_MADE_FLAG', palette={'Stephen Curry': 'blue', 'Nikola Jokic': 'orange'}, alpha=0.6, ax=ax, zorder=3)
# plt.title("NBA Player Shot Chart")
# plt.xlim(-250, 250)
# plt.ylim(-50, 470)
# plt.axis('off')
# plt.show()
