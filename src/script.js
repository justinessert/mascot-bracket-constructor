bracket_data = {
    "east": [
        "alabama",
        "wisconsin",
        "vcu",
        "yale",
        "virginia",
        "texas_a&m",
        "tcu",
        "virginia_tech",
        "akron",
        "auburn",
        "boise_state",
        "colgate",
        "fdu",
        "gonzaga",
        "iowa",
        "louisiana"
    ],
    "west": [
        "wisconsin",
        "alabama",
        "vcu",
        "yale",
        "virginia",
        "texas_a&m",
        "tcu",
        "virginia_tech",
        "akron",
        "auburn",
        "boise_state",
        "colgate",
        "fdu",
        "gonzaga",
        "iowa",
        ["louisiana", "drake"]
    ],
    "midwest": [
        "vcu",
        "wisconsin",
        "alabama",
        "yale",
        "virginia",
        "texas_a&m",
        "tcu",
        "virginia_tech",
        "akron",
        "auburn",
        "boise_state",
        "colgate",
        "fdu",
        "gonzaga",
        "iowa",
        ["louisiana", "drake"]
    ],
    "south": [
        "yale",
        "wisconsin",
        "vcu",
        "alabama",
        "virginia",
        "texas_a&m",
        "tcu",
        "virginia_tech",
        "akron",
        "auburn",
        "boise_state",
        "colgate",
        "fdu",
        "gonzaga",
        "iowa",
        ["louisiana", "drake"]
    ]
}
nicknames = {
    "akron": "zips",
    "alabama": "crimson tide",
    "arizona_state": "sun devils",
    "arizona": "wildcats",
    "arkansas": "razorbacks",
    "auburn": "tigers",
    "baylor": "bears",
    "boise_state": "broncos",
    "bryant": "bulldogs",
    "charleston": "cougars",
    "chattanooga": "mocs",
    "cleveland_state": "vikings",
    "colgate": "raiders",
    "colorado_state": "rams",
    "creighton": "bluejays",
    "csu_fullerton": "titans",
    "davidson": "wildcats",
    "delaware": "blue hens",
    "drake": "bulldogs",
    "duke": "blue devils",
    "fdu": "knights",
    "florida_atlantic": "owls",
    "furman": "paladins",
    "georgia_state": "panthers",
    "gonzaga": "bulldogs",
    "grand_canyon": "antelopes",
    "houston": "cougars",
    "howard": "bison",
    "illinois": "fighting illini",
    "indiana": "hoosiers",
    "iona": "gaels",
    "iowa_state": "cardinals",
    "iowa": "hawks",
    "jacksonville_state": "gamecocks",
    "kansas_state": "wildcats",
    "kansas": "jayhawks",
    "kennesaw_state": "owls",
    "kent_state": "golden flashes",
    "kentucky": "wildcats",
    "long_beach_state": "the beach",
    "longwood": "lancers",
    "louisiana": "ragin cajuns",
    "loyola_chicago": "ramblers",
    "lsu": "tigers",
    "marquette": "golden eagles",
    "maryland": "terrapins",
    "memphis": "tigers",
    "miami": "hurricanes",
    "michigan_state": "spartans",
    "michigan": "wolverines",
    "mississippi_state": "bulldogs",
    "missouri": "mizzou",
    "montana_state": "fighting bobcats",
    "murray_state": "racers",
    "nc_state": "wolfpack",
    "new_mexico_state": "aggies",
    "new_orleans": "privateers",
    "norfolk_state": "spartans",
    "north_carolina": "tar heels",
    "north_texas": "mean green",
    "northern_iowa": "panthers",
    "northern_kentucky": "norse",
    "northwestern": "wildcats",
    "notre_dame": "fighting irish",
    "ohio_state": "buckeyes",
    "oral_roberts": "golden eagles",
    "penn_state": "nittany lions",
    "pittsburgh": "panthers",
    "providence": "friars",
    "purdue": "boilmakers",
    "richmond": "spiders",
    "rutgers": "scarlet knights",
    "saint_marys": "gaels",
    "saint_peters": "peacocks",
    "san_diego_state": "aztecs",
    "san_francisco": "dons",
    "seton_hall": "pirates",
    "south_dakota_state": "jackrabbits",
    "southeast_missouri_state": "redhawks",
    "tcu": "horned frogs",
    "tennessee": "volunteers",
    "texas_a&m_cc": "islanders",
    "texas_a&m": "aggies",
    "texas_southern": "tigers",
    "texas_state": "bobcats",
    "texas_tech": "red raiders",
    "texas": "longhorns",
    "toledo": "rockets",
    "uab": "blazers",
    "ucla": "bruins",
    "uconn": "huskies",
    "ucsb": "bison",
    "unc_asheville": "bulldogs",
    "unc_wilmington": "seahawks",
    "usc": "trojans",
    "utah_state": "aggies",
    "vcu": "rams",
    "vermont": "catamounts",
    "villanova": "wildcats",
    "virginia_tech": "hokies",
    "virginia": "cavaliers",
    "wagner": "seahawks",
    "wake_forest": "demon deacons",
    "west_virginia": "mountaineers",
    "wisconsin": "badgers",
    "wright_state": "raiders",
    "wyoming": "cowboys",
    "xavier": "musketeers",
    "yale": "bulldogs",
    "nevada": "wolf pack",
    "princeton": "tigers"
}
region_seeds = {
    "midwest": 1,
    "east": 2,
    "south": 3,
    "west": 4
}

