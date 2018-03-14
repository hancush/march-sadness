var east = [];
var west = [];
var midwest = [];
var south = [];

$.get('static/data/teams.json', function(data) {
    $.each(data, function(i, team) {
      if ( team.sl <= 15 ) {
        east.push(team);
      } else if ( team.sl <= 31 ) {
        west.push(team);
      } else if ( team.sl <= 47 ) {
        midwest.push(team);
      } else if ( team.sl <= 63 ) {
        south.push(team);
      }
    });
  }
);

var matchups = [
    [1, 16],
    [2, 15],
    [3, 14],
    [4, 13],
    [5, 12],
    [6, 11],
    [7, 10],
    [8, 9],
];

function get_seed_from_region(region, seed) {
    var team = region.filter(function(team) { return team.s == seed });
    return team[0];
}

function compare_region(region) {
    $.each(matchups, function(i, seeds) {
        team1 = get_seed_from_region(region, seeds[0]);
        team2 = get_seed_from_region(region, seeds[1]);
        console.log(compare_teams(team1, team2));
    });
}

function compare_teams(team1, team2) {
  var too_close_for_science = Math.abs(team1.bpi - team2.bpi) < 10;

  if ( too_close_for_science ) {
    return compare_colors('yellow', team1, team2);
  } else {
    return compare_bpi(team1, team2);
  }
}

function compare_colors(base_color, team1, team2) {
  var color_sort = function(a, b) {
    return chroma.distance(base_color, a.c) - chroma.distance(base_color, b.c);
  }

  // order teams by color distance
  var ordered = [team1, team2].sort(color_sort);

  return ordered[0];
}

function compare_bpi(team1, team2) {
  // order teams by bpi ranking
  var ordered = [team1, team2].sort(function(a, b) {return a.bpi - b.bpi});

  // return underdog a quarter of the time
  var underdog = Math.random() <= 0.25;

  if ( underdog ) {
    return ordered[1];
  } else {
    return ordered[0];
  }
}
