events = {}

for i in [2, 3, 4, 5, 6, 7]:
    i = str(i)
    events[i*3] = [
        i,
        i * 2,
        i * 3,
        i + "x" + i,
        i + "x" + i + "x" + i,
        i + "x" + i + "x" + i + " cube",
        i + "x" + i + " cube"
    ]

events["333"].append("rubik's cube")
events["333"].append("rubiks cube")
events["333"].append("rubrics cube")
events["333"].append("rubix cube")
events["333"].append("rubric cube")
events["333"].append("rubric")

events["222"].append("pocket cube")

events["444"].append("rubik's revenge")
events["444"].append("rubiks revenge")

events["555"].append("professor's cube")
events["555"].append("professors cube")
events["555"].append("professor cube")

events["666"].append("vcube6")
events["666"].append("vcube 6")
events["666"].append("v cube 6")
events["666"].append("v-cube6")
events["666"].append("v-cube 6")

events["777"].append("vcube7")
events["777"].append("vcube 7")
events["777"].append("v cube 7")
events["777"].append("v-cube7")
events["777"].append("v-cube 7")

events["333bf"] = ["bld", "3bld", "333bf", "3x3 blindfolded", "3x3x3 blindfolded", "blindfolded", "blind", "3x3 blind", "3x3x3 blind", "rubik's cube without looking", "rubiks cube without looking"]
events["333fm"] = ["fmc", "3fmc", "333fm", "3x3 fewest moves", "3x3x3 fewest moves", "fewest moves challenge", "rubik's cube but it's like an exam"]
events["333oh"] = ["3oh", "33oh", "333oh", "3x3oh", "3x3x3oh", "3x3 one handed", "3x3x3 one handed", "3x3 one-handed", "3x3x3 one-handed", "oh", "3x3 oh", "3x3x3 oh", "rubik's cube using one hand", "fastest hand"]
events["clock"] = ["clock", "clk", "rubiks clock", "rubik's clock", "the best event", "best event"]
events["minx"] = ["minx", "mega", "megaminx", "megamnix", "dodecahedron rubiks cube", "dodecahedron cube"]
events["pyram"] = ["pyram", "pyraminx", "py", "rubiks triangle", "rubik's triangle", "triangle cube", "triangle rubiks cube", "triangle rubik's cube", "the worst event", "worst event"]
events["skewb"] = ["skewb", "sk", "skweb", "skewed cube"]
events["sq1"] = ["square-1", "square-one", "square 1", "square one", "sq1", "squan", "sq-1", "shapeshifter rubric"]
events["444bf"] = ["444bf", "4x4bld", "4bld", "4x4bld", "4x4x4bld", "4 blind", "4x4 blind", "4x4x4 blind", "4 blindfolded", "4x4 blindfolded", "4x4x4 blindfolded", "rubiks revenge without looking", "rubik's revenge without looking"]
events["555bf"] = ["555bf", "5x5bld", "5bld", "5x5bld", "5x5x5bld", "5 blind", "5x5 blind", "5x5x5 blind", "5 blindfolded", "5x5 blindfolded", "5x5x5 blindfolded", "professor cube without looking", "professors without looking", "professor's cube without looking"]
events["333mbf"] = ["333mbf", "mbld", "3mbld", "3x3 mbld", "3x3x3 mbld", "multi-blind", "3x3 multi-blind", "multiblind", "3x3 multiblind", "multi blind", "3x3 multi blind", "multiple blindfolded", "3x3 multiple blindfolded", "3x3x3 multiple blindfolded", "lots of rubiks cubes without looking", "lots of rubik's cubes without looking"]


eventids = {}
eventids["222"] = ["2x2", "2x2"]
eventids["333"] = ["3x3", "3x3"]
eventids["444"] = ["4x4", "4x4"]
eventids["555"] = ["5x5", "5x5"]
eventids["666"] = ["6x6", "6x6"]
eventids["777"] = ["7x7", "7x7"]
eventids["333bf"] = ["3x3 Blindfolded", "3BLD"]
eventids["333fm"] = ["Fewest Moves", "FMC"]
eventids["333oh"] = ["One Handed", "OH"]
eventids["clock"] = ["Clock", "Clock"]
eventids["minx"] = ["Megaminx", "Mega"]
eventids["pyram"] = ["Pyraminx", "Pyra"]
eventids["skewb"] = ["Skewb", "Skewb"]
eventids["sq1"] = ["Square-1", "Square-1"]
eventids["444bf"] = ["4x4 Blindfolded", "4BLD"]
eventids["555bf"] = ["5x5 Blindfolded", "5BLD"]
eventids["333mbf"] = ["Multi Blind", "MBLD"]
