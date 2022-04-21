import json
import os
import ssl
import urllib.request
import yaml

allACTIONS = {}
listACTIONS = []

def process_walk(key, node):
  global allACTIONS
  global listACTIONS
  if key == "uses":
    action = node.split('@')
    version = ""
    if '@' in node:
      version = action[1]
    action = action[0]
    if action not in allACTIONS:
      allACTIONS[action] = {
        "versions": [],
        "latest": ""
      }
    allACTIONS[action]["versions"].append(version)
    allACTIONS[action]["versions"] = list(set(allACTIONS[action]["versions"]))
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
      listACTIONS = []
      print(
        " " +
        ("-" * (len(os.path.join(r,filename)) + 2)) +
        " "
      )
      print("| " + os.path.join(r,filename) + " |")
      with(open(os.path.join(r,filename), "r", encoding="utf-8")) as yamlFile:
        print(
          " " +
          ("-" * (40 + 5 + 10 + 2)) +
          " "
        )
        yml = yaml.safe_load(yamlFile)
        walk("uses", yml)
        dictACTIONS = {}
        for k in sorted(list(set(listACTIONS))):
          action = k.split('@')[0]
          version = k.split('@')[1] if '@' in k else ""
          latest = ""
          if "./." not in action:
            apiURL = f"https://api.github.com/repos/{action}/releases/latest"
            if True:
              apiReq = None
              try:
                apiReq = urllib.request.urlopen(apiURL, context=ssl._create_unverified_context())
              except urllib.error.URLError as e:
                if e.code != 403:
                  print(e.code, apiURL)
              if apiReq:
                apiRes = json.loads(apiReq.read().decode("utf-8"))
                if apiRes:
                  latest = apiRes["tag_name"] if "tag_name" in apiRes else ""
                  if latest != "":
                    allACTIONS[action]["latest"] = latest
          dictACTIONS[action] = version
        for action, version in dictACTIONS.items():
          print(
            "| %s\t%s\t%s |"
            %
            (
              action.ljust(40),
              (version or "N/A").ljust(10),
              allACTIONS[action]["latest"]
            )
          )
        print(
          " " +
          ("-" * (40 + 5 + 10 + 2)) +
          " "
        )
      print("")

print(
  " " +
  ("-" * (len("| Outdated |") - 2)) +
  " "
)
print("| Outdated |")
print(
  " " +
  ("-" * (len("| Outdated |") - 2)) +
  " "
)
for action, actionData in allACTIONS.items():
  if len(actionData["versions"]) > 0:
    if allACTIONS[action]["latest"] != "" and actionData["versions"][0] != allACTIONS[action]["latest"]:
      print(
        "| %s\t%s\t%s |"
        %
        (
          action.ljust(40),
          (",".join(actionData["versions"]) or "N/A").ljust(10),
          actionData["latest"].ljust(10)
        )
      )
