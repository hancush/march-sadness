var east = [];
var west = [];
var midwest = [];
var south = [];
var matchups;
var secret_sauce;

$.get('static/data/teams.json', function(data) {
    $.each(data, function(i, team) {
      var region = get_region(team);

      if ( region == 'south' ) {
        south.push(team);
      } else if ( region == 'west' ) {
        west.push(team);
      } else if ( region == 'east' ) {
        east.push(team);
      } else if ( region == 'midwest' ) {
        midwest.push(team);
      }
    });
  }
);

function get_region(team) {
  if ( team.sl <= 15 ) {
    return 'east';
  } else if ( team.sl <= 31 ) {
    return 'west';
  } else if ( team.sl <= 47 ) {
    return 'south';
  } else if ( team.sl <= 63 ) {
    return 'midwest';
  }
}

function reset_matchups() {
  matchups = [
    [1, 16],
    [8, 9],
    [5, 12],
    [4, 13],
    [6, 11],
    [3, 14],
    [7, 10],
    [2, 15],
  ];
}

function update_matchups(remaining_seeds) {
  matchups = [];
  for ( i = 0; i < remaining_seeds.length; i += 2 ) {
    matchups.push(remaining_seeds.slice(i, i + 2));
  }
}

function get_seed_from_region(region, seed) {
  var team = region.filter(function(team) { return team.s == seed });
  return team[0];
}

function compare_region(region) {
  var remaining_seeds = [];
  var remaining_teams = [];

  $.each(matchups, function(i, seeds) {
    var team1 = get_seed_from_region(region, seeds[0]);
    var team2 = get_seed_from_region(region, seeds[1]);
    var victor = compare_teams(team1, team2);

    var element = '#' + get_region(victor) + '-' + (matchups.length * 2);
    render_matchup(team1, team2, victor, element);

    remaining_seeds.push(victor.s);
    remaining_teams.push(victor);
  });

  update_matchups(remaining_seeds);

  return remaining_teams;
}

function compare_teams(team1, team2) {
  var too_close_for_science = Math.abs(team1.bpi - team2.bpi) < 15;

  if ( too_close_for_science ) {
    return compare_colors(secret_sauce, team1, team2);
  } else {
    return compare_bpi(team1, team2);
  }
}

function compare_colors(base_color, team1, team2) {
  function color_sort(a, b) {
    var color_a = a.c ? a.c : '000000';
    var color_b = a.c ? a.c : '000000';

    return chroma.distance(base_color, color_a) - chroma.distance(base_color, color_b);
  }

  // order teams by color distance
  var ordered = [team1, team2].sort(color_sort);

  return ordered[0];
}

function compare_bpi(team1, team2) {
  // order teams by bpi ranking
  var ordered = [team1, team2].sort(function(a, b) { return a.bpi - b.bpi });

  // return underdog a quarter of the time
  var underdog = Math.random() <= 0.33;

  if ( underdog ) {
    return ordered[1];
  } else {
    return ordered[0];
  }
}

function render_matchup(team1, team2, victor, element) {
  $(element).append(`
    <div class="matchup">
      <p>
        ${ team1.s} ${ team1.n } v. ${ team2.s } ${ team2.n }<br />
        <strong>WINNER</strong>: ${ victor.n }
      </p>
    </div>
  `);
}

function run(color) {
  secret_sauce = color;

  $('div.result').empty();
  $('#the-good-stuff').show();

  var regions = [south, west, east, midwest];
  var regional_champs = [];

  $.each(regions, function(i, region) {
    reset_matchups();
    region = region;
    while ( region.length > 1 ) {
      region = compare_region(region);
    }
    regional_champs.push(region[0]);
  })

  // order: south, west, east, midwest
  var final_four = regional_champs.sort(function(a, b) { return a.sl - b.sl });

  var left = compare_teams(final_four[0], final_four[1]);
  var right = compare_teams(final_four[2], final_four[3]);

  render_matchup(final_four[0], final_four[1], left, '#final-4');
  render_matchup(final_four[2], final_four[3], right, '#final-4');

  var national_champ = compare_teams(left, right);

  render_matchup(left, right, national_champ, '#final-2');

  $('#champion').append(`
    <div>
      <h2><strong>🎊 ${ national_champ.n } 🎊</strong></h2>
      <h3>
        #${ national_champ.s } in the ${ get_region(national_champ) }<br />
        #1 in the country<br />
        #1 in your heart<br />
        (for the next month)
      </h3>
  `)
}
