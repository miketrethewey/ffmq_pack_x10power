import commentjson
import os

chathud = {}
codes = []

print("Reading Items")
dirname = os.path.join(".", "items")
for filename in os.listdir(dirname):
    if os.path.isfile(os.path.join(dirname, filename)):
        if os.path.splitext(filename)[1].lower() == ".json":
            print(f"Reading: {os.path.join(dirname, filename)}")
            with open(os.path.join(dirname, filename), "r") as itemsFile:
                itemsManifest = commentjson.load(itemsFile)
                for item in itemsManifest:
                    if "codes" in item:
                        primary = item["codes"].split(",")[0].strip()
                        chathud[primary] = {
                            "codes": [],
                            "secondary_codes": [],
                            "name": item["name"],
                            "type": item["type"]
                        }
                        itemCodes = list(map(lambda x: x.strip(), item["codes"].split(",")))
                        for tmp in sorted(itemCodes):
                            chathud[primary]["codes"].append(tmp)
                        chathud[primary]["codes"] = sorted(set(chathud[primary]["codes"]))
                        codes += itemCodes
                    else:
                        print(f"Codes not defined for '{item['name']}'")
                    if "stages" in item:
                        for stage in item["stages"]:
                            for code in ["codes", "secondary_codes"]:
                                if code in stage:
                                    stageCodes = list(map(lambda x: x.strip(), stage[code].split(",")))
                                    for tmp in sorted(stageCodes):
                                        chathud[primary][code].append(tmp)
                                    chathud[primary][code] = sorted(set(chathud[primary][code]))
                                    codes += stageCodes
print("")

chatcodes = ""
for [cCode, cCodes] in chathud.items():
    cName = cCodes["name"]
    chatcodes += (f"{cName}") + "\n"
    chatcodes += ("-" * len(cName)) + "\n"
    chatcodes += (f"!hud {cCode}") + "\n"
    if len(cCodes["secondary_codes"]) or cCodes["type"] == "consumable":
        chatcodes += (f"> !hud {cCode} up") + "\n"
        chatcodes += (f"> !hud {cCode} down") + "\n"
        for secondary in cCodes["secondary_codes"]:
            chatcodes += (f"> !hud {cCode} {secondary}") + "\n"

    chatcodes += ("") + "\n"

codes = set(codes)
codes = list(codes)
codes.sort()

outputdir = os.path.join(".", "resources", "tests", "output")
if not os.path.exists(outputdir):
    os.makedirs(outputdir)
with open(os.path.join(outputdir, "chathud.txt"), mode="w+", encoding="utf-8") as chathudTxt:
    chathudTxt.write(chatcodes)
with open(os.path.join(outputdir, "itemCodes.json"), mode="w+", encoding="utf-8") as itemsJSON:
    itemsJSON.write(commentjson.dumps(codes, indent=2))
