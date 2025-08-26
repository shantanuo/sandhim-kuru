import networkx as nx
from collections import defaultdict
from indic_transliteration.sanscript import transliterate
from functools import partial


class SandhiGraph:
    
    def __init__(self, input_trans, output_trans):
        self.G = nx.DiGraph()
        self.depth_map = defaultdict(list)
        self.transliterate = partial(transliterate, _from=input_trans, _to=output_trans)
        print(f"{input_trans=}, {output_trans=}")

    def add_node(self, name: str, depth: int):
        # Add the node to the graph with its attributes
        self.G.add_node(name, depth=depth)
        self.depth_map[depth].append(name)

    def add_edge(self, edge: tuple[str, str]):
        # Add the edge
        self.G.add_edge(edge[0], edge[1])

    def remove_descendants(self, node: str):
        # Remove the node and all its descendants from the graph
        descendants = set(self.G.successors(node))
        descendants.add(node)
        self.G.remove_nodes_from(descendants)
        for depth in self.depth_map:
            self.depth_map[depth] = [n for n in self.depth_map[depth] if n not in descendants]

    def keep_only(self, name:str, depth:int):
        # Only keep this node at depth and remove descendants of all other nodes
        for n in self.depth_map[depth]:
            if n.name != name:
                self.remove_descendants(n)
    
    def to_tree_view(self) -> dict:
        root = self.depth_map[0][0]
        data = {
            "id": root,
            "name": self.transliterate(root),
            }
        print(f"output = {data['id']}")
        self._add_children(data)
        return data

    def _add_children(self, parent: dict):
        for child_name in self.G.successors(parent["id"]):
            child_dict = {
                "id": child_name,
                "name": self.transliterate(child_name),
                }
            if "children" not in parent:
                parent["children"] = []
            parent["children"].append(child_dict)
            self._add_children(child_dict)