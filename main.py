import os
from graphviz import Digraph


def get_path_from_head(path):  # получаем путь до файлов, в которых есть инфа о коммитах
    path += "/logs/refs/heads"
    return path


def get_branches_files(path):  # т.к. веток у проекта может быть несколько, смотрим все файлы (каждый файл в refs/heads
    return os.listdir(path)  # это отдельная ветка)


def get_parent(commit_string):  # получаем ключ родителя из строки с информацией о коммите
    return commit_string[0:40]


def get_child_from_string(commit_string):  # получаем ключ следующего коммита из строки с информацией о коммите
    return commit_string[41:81]


def get_commit_info(commit_string):  # получаем информацию о самом коммите (что написали при коммите версии)
    return commit_string[commit_string.find(':'):-1]


def get_info_from_file(path):  # тут мы считываем из файла ветки все коммиты. Из одного коммита ключ родителя, дочернего
    fp = open(path, 'r')  # элемента, сам коммит. Получится двумерный массив
    line = fp.readline()
    array = []
    while line != '':
        array.append([get_parent(line),get_child_from_string(line),get_commit_info(line)])
        line = fp.readline()
    return array


def creating_edge(graph, commit, next_commit):  # просто создаем связь в графе
    if commit is None or graph is None:
        return

    graph.edge(commit, next_commit)
    return graph


def creating_commit_edges(commits_array, graph):  # функция для записи всех коммитов из одного файла в неё
    for i in range(len(commits_array) - 1):  # каждый коммит добавляем в граф
        graph = creating_edge(
            graph,
            commits_array[i][1],
            commits_array[i + 1][1]
            # commits_array[i][2][commits_array[i][2].find(':') + 2:]
        )
        graph.body[len(graph.body) - 1] = graph.body[len(graph.body) - 1][:-1] + (f" [label=" +
                                      '"' +
                                      commits_array[i][2][commits_array[i][2].find(':') + 2:] +
                                      '"]\n')


if __name__ == '__main__':  # Строка: C:/Users/Фёдор/IdeaProjects/MTG_collection/.git (типа до самой папки .git)
    my_graph = Digraph(comment="Git Tree")
    path = str(input("Please enter the '.git' path: "))
    path = get_path_from_head(path)
    print(get_branches_files(path))
    print(get_info_from_file(f"{path}/{get_branches_files(path)[get_branches_files(path).index('new_branch')]}"))
    print("\n\n")

    # Получаем информацию о всех коммитах, что лежат в master
    commits_array = get_info_from_file(f"{path}/{get_branches_files(path)[get_branches_files(path).index('master')]}")
    creating_commit_edges(commits_array, my_graph)

    # добавляем инфу о других ветках
    for file in get_branches_files(path):
        if file == 'master':  # т.к. master уже добавляли, пропустим её
            continue
        # получаем информацию о коммитах каждой ветки
        commits_array = get_info_from_file(f"{path}/{get_branches_files(path)[get_branches_files(path).index(file)]}")
        creating_commit_edges(commits_array, my_graph)

    print(my_graph.source)
    print(my_graph.body[0])
