import os
import re
import json


class Configuration:
    def __init__(self, sh_file) -> None:
        self.sh_file = sh_file
        self.name = os.path.basename(sh_file)
        self.type = "python"
        self.request = "launch"
        self.program = None
        self.console = "integratedTerminal"
        self.cwd = "${workspaceFolder}"
        self.env = {}
        self.args = []

    def cleanStr(self, content: str) -> str:
        content = content.rstrip('\n')
        content = content.rstrip()
        content = content.rstrip('\\')
        content = content.rstrip()
        content = content.lstrip()
        return re.sub(' +', ' ', content)

    def readEnv(self, content: str):
        envs = content.split(' ')
        for env in envs:
            env_split = env.split('=')
            if (len(env_split) != 2):
                raise TypeError(
                    f"'=' not found in {env} when reading {content}")
            self.env[env_split[0]] = env_split[1]

    def readArgs(self, content: str):
        args = content.split(' ')
        self.args.extend(args)

    def readMix(self, content: str):
        # split to 3 blocks: 0.envs, 1.python, 2.program name and args
        blocks = content.partition("python")
        envs = blocks[0].rstrip()
        mixes = blocks[2].lstrip()
        if len(envs) > 0:
            self.readEnv(envs)

        # len(mixes) definitely > 0
        if ' ' in mixes:
            # blanks exist here, split to 2 blocks: program name, args
            mix = mixes.split(' ', 1)
            self.program = mix[0]
            self.readArgs(mix[1])
        else:   # no blanks here, which means no args in content
            self.program = mixes

        # handle relative path
        if self.program.startswith("./"):
            self.program = self.program.replace("./", "${workspaceFolder}/")

    def read(self):
        with open(self.sh_file, 'r') as f:
            pythonFound = False
            while True:
                content = f.readline()
                if not content:
                    break
                if (content[0] == '#'):
                    continue

                content = self.cleanStr(content)
                if len(content) == 0:
                    continue

                if pythonFound:     # "python" already exists before, parse args now
                    self.readArgs(content)
                elif ("python" in content):  # just find "python", handle program
                    # if a line ends with "python", then the program name is in the next line
                    if (content.endswith("python")):
                        content = ' '.join([content, f.readline()])
                        content = self.cleanStr(content)
                    self.readMix(content)
                    pythonFound = True
                else:                       # "python" not found yet, parse envs only
                    self.readEnv(content)

    def exportJson(self):
        configuration = {
            "name": self.name,
            "type": self.type,
            "request": self.request,
            "program": self.program,
            "console": self.console,
            "cwd": self.cwd,
            "env": self.env,
            "args": self.args,
        }
        return json.dumps(configuration)


if __name__ == '__main__':
    CUB_GZSL = Configuration('./CUB_GZSL.sh')
    CUB_GZSL.read()
