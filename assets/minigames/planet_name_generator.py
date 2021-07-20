import js2py as js2py

js = """

var part1 = [
    "Æ",
    "Arc",
    "A",
    "Ab",
    "Ag",
    "At",
    "Am",
    "Amon",
    "An",
    "Ant",
    "Aer",
    "Aeria",
    "Ar",
    "Aria",
    "Atar",
    "Astar",
    "Ana",
    "Av",
    "Ba",
    "Ban",
    "Bant",
    "Bar",
    "Be",
    "Bet",
    "Bi",
    "Bro",
    "Bo",
    "Bon",
    "Brum",
    "B’",
    "Ca",
    "Camp",
    "Car",
    "Carr",
    "Ce",
    "Cer",
    "Ci",
    "Clo",
    "Chur",
    "Cold",
    "Con",
    "Coper",
    "Corr",
    "Cu",
    "Cy",
    "C’",
    "Da",
    "Dark",
    "De",
    "Del",
    "Deep",
    "Dep",
    "Der",
    "Dikar",
    "Du",
    "Dur",
    "Dun",
    "E",
    "Ea",
    "El",
    "Er",
    "Exo",
    "Far",
    "Fox",
    "Fog",
    "Fon",
    "Fur",
    "Fun",
    "Fung",
    "Galad",
    "Gunt",
    "Gren",
    "H",
    "Hub",
    "Har",
    "Hel",
    "Hon",
    "Hed",
    "Ib",
    "Ian",
    "Int",
    "Iv",
    "Jan",
    "Ko",
    "K'",
    "Kaan",
    "Khan",
    "Kne",
    "Ken",
    "Ket",
    "Kep",
    "Ku",
    "Klin",
    "Lad",
    "Leg",
    "Lo",
    "Lo",
    "Lone",
    "Long",
    "L'",
    "Ll'",
    "Majest",
    "Maz",
    "Mer",
    "Merc",
    "Miran",
    "Mun",
    "Nar",
    "Nad",
    "Night",
    "Nir",
    "Nit",
    "Nib",
    "Non",
    "No",
    "Ob",
    "Ox",
    "Out",
    "Ov",
    "Oz",
    "Pa",
    "Pat",
    "Pap",
    "Pan",
    "Pert",
    "Plane",
    "Plu",
    "Plo",
    "Pro",
    "Pra",
    "Pran",
    "Por",
    "Pool",
    "Pling",
    "Rem",
    "Sai",
    "S'",
    "So'",
    "Sat",
    "Sen",
    "Sev",
    "Shan",
    "Shandak",
    "Siden",
    "Sizen",
    "Sot",
    "Sop",
    "Sot Ank",
    "Sot Lo",
    "Son",
    "Scar",
    "Steep",
    "Suil",
    "Sul",
    "Sum",
    "Sun",
    "Sva",
    "T",
    "Tac",
    "Tad",
    "Taf",
    "Tag",
    "Tai",
    "Tal",
    "Talm",
    "Tam",
    "Tar",
    "Tas",
    "Tash",
    "Tav",
    "Tax",
    "Tat",
    "Tap",
    "Tep",
    "Tha",
    "Than",
    "Than Dok",
    "Thry",
    "Trel",
    "Treep",
    "Ter Threp",
    "Tol",
    "Ur",
    "Uran",
    "Um",
    "Vab",
    "Vad",
    "Vak",
    "Vak",
    "Vam",
    "Vad",
    "Ven",
    "Ver",
    "Viv",
    "Vul",
    "Vop",
    "War",
    "Won",
    "Wo",
    "Won",
    "What",
    "Whim",
    "Wim",
    "Win",
    "War",
    "Wun",
    "X'",
    "Xe'",
    "Xen",
    "Xio",
    "Xy",
    "Zing",
    "Zed",
    "Zer",
    "Zem",
    "Zeng",
];

var part2 = [
    "-o",
    "acalla",
    "addon",
    "adon",
    "acan",
    "aroid",
    "anbula",
    "angolia",
    "angalia",
    "ankor",
    "aldi",
    "aka",
    "aleko",
    "alis",
    "alla",
    "alos",
    "an",
    "andia",
    "anella",
    "ania",
    "amis",
    "arnia",
    "aran",
    "ara",
    "arth",
    "arius",
    "atoid",
    "avera",
    "budram",
    "budria",
    "burto",
    "borto",
    "bongo",
    "can",
    "cania",
    "cania",
    "caris",
    "cury",
    "chil",
    "chin",
    "chia",
    "chania",
    "con",
    "da",
    "dai",
    "dania",
    "daleko",
    "dalekon",
    "doria",
    "donia",
    "dikar",
    "eko",
    "ella",
    "elos",
    "elius",
    "elerth",
    "elialia",
    "eria",
    "era",
    "enia",
    "enella",
    "erebus",
    "es",
    "esh",
    "eaux",
    "ebus",
    "eus",
    "eran",
    "fall",
    "far",
    "finer",
    "gania",
    "gatis",
    "gill",
    "golia",
    "ian",
    "ion",
    "illian",
    "illa",
    "idian",
    "inax",
    "iman",
    "itas",
    "ius",
    "iza",
    "iru",
    "ix",
    "kail",
    "kien",
    "las",
    "lax",
    "lak",
    "ler",
    "land",
    "lejos",
    "lok",
    "los",
    "lox",
    "lon",
    "miniar",
    "nar",
    "nia",
    "nicus",
    "nor",
    "nt",
    "ntos",
    "oda",
    "oid",
    "oin",
    "ol",
    "omi",
    "on",
    "onine",
    "ong",
    "ongolia",
    "onia",
    "ornia",
    "ornania",
    "opa",
    "opia",
    "opia",
    "olok",
    "os",
    "oros",
    "orox",
    "orkon",
    "ovin",
    "ox",
    "pidor",
    "pid",
    "pod",
    "rax",
    "reus",
    "rock",
    "roid",
    "rog",
    "ryn",
    "sea",
    "shaa",
    "tan",
    "tara",
    "taria",
    "ton",
    "tes",
    "tep",
    "thra",
    "tania",
    "to",
    "tos",
    "tose",
    "tonia",
    "tronia",
    "topia",
    "tos",
    "trock",
    "tropic",
    "tus",
    "udros",
    "ule",
    "um",
    "umi",
    "uram",
    "urn",
    "urrinia",
    "ury",
    "urdan",
    "uria",
    "uridan",
    "uridian",
    "us",
    "utlis",
    "va",
    "vana",
    "vas",
    "vav",
    "vin",
    "vis",
    "viz",
    "za",
    "‘am",
    "‘an",
    "‘us",
    "al",
]

var prefix = [
    "Alpha",
    "Alpha Omega",
    "Beta",
    "Gamma",
    "Ceti",
    "Delta",
    "Epsilon",
    "Theta",
    "Zeta",
    "Omega",
    "Tau",
    "Tau Ceti",
    "The planet of",
    "The moon of",
    "The ringed planet of",
    "The robot world of",
    "The mountainous planet of",
    "The mist planet of",
    "The lava world of",
    "The ghost world of",
    "The desert planet of",
    "The ancient planet of",
    "New",
    "White",
    "East",
    "West",
    "North",
    "Old",
    "Las",
    "Los",
    "La",
];

var suffix = [
    "Alpha",
    "Beta",
    "Gamma",
    "Kappa",
    "Sigma",
    "Prime",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIV", "XV", "XVI",
    "World", "Moon", "gas giant",
    "e1", "e2", "e3", "e4"
]

generateNew = function () {
    var final = "";
    // var type = Math.floor(Math.random() * 100);
    var prefixChance = Math.floor(Math.random() * 100);
    var suffixChance = Math.floor(Math.random() * 100);
    var randomPrefix = prefix[Math.floor(Math.random() * prefix.length)];
    var randomSuffix = suffix[Math.floor(Math.random() * suffix.length)];
    var secondWordChance = suffix[Math.floor(Math.random() * suffix.length)];

    final = planetName();

    if (prefixChance <= 20) {
        final = randomPrefix + " " + final;
    }

    if (secondWordChance <= 20) {
        final = final + " " + planetName();
    }

    if (suffixChance <= 25){
        final = final + " " + randomSuffix;
    } else if(suffixChance > 25 && suffixChance <= 50) {
        final = final + " " + Math.floor(Math.random() * 400);
    }   
    return final;
}

//--a simple planet name
planetName = function(){
    var randomPart1 = part1[Math.floor(Math.random() * part1.length)];
    var randomPart2 = part2[Math.floor(Math.random() * part2.length)];

    return randomPart1 + randomPart2;
}

generateNew()

"""


def generatePlanetName():
    return js2py.eval_js(js)