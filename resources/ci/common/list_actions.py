import os
import yaml

allACTIONS = {}
listACTIONS = []

def process_walk(key, node):
  global allACTIONS
  global listACTIONS
  if key == "uses":
    action = node.split('@')
    if '@' in node:
      version = action[1]
      action = action[0]
    if action not in allACTIONS:
      allACTIONS[action] = []
    allACTIONS[action].append(version)
    allACTIONS[action] = list(set(allACTIONS[action]))
    listACTIONS.append(node)

def walk(key, node):
  if type(node) is dict:
    return {k: walk(k, v) for k, v in node.items()}
  elif type(node) is list:
    return [walk(key, x) for x in node]
  else:
    return process_walk(key, node)

for r,d,f in os.walk(os.path.join(".",".github")):
  if "actions" in r or "workflows" in r:
    for filename in f:
      print(
        " " +
        ("-" * (len(os.path.join(r,filename)) + 2)) +
        " "
      )
      print("| " + os.path.join(r,filename) + " |")
      with(open(os.path.join(r,filename), "r")) as yamlFile:
        print(
          " " +
          ("-" * (30 + 5 + 10 + 2)) +
          " "
        )
        yml = yaml.safe_load(yamlFile)
        walk("uses", yml)
        dictACTIONS = {k.split('@')[0]: (k.split('@')[1] if '@' in k else "") for k in sorted(list(set(listACTIONS)))}
        for action, version in dictACTIONS.items():
          print(
            "| %s\t%s |"
            %
            (
              action.ljust(30),
              version or "N/A"
            )
          )
        print(
          " " +
          ("-" * (30 + 5 + 10 + 2)) +
          " "
        )
      print("")

for action, versions in allACTIONS.items():
  if len(versions) > 1:
    print(
      "| %s\t%s |"
      %
      (
        action.ljust(30),
        versions or "N/A"
      )
    )
