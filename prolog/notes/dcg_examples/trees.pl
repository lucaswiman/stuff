tree_nodes(nil) --> [].
tree_nodes(node(Name, Left, Right)) -->
  tree_nodes(Left),
  [Name],
  tree_nodes(Right).