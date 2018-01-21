import csv

def SoftwareLink(libname, homepage):
    return "[{}]({})".format(libname,homepage)

def RecipeLink(repo, reponame):
    if repo == "bitbucket":
        s = "bitbucket.org"
    elif repo == "github":
        s = "github.com"
    else:
        raise NameError("Unknown repo: {}".format(repo))

    return '[<img src="https://{0}/favicon.ico" height="28">](https://{0}/joakimono/{1})'.format(s,reponame)

def BadgeBintray(libname):
    return "[![Download](https://api.bintray.com/packages/joakimono/conan/{0}%3Ajoakimono/images/download.svg)](https://bintray.com/joakimono/conan/{0}%3Ajoakimono/_latestVersion)".format(libname)

def BadgeTravis(reponame, branch):
    return "[![Build Status UNIX](https://travis-ci.org/joakimono/{0}.png?branch={1})](https://travis-ci.org/joakimono/{0})".format(reponame,branch)

def BadgeAppveyor(repo,reponame,branch):
    return "[![Build Status WIND](https://ci.appveyor.com/api/projects/status/{0}/joakimono/{1}?branch={2}&svg=true)](https://ci.appveyor.com/project/joakimono/{1})".format(repo,reponame,branch)

def TableHeader():
    return "# status-my-conan-recipes\n\nSoftware | Recipe | Bintray | Linux, macOS | Windows\n---|---|---|---|---\n"

def WriteRow(libname,homepage,repo,reponame,branch,inTable):
    if not inTable:
        return "{}\n{}\n{}\n".format(BadgeBintray(libname),
                                     BadgeTravis(reponame,branch),
                                     BadgeAppveyor(repo,reponame,branch))
    else:
        return "{}|{}|{}|{}|{}\n".format(SoftwareLink(libname,homepage),
                                         RecipeLink(repo,reponame),
                                         BadgeBintray(libname),
                                         BadgeTravis(reponame,branch),
                                         BadgeAppveyor(repo,reponame,branch))

def GetStatusFor(library):
    with open('list.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if library == row['library']:
                print(WriteRow(row['library'], row['homepage'], row['repo'],
                                   row['reponame'],row['branch'], False))

def WriteLibReadmeFor(library):
    with open('list.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if library == 'ALL' or library == row['library']:
                with open('TemplateReadme.md', 'rt') as mdfile:
                    temp = mdfile.read()
                with open('README_{}.md'.format(row['library']), 'w') as fil:
                    fil.write(temp.format(WriteRow(row['library'],
                                                   row['homepage'],
                                                   row['repo'],
                                                   row['reponame'],
                                                   row['branch'], False),
                                          row['library'],
                                          row['homepage'],
                                          row['version'],
                                          row['opt_example']))
    
def WriteLibReadme(libname, homepage, repo, reponame, branch, version, opt_example):
    with open('TemplateReadme.md', 'rt') as mdfile:
        temp = mdfile.read()
    


def WriteStatusFile():
    with open('Out.md', 'w') as fil:
        fil.write(TableHeader())
        with open('list.csv', 'rt') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                theLine = WriteRow(row['library'], row['homepage'], row['repo'],
                                   row['reponame'],row['branch'], True)
                fil.write(theLine)