function title(str) {
    return str.replace(/_/g, ' ').replace(/\b\w/g, match => match.toUpperCase());
}

class Team {
    constructor(name, seed) {
        this.name = name;
        this.nickname = nicknames[name];
        this.seed = seed;
        this.pretty_name = title(`${this.name} ${this.nickname}`);
        this.display_name = `${this.seed}. ${this.pretty_name}`;
        this.image_path = `../imgs/${this.name}.jpg`;
    }
}

class EffectiveSeed {
    constructor(effective_seed_idx, teams) {
        this.effective_seed_idx = effective_seed_idx;
        this.teams = teams;
        this.display_name = this.teams.map(team => team.display_name).join(" ");
    }
}

class MatchupPair {
    constructor(top_team, bot_team) {
        this.top_team = top_team;
        this.bot_team = bot_team;
        this.teams = [top_team, bot_team];
        this.current_selection = null;
    }
    
    display() {
        document.querySelector('.match-container').innerHTML = `
            <div class="image-container" onclick="current_region.selectWinner(0)">
                <h3>${this.top_team.display_name}</h3>
                <img src="${this.top_team.image_path}" alt="${this.top_team.display_name}">
                <div class="selection-box" id="selection0"></div>
            </div>
            <div class="image-container" onclick="current_region.selectWinner(1)">
                <h3>${this.bot_team.display_name}</h3>
                <img src="${this.bot_team.image_path}" alt="${this.bot_team.display_name}">
                <div class="selection-box" id="selection1"></div>
            </div>
        `;
    }

    selectWinner(idx) {
        document.getElementById(`selection${idx}`).style.display = 'block';
        document.getElementById(`selection${1-idx}`).style.display = 'none';
        this.current_selection = this.teams[idx];
    }
}

class Matchup {
    constructor(top_seed, bot_seed) {
        this.top_seed = top_seed;
        this.bot_seed = bot_seed;
        // TODO: FIX
        this.possible_matchup_pairs = [
            new MatchupPair(this.top_seed.teams[0], this.bot_seed.teams[0])
        ];
        this.current_matchup_pair_idx = 0;
        this.winners = [];
    }

    selectWinner(idx) {
        this.possible_matchup_pairs[this.current_matchup_pair_idx].selectWinner(idx);
    }

    displayMatchupPair() {
        this.possible_matchup_pairs[this.current_matchup_pair_idx].display();
    }

    submitMatchupPair() {
        let winner = this.possible_matchup_pairs[this.current_matchup_pair_idx].current_selection;
        if (!this.winners.includes(winner)) {
            this.winners.push(winner);
        }
        this.current_matchup_pair_idx++;
    }

    isComplete() {
        return this.current_matchup_pair_idx >= this.possible_matchup_pairs.length;
    }

    getNextEffectiveSeed() {
        return new EffectiveSeed(this.top_seed.effective_seed_idx, this.winners);
    }
}

class Round {
    constructor(round_number, num_seeds) {
        this.round_number = round_number;
        this.num_seeds = num_seeds;
        this.seeds = {};
        for (let i = 1; i <= num_seeds; i++) {
            this.seeds[i] = null;
        }
        this.num_matchups = Math.floor(num_seeds / 2);
        this.matchups = []
        this.current_matchup_idx = null;
    }

    updateHTMLBracket(effective_seed_idx) {
        var dynamicTextSpan = document.getElementById(`rnd${this.round_number}-eSeed${effective_seed_idx}`);
        let effective_seed = this.seeds[effective_seed_idx]
        if (effective_seed == null){
            dynamicTextSpan.textContent = "";
        } else {
            dynamicTextSpan.textContent = effective_seed.display_name;
        }
    }

    initializeMatchups(){
        if (this.matchups.length > 0) {
            return;
        }
        for (let i = 1; i <= this.num_matchups; i++) {
            this.matchups.push(new Matchup(this.seeds[i], this.seeds[this.num_seeds - i + 1]));
        }
        this.current_matchup_idx = 0;
    }

    isReady() {
        for (key in this.seeds) {
            if (this.seeds[key] === null) {
                return false;
            }
        }
        this.initializeMatchups();
        return true;
    }

    addSeed(effective_seed, update_html=true) {
        this.seeds[effective_seed.effective_seed_idx] = effective_seed;
        if (update_html){
            this.updateHTMLBracket(effective_seed.effective_seed_idx);
        }
        return this.isReady()
    }

