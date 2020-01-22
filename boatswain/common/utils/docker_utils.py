#  This file is part of Boatswain.
#
#      Boatswain<https://github.com/theboatswain> is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtWidgets import QMessageBox

from boatswain.common.models.container import Container


def notifyDockerNotAvailable():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Docker daemon isn't running")
    msg.setInformativeText("Boatswain requires to have Docker daemon already up and running")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def notifyDockerException(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Exception occurred!!!")
    msg.setInformativeText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def notifyContainerNotRunning(container: Container, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Container %s is not running" % container.name)
    msg.setInformativeText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def mergeTagMap(tag_map_1, tag_map_2):
    result = {**tag_map_1}
    for key in tag_map_2:
        if key in result:
            if tag_map_1[key] == 1 and tag_map_2[key] == 1:
                continue
            if tag_map_2[key] == 1:
                result[key][key] = 1
            elif tag_map_1[key] == 1:
                result[key] = tag_map_2[key]
                result[key][key] = 1
            else:
                result[key] = mergeTagMap(result[key], tag_map_2[key])
        else:
            result[key] = tag_map_2[key]
    return result


def parseTagMap(container_name, tag_name):
    tag_map = generateTagMap(container_name, tag_name.split('.'))
    first_key = list(tag_map)[0]
    parts = first_key.split('.', 1)
    if len(parts) > 1:
        tag_map[parts[0]] = {first_key: tag_map[first_key]}
        del tag_map[first_key]
    first_key = list(tag_map)[0]
    parts = first_key.split('-', 1)
    if len(parts) > 1:
        tag_map[parts[0]] = {first_key: tag_map[first_key]}
        del tag_map[first_key]
    return tag_map


def generateTagMap(container_name, tag_parts, index=0):
    if index < len(tag_parts) - 1:
        prefix = tag_parts[:index + 1]
        postfix = tag_parts[index + 1:]
        key = container_name + ':' + '.'.join(prefix) + '.' + '.'.join(['x' for x in postfix])
        return {key: generateTagMap(container_name, tag_parts, index + 1)}
    last_part = tag_parts[index].split('-', 1)
    if len(last_part) > 1:
        prefix = '.'.join(tag_parts[:index])
        if prefix:
            prefix += '.'
        key = container_name + ':' + prefix + last_part[0]
        return {key: {container_name + ':' + '.'.join(tag_parts): 1}}
    # if len(tag_parts) > 1:
    #     return {container_name + ':' + '.'.join(tag_parts): {container_name + ':' + '.'.join(tag_parts): 1}}
    return {container_name + ':' + '.'.join(tag_parts): 1}
