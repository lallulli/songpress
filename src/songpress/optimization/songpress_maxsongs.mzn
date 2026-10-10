%%%%%%%%%%%%%%
% Parameters %
%%%%%%%%%%%%%%

int: n_blocks;
int: n_songs;
int: column_height;
int: column_module;
int: empty_starting_columns; % in 0..column_module - 1
int: min_isolated_block_height;
int: ub; % Upper bound on the number of columns (from a greedy solution)
% dfloat: beta = 1.2;

set of int: BLOCKS = 1..n_blocks;
set of int: BLOCKS_0 = 0..n_blocks;
set of int: COLUMNS = 1..ub;
set of int: SONGS = 1..n_songs;

array[BLOCKS] of BLOCKS_0: previous;
array[BLOCKS] of int: height;
array[BLOCKS] of SONGS: song;


% Lower bound on the number of columns: total height over column height
int: lb = (sum(height) + column_height - 1) div column_height;

% Derivative: song height
array[SONGS] of int: song_height = [sum(b in BLOCKS where song[b] = s)(height[b]) | s in SONGS];
% Value of a song: its height, plus a superlinear bonus that favors bulky songs
% array[SONGS] of int: value = [song_height[s] + beta * song_height[s] * song_height[s] div column_height | s in SONGS];


%%%%%%%%%%%%%
% Variables %
%%%%%%%%%%%%%

array[BLOCKS] of var COLUMNS: column;
array[BLOCKS] of var bool: first; % First block of a column
array[SONGS] of var bool: selected;


%%%%%%%%%%%%%%%%%%%%%%
% Objective function %
%%%%%%%%%%%%%%%%%%%%%%


% Main terms: number of selected blocks and songs

var 0..n_blocks: selected_blocks :: output = sum(i in BLOCKS)(selected[song[i]]);
var 0..n_songs: selected_songs :: output = sum(i in SONGS)(selected[i]);

% Preferred term: column start with first block of a song

var int: clean_columns :: output = (column_height div 6) * sum(b in BLOCKS where previous[b] == 0)(first[b]);


% solve maximize 5 * selected_songs + 3 * selected_blocks + clean_columns;
solve maximize sum(s in SONGS)(selected[s] * song_height[s]) + clean_columns;


%%%%%%%%%%%%%%%
% Constraints %
%%%%%%%%%%%%%%%

%% Total block height of blocks assigned to each column does not exceed max value

constraint forall(c in COLUMNS)(
  sum(b in BLOCKS)((selected[song[b]] /\ column[b] == c) * height[b]) <= column_height
);


%% Each block has a predecessor on the same column, max 1 per column can be wrapped unless for column 0 mod column_module

constraint forall(b in BLOCKS where previous[b] > 0)( selected[song[b]] -> (
  (column[previous[b]] == column[b])
  \/
  (first[b] /\ (column[previous[b]] == column[b] - 1) /\ (column[b] mod column_module != (empty_starting_columns + 1) mod column_module))
));

%% Small blocks cannot be isolated in a page

constraint forall(b in BLOCKS where previous[b] > 0 /\ previous[previous[b]] == 0)(
  selected[song[b]] -> ((column[previous[b]] < column[b]) -> (height[previous[b]] >= min_isolated_block_height))
);

%% Each column has at most 1 first block

constraint forall(c in COLUMNS)(
  sum(b in BLOCKS)((selected[song[b]] /\ column[b] == c) * first[b]) <= 1
);

% A song that takes more than 2 columns must not be interleaved with other songs
constraint forall(i, j, k in BLOCKS where i < k /\ song[i] = song[k])(
  (selected[song[i]] /\ selected[song[j]] /\ column[i] < column[j] /\ column[j] < column[k]) -> song[j] = song[k]
);



