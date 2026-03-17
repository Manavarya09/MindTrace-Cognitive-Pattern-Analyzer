# MindTrace - Advanced Visualizations Module

import nbformat
from nbformat import v4

nb = v4.new_notebook()

nb.cells.append(v4.new_markdown_cell('# MindTrace - Advanced Visualizations'))

# Radar Chart
nb.cells.append(v4.new_markdown_cell('### 1. Radar/Spider Charts'))
code = '''def plot_radar(df):
    emotions = ["joy", "anger", "sadness", "fear", "surprise", "anticipation"]
    values = [df[f"emotion_{e}"].mean() for e in emotions]
    values += values[:1]
    
    angles = np.linspace(0, 2*np.pi, len(emotions), endpoint=False).tolist()
    angles += angles[:1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=emotions+[emotions[0]], fill="toself", 
                                name="Emotions", line_color="#9b59b6", fillcolor="rgba(155,89,182,0.3)"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])), showlegend=False,
                    title="Emotion Radar", height=450)
    return fig

fig = plot_radar(dashboard.df)
fig.show()'''
nb.cells.append(v4.new_code_cell(code))

# Sunburst Chart
nb.cells.append(v4.new_markdown_cell('### 2. Sunburst Chart'))
code = '''def plot_sunburst(df):
    # Create hierarchy: sentiment -> emotion -> count
    data = []
    for sent in df["sentiment_label"].unique():
        sent_data = df[df["sentiment_label"] == sent]
        for emo in sent_data["emotion_dominant"].unique():
            count = len(sent_data[sent_data["emotion_dominant"] == emo])
            data.append({"sentiment": sent, "emotion": emo, "count": count})
    
    fig = px.sunburst(data, path=["sentiment", "emotion"], values="count",
                    title="Sentiment-Emotion Distribution", height=500)
    return fig

fig = plot_sunburst(dashboard.df)
fig.show()'''
nb.cells.append(v4.new_code_cell(code))

# Treemap
nb.cells.append(v4.new_markdown_cell('### 3. Treemap Visualization'))
code = '''def plot_treemap(df):
    daily = df.groupby(["date", "sentiment_label"]).size().reset_index(name="count")
    daily["date"] = daily["date"].astype(str)
    
    fig = px.treemap(daily, path=["date", "sentiment_label"], values="count",
                    title="Activity Treemap by Date and Sentiment", height=500)
    return fig

fig = plot_treemap(dashboard.df)
fig.show()'''
nb.cells.append(v4.new_code_cell(code))

# Parallel Categories
nb.cells.append(v4.new_markdown_cell('### 4. Parallel Categories'))
code = '''def plot_parallel(df):
    sample = df.sample(min(500, len(df)))
    
    fig = px.parallel_categories(sample, dimensions=["sentiment_label", "emotion_dominant", "time_period"],
                                color="polarity", color_continuous_scale="RdBu",
                                title="Category Flow Analysis", height=500)
    return fig

fig = plot_parallel(dashboard.df)
fig.show()'''
nb.cells.append(v4.new_code_cell(code))

# Save
with open('advanced_viz.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print('Advanced visualizations created')
