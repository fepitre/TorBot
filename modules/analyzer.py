"""
Module is used for analyzing link relationships
"""
from requests.exceptions import HTTPError

from ete3 import Tree, TreeStyle, TextFace, add_face_to_node
from .link import LinkNode
from .utils import multi_thread


def default_layout(node):
    node_style = TextFace(node.name, tight_text=True)
    add_face_to_node(node_style, node, column=0, position='branch-bottom')


default_style = TreeStyle()
default_style.show_leaf_name = False
default_style.layout_fn = default_layout


def build_tree(link, stop=1, rec=0):
    """
    Builds link tree by traversing through children nodes.

    Args:
        link (LinkNode): root node of tree
        stop (int): depth of tree
        rec (int): level of recursion

    Returns:
        tree (ete3.Tree): Built tree.
    """

    tree = Tree(name=link.name)

    if rec == stop:
        return tree
    else:
        rec += 1

    for child in link.links:
        try:
            node = LinkNode(child)
        except Exception as error:
            print(f"Failed to create LinkNode for link: {child}.")
            print(f"Error: {error}")
            continue
        if node.links:
            tree.add_child(build_tree(node, stop, rec))
        else:
            tree.add_child(Tree(name=node.name))

    return tree


class LinkTree:
    """
    This is a class that represents a tree of links within TorBot. This can
    be used to build a tree, examine the number of nodes, check if a node
    exists within a tree, displaying the tree, and downloading the tree. It
    will be expanded in the future to meet further needs.

    Attributes:
        root (LinkNode): root node
        stop_depth (int): Depth of which to stop searching for links
    """

    def __init__(self, root_node, stop_depth=1):
        self._root_node = root_node
        self._tree = build_tree(root_node, stop=stop_depth)

    def __len__(self):
        return len(self._tree)

    def __contains__(self, link):
        return self._tree.search_nodes(name=link)

    @property
    def root_node(self):
        return self._root_node

    @property
    def children(self):
        return self._tree.get_children()

    def save(self, file_name, tree_style=default_style):
        """
        Saves LinkTree to file with given file_name
        Current file types supported are .png, .pdf, .svg

        Args:
            file_name (str): Name of file being saved to
            tree_style (TreeStyle): Styling of downloaded tree
        """
        self._tree.render(file_name, tree_style)

    def show(self, tree_style=default_style):
        """
        Displays image of LinkTree

        Args:
            tree_style (TreeStyle): Styling of downloaded tree
        """
        self._tree.show(tree_style)
