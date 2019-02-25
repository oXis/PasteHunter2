import os


class Report():

    def __init__(self, meta, content, matches):

        self.parser = meta["parser"]
        self.meta = meta
        self.content = content
        self.matches = matches

        self.urgent = False
        for matche in matches:
            if matche.urgent:
                self.urgent = True

    def __str__(self):
        ret = ""
        ret += "User     --> " + self.parser.getUser(self.meta) + "\n"
        ret += "URL      --> " + self.parser.getURL(self.meta) + "\n"
        ret += "Matches  --> " + str(f.desc for f in self.matches)

        return ret

    def getURL(self):
        return self.parser.getURL(self.meta)

    def save(self):

        if not os.path.exists(os.getcwd() + "/saved"):
            os.mkdir(os.getcwd() + "/saved")

        with open("./saved/{}.{}".format(self.meta["key"], self.parser.name), 'a') as out:
            out.write(str(self) + '\n')
            out.write("Content --\n")
            out.write(self.content)
            out.write('\n')
