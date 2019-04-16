def load_project_structure(startpath, tree):
    """
    Load Project structure tree
    :param startpath: 
    :param tree: 
    :return: 
    """
    import os
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QIcon
    for element in os.listdir(startpath):
        path_info = startpath + "/" + element
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        if os.path.isdir(path_info):
            load_project_structure(path_info, parent_itm)
            parent_itm.setIcon(0, QIcon('assets/folder.ico'))
        else:
            parent_itm.setIcon(0, QIcon('assets/file.ico'))