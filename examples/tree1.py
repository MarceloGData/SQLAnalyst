#https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python

from anytree import Node, RenderTree

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

print(udo)

print(joe)

for pre, fill, node in RenderTree(udo):
    print("%s%s" % (pre, node.name))

print(dan.children)

root = Node({'a':'b', 'c':'d'})
leaf1 = Node({'a':'1', 'c':'2'}, parent=root)
leaf1 = Node({'a':'3', 'c':'4'}, parent=root)

print(root.children)

for leaf in root.children:
    print (leaf.name)
    print (leaf.name["a"])
