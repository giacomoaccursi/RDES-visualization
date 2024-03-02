import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from YAMLDataLoader import YAMLDataLoader
import matplotlib.gridspec as gridspec
import os

snapshot_dir = "step-snapshot"
files = os.listdir(snapshot_dir)

for file in files: 
    file_name = os.path.splitext(file)[0]
    loader = YAMLDataLoader(os.path.join(snapshot_dir, file))

    time = loader.time
    step = loader.step
    nodes = loader.nodes
    events = loader.events
    event_list = loader.event_list

    # Generate random color for node. 
    node_colors = sns.color_palette("hls", len(nodes)).as_hex()

    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 0])
    fig = plt.figure()
    fig.suptitle("Time: {} \nStep: {}".format(time, step), fontsize=10)

    plt.subplots_adjust(hspace=0.4) 

    G = nx.Graph()
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title('Nodes neighborhood', fontsize=10)


    # Add nodes to the graph.
    for i, node in enumerate(nodes): 
        G.add_node(node.id, color=node_colors[i])
        # Add edge between neighbors
        for neigh in node.neighbors: 
            G.add_edge(node.id, neigh)

    # Get node colors.
    color = nx.get_node_attributes(G, 'color')

    options = {
        'node_color': [color[node] for node in G.nodes()],
        'node_size': 400,
        'width': 2,
    }

    nx.draw_shell(G, ax=ax1, with_labels=True, font_weight='bold', **options )

    G = nx.DiGraph()
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title('Event dependencies', fontsize=10)

    # Add nodes to the graph.
    for event in events: 
        G.add_node(event.id, color=node_colors[event.node-1])
        # Add edge between neighbors
        for deps in event.dependencies: 
            G.add_edge(event.id, deps)

    # Get node colors.
    color = nx.get_node_attributes(G, 'color')

    options = {
        'node_color': [color[node] for node in G.nodes()],
        'node_size': 200,
        'width': 1,
        'arrows': True,
        'arrowstyle': '->',
        'arrowsize': 7,
    }
    nx.draw_shell(G,  ax=ax2, with_labels=True, font_weight='bold', connectionstyle='arc3,rad=0.2', **options)

    ax3 = fig.add_subplot(gs[1, :]) 

    G = nx.Graph()
    fel_string = "Future Event List (event, time)\n\n {}".format([(event.id, event.time)for event in event_list])
    ax3.set_title(fel_string, fontsize=10)
    nx.draw(G, ax=ax3, with_labels=True, font_weight='bold')
    plt.savefig("step-visualization/{}.svg".format(file_name), format="SVG")
