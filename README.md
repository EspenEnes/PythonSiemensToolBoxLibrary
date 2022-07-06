# PythonSiemensToolBoxLibrary

Searches for step7 projects in a given folder archived or unpacked with Step7Finder.
Reads project header without unpacking zip

creates a project class if step7 path is passed to project.
Reads stations, CPU, blocks ,networkinterface 
Parse DB layout to give adresses


if __name__ == "__main__":
    projects = list()

    for i, project in enumerate(Step7Finder.search()):
        project.loadProject()
        projects.append(project)


        if i > 10: break

    z = projects[0]
    z.loadProject()