    setHTML() {
        for (key in this.seeds) {
            this.updateHTMLBracket(key);
        }
    }

    selectWinner(idx) {
        this.matchups[this.current_matchup_idx].selectWinner(idx);
    }

    displayMatchup() {
        this.matchups[this.current_matchup_idx].displayMatchupPair();
    }

    submitMatchup() {
        let matchup = this.matchups[this.current_matchup_idx];
        matchup.submitMatchupPair();
        if (matchup.isComplete()) {
            this.current_matchup_idx++;
            return matchup.getNextEffectiveSeed();
        }

        return null;
    }

    isComplete() {
        for (key in this.matchups) {
            if (this.matchups[key] === null) {
                return false;
            }
            if (!this.matchups[key].isComplete()) {
                return false;
            }
        }
        return true;
    }
}

class RegionBracket {
    constructor(region_name, num_rounds) {
        this.region_name = region_name;
        this.num_rounds = num_rounds;
        this.rounds = {};
        for (let i = 1; i <= num_rounds; i++) {
            let num_seeds = 2 ** (num_rounds - i + 1);
            this.rounds[i] = new Round(i, num_seeds);
        }
        this.current_round_idx = 1;
        this.region_winner = null;
    }

    addSeed(effective_seed, update_html=true) {
        this.rounds[this.current_round_idx].addSeed(effective_seed, update_html);
    }

    setHTML() {
        for (key in this.rounds) {
            this.rounds[key].setHTML();
        }
    }

    selectWinner(idx) {
        this.rounds[this.current_round_idx].selectWinner(idx);
    }

    displayWinner() {
        if (this.region_name == "final_four") {
            document.querySelector('.match-container').innerHTML = `<h2>Your overall winner is ${this.region_winner.display_name}!</h2>`;

        } else {
            document.querySelector('.match-container').innerHTML = `<h2>Your winner of the ${title(this.region_name)} is ${this.region_winner.display_name}!</h2>`;
        }
        // TODO
    }

    isComplete() {
        for (key in this.rounds) {
            if (!this.rounds[key].isComplete()) {
                return false;
            }
        }
        return true;
    }

    displayChoice(){
        if (this.isComplete()){
            this.displayWinner()
        } else if (!this.rounds[this.current_round_idx].isReady()) {
            document.querySelector('.match-container').innerHTML = `<h2>Please complete other regions first.</h2>`;
        } else {
            this.rounds[this.current_round_idx].displayMatchup()
        }
    }

    setRegionWinner(winner) {
        this.region_winner = winner;

        var dynamicTextSpan = document.getElementById(`region-winner`);
        dynamicTextSpan.textContent = this.region_winner.display_name;

        if (this.region_name != "final_four") {
            let effective_seed = new EffectiveSeed(region_seeds[this.region_name], winner.teams);
            brackets["final_four"].addSeed(effective_seed, false)
        }
    }

    submitChoice() {
        let current_round = this.rounds[this.current_round_idx];
        let winner = current_round.submitMatchup();
        if (winner != null) {
            if (this.current_round_idx < this.num_rounds) {
                // Add winner to next round
                this.rounds[this.current_round_idx + 1].addSeed(winner);
            } else {
                this.setRegionWinner(winner)
            }
        }
        if (current_round.isComplete()) {
            this.current_round_idx++;
        }

        this.displayChoice()
    }
}

brackets = {
    "east": new RegionBracket("east", 4),
    "west": new RegionBracket("west", 4),
    "midwest": new RegionBracket("midwest", 4),
    "south": new RegionBracket("south", 4),
    "final_four": new RegionBracket("final_four", 2),
}

function initialize_effective_seed(team_names, seed) {
    if (typeof team_names === 'string') {
        team_names = [team_names];
    }
    let teams = team_names.map(team_name => new Team(team_name, seed));
    return new EffectiveSeed(seed, teams);
}

function initialize() {
    for (key in bracket_data) {
        let region_bracket = brackets[key];
        let region_data = bracket_data[key];
        for (let i=0; i<region_data.length; i++) {
            team_names = region_data[i];
            seed = i + 1;
            region_bracket.addSeed(initialize_effective_seed(team_names, seed), false);
        }
    }
}

function updateRegion(region_name) {
    current_region = brackets[region_name];
    var regions_bracket = document.getElementById('regions-bracket');
    var final_four_bracket = document.getElementById('final-four-bracket');

    if (region_name == "final_four") {
        regions_bracket.classList.add("hidden");
        final_four_bracket.classList.remove("hidden");
    } else {
        final_four_bracket.classList.add("hidden");
        regions_bracket.classList.remove("hidden");
    }
    current_region.setHTML();
    current_region.displayChoice();
}

current_region = null;

window.onload = function() {
    initialize();
    updateRegion("east");
};