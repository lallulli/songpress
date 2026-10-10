%%%%%%%%%%%%%%
% Parameters %
%%%%%%%%%%%%%%

int: n_blocks;
int: column_height;
int: column_module;
int: empty_starting_columns; % in 0..column_module - 1
int: min_isolated_block_height;
int: ub; % Upper bound on the number of columns (from a greedy solution)

set of int: BLOCKS = 1..n_blocks;
set of int: BLOCKS_0 = 0..n_blocks;
set of int: COLUMNS = 1..ub;

array[BLOCKS] of BLOCKS_0: previous;
array[BLOCKS] of int: height;

% Lower bound on the number of columns: total height over column height
int: lb = (sum(height) + column_height - 1) div column_height;


%%%%%%%%%%%%%
% Variables %
%%%%%%%%%%%%%

array[BLOCKS] of var COLUMNS: column;
array[BLOCKS] of var bool: first; % First block of a column


%%%%%%%%%%%%%%%%%%%%%%
% Objective function %
%%%%%%%%%%%%%%%%%%%%%%


% Main term: number of generated columns

var lb..ub: max_column :: output = max(i in BLOCKS)(column[i]);


% Preferred term: column start with first block of a song

var int: clean_columns :: output = sum(b in BLOCKS where previous[b] == 0)(first[b]);


solve minimize max_column;
% solve minimize 20 * max_column - clean_columns;



%%%%%%%%%%%%%%%
% Constraints %
%%%%%%%%%%%%%%%

%% Total block height of blocks assigned to each column does not exceed max value

constraint forall(c in COLUMNS)(
  sum(b in BLOCKS)((column[b] == c) * height[b]) <= column_height
);


%% Each block has a predecessor on the same column, max 1 per column can be wrapped unless for column 0 mod column_module

constraint forall(b in BLOCKS where previous[b] > 0)(
  (column[previous[b]] == column[b])
  \/
  (first[b] /\ column[previous[b]] == column[b] - 1 /\ (column[b] mod column_module != empty_starting_columns))
);

%% Small blocks cannot be isolated in a page

constraint forall(b in BLOCKS where previous[b] > 0 /\ previous[previous[b]] == 0)(
  (column[previous[b]] < column[b]) -> (height[previous[b]] >= min_isolated_block_height)
);

%% Each column has at most 1 first block

constraint forall(c in COLUMNS)(
  sum(b in BLOCKS)((column[b] == c) * first[b]) <= 1
);




