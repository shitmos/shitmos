import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Define nodes (repositories and your local setup)
nodes = {
    "cosmos/chain-registry": "Upstream Repo\n(Main Repository)",
    "your-fork": "Your Fork\n(on GitHub)",
    "local-clone": "Your Local Clone\n(on Your Machine)",
    "feature-branch": "Feature Branch\n(Work on Changes)",
}

# Add nodes to the graph
for key, label in nodes.items():
    G.add_node(key, label=label)

# Define edges (workflow steps)
edges = [
    ("cosmos/chain-registry", "your-fork", "1. Fork the Repo"),
    ("cosmos/chain-registry", "local-clone", "2. Clone Upstream Repo"),
    ("local-clone", "your-fork", "3. Add Fork as Remote"),
    ("local-clone", "feature-branch", "4. Create a New Branch"),
    ("feature-branch", "your-fork", "5. Push Branch to Fork"),
    ("your-fork", "cosmos/chain-registry", "6. Open a Pull Request"),
]

# Add edges to the graph
for src, dst, label in edges:
    G.add_edge(src, dst, label=label)

# Draw the graph
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)  # Position nodes using spring layout
labels = nx.get_node_attributes(G, "label")
edge_labels = {(src, dst): label for src, dst, label in edges}

nx.draw(G, pos, with_labels=True, labels=labels, node_size=4000, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red")

# Show the diagram
plt.title("Git Workflow for Contributing to cosmos/chain-registry")
plt.show()
