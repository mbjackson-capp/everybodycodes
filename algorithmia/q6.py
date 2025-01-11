from itertools import chain

example = """RR:A,B,C
A:D,E
B:F,@
C:G,H
D:@
E:@
F:@
G:@
H:@""".split('\n')

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name 
        self.children = []
        self.parent = None

    def path_to(self):
        if len(self.children) == 0:
            return [self.name]
        else:
            # result = []
            # for child in self.children:
            #     child_paths = child.path_to()
            #     for path in child_paths:
            #         result.append(self.name + path)
            # return result
            list_2d = [[self.name + path for path in child.path_to()] for child in self.children]
            return list(chain(*list_2d))
        
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def __repr__(self):
        return f"TreeNode(name: {self.name}; children: [{self.children}])"

nodes = {}

# TODO: because fruits all have the name '@', each node needs a unique id integer which can be used to access it

def parse_lines(lines: list[str]):
    nodes = {}
    id = 0
    for line in lines:
        print(f"Parsing line {line}...")
        root, children = line.split(":")
        print(f"Root: {root}")
        children = children.split(",")
        par = Node(id, root)
        # TODO: fix parent to use node id
        nodes[id] = par
        for child_name in children:
            id += 1
            child = Node(id, child_name)
            nodes[id] = child
            par.add_child(child)
            print(f"new child {child.name} created; its parent is {child.parent}")
        
    return nodes 

collection = parse_lines(example)
for id in collection.keys():
    print(collection[id].children)





# for line in example:
#     line_parse(line)

# print(nodes['RR'].path_to())


