import yaml
import os
import networkx as nx

def overlaps(set1, set2):
    s1 = set(set1)
    s2 = set(set2)
    intersect = s1.intersection(s2)
    if not intersect: return False
    if s1.issubset(s2) or s2.issubset(s1): return False
    return True

def analyze_structure(targets, out_file):
    G = nx.Graph()
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("| Step | Added Constraint (Pratyahara) | Overlap Components | Structural Freedom (Max Blocks) |\n")
        f.write("|---|---|---|---|\n")
        
        active_nodes = []
        
        for idx, t in enumerate(targets):
            node_id = t['id']
            G.add_node(node_id, elements=set(t['set']))
            active_nodes.append(node_id)
            
            for prev_node in active_nodes[:-1]:
                if overlaps(t['set'], G.nodes[prev_node]['elements']):
                    G.add_edge(node_id, prev_node)
                    
            num_components = nx.number_connected_components(G)
            
            covered_elements = set()
            for n in active_nodes:
                covered_elements.update(G.nodes[n]['elements'])
                
            uncovered_count = 41 - len(covered_elements)
            freedom = num_components + uncovered_count
            
            f.write(f"| {idx+1} | `{node_id}` (len {len(t['set'])}) | {num_components} | {freedom} |\n")
            
    return G

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'pq_tree_reduction.md')
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    targets = []
    for p in data['pratyaharas']:
        targets.append(p)
        
    G = analyze_structure(targets, out_file)
    
    components = list(nx.connected_components(G))
    with open(out_file, 'a', encoding='utf-8') as f:
        f.write("\n### Final Rigid Blocks (Connected Components in Overlap Graph)\n")
        for i, comp in enumerate(components):
            f.write(f"- Block {i+1} ({len(comp)} sets): {', '.join(comp)}\n")

if __name__ == "__main__":
    main()
