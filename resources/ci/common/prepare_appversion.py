import common
import json
import os                 # for env vars
from shutil import copy   # file manipulation


def prepare_appversion():
    env = common.prepare_env()

    CI_SETTINGS = {}
    manifest_path = os.path.join(".", "resources", "app", "meta", "manifests", "ci.json")
    if not os.path.isfile(manifest_path):
        raise AssertionError("Manifest not found: " + manifest_path)
    with open(manifest_path) as ci_settings_file:
        CI_SETTINGS = json.load(ci_settings_file)

    dirs = [
        os.path.join("..", "build"),
        os.path.join("..", "merge"),
        os.path.join("..", "merge", "scripts")
    ]
    for dirname in dirs:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    # set tag to app_version.txt
    if not env["GITHUB_TAG"] == "":
        with open(os.path.join(".", *CI_SETTINGS["common"]["prepare_appversion"]["app_version"]), mode="w+", encoding="utf-8") as f:
            _ = f.read()
            f.seek(0)
            f.write(env["GITHUB_TAG"])
            f.truncate()
            print("Wrote %s as AppVersion" % env["GITHUB_TAG"])
        with open(os.path.join(dirs[1], "scripts", "ver.lua"), mode="w+", encoding="utf-8") as ver:
            _ = ver.read()
            ver.seek(0)
            with (open(os.path.join(".", "manifest.json"))) as manifestFile:
              manifestJSON = json.load(manifestFile)
              ver.writelines([
                "print(\"Package Name:    " + manifestJSON["name"] + "\")",
                "print(\"Package Author:  " + manifestJSON["author"] + "\")",
                "print(\"Package Version: " + env["GITHUB_TAG"] + "\")"
              ])
              ver.truncate()
              print("Wrote %s as Pack Version lua script" % env["GITHUB_TAG"])

    copy(
        os.path.join(".", *CI_SETTINGS["common"]["prepare_appversion"]["app_version"]),
        os.path.join(dirs[0], "app_version.txt")
    )


def main():
    prepare_appversion()


if __name__ == "__main__":
    main()
else:
    raise AssertionError("Script improperly used as import!")
