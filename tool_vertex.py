import maya.cmds as cmds
from PySide2 import QtWidgets
import sys

def export_vertex(object):
    if not cmds.objExists(object):
        print(f"Object {object} does not exist.")
        return []
    
    verts_count = cmds.polyEvaluate(object, vertex=True)
    vertices = [cmds.pointPosition(f'{object}.vtx[{i}]', local=True) for i in range(verts_count)]
    return vertices

def compare_vertex(object1, object2):
    if not cmds.objExists(object1):
        print(f"Object {object1} does not exist.")
        return "", ""
    if not cmds.objExists(object2):
        print(f"Object {object2} does not exist.")
        return "", ""

    verts_count1 = cmds.polyEvaluate(object1, vertex=True)
    verts_count2 = cmds.polyEvaluate(object2, vertex=True)

    if verts_count1 != verts_count2:
        print(f"Objects {object1} and {object2} have different number of vertices.")
        return f"Objects {object1} and {object2} have different number of vertices.", ""

    differences = []
    extra_info = ""

    for i in range(verts_count1):
        pt1 = cmds.pointPosition(f'{object1}.vtx[{i}]', local=True)
        pt2 = cmds.pointPosition(f'{object2}.vtx[{i}]', local=True)
        if pt1 != pt2:
            differences.append((i, pt1, pt2))
            cmds.warning(f"Vertex {i} is different")

    if not differences:
        result = f"Objects {object1} and {object2} have identical vertex positions."
    else:
        result = f"Differences found in vertex positions between {object1} and {object2}:\n"
        for diff in differences:
            extra_info += f"Vertex {diff[0]}: \n {object1} -> {diff[1]} \n {object2} -> {diff[2]}\n \n"

    return result, extra_info

def show_result(result, extra_info):
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    msg_box = QtWidgets.QMessageBox()
    msg_box.setText(result)
    msg_box.setWindowTitle("Vertex Comparator")

    extra_info_button = None
    if extra_info:
        extra_info_button = msg_box.addButton("More Info", QtWidgets.QMessageBox.ActionRole)

    msg_box.exec_()
    if extra_info_button and msg_box.clickedButton() == extra_info_button:
        info_box = QtWidgets.QMessageBox()
        info_box.setText(extra_info)
        info_box.setWindowTitle("Vertex different")
        info_box.exec_()

def show_error_message(message):
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText(message)
    msg_box.setWindowTitle("Selection Error")
    msg_box.exec_()

selection = cmds.ls(sl=True)

if len(selection) != 2:
    show_error_message("Please select exactly two objects.")
else:
    object1 = selection[0]
    object2 = selection[1]

    result, extra_info = compare_vertex(object1, object2)
    print(result)
    show_result(result, extra_info)