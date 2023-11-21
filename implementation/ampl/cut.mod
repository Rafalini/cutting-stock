# ----------------------------------------
# CUTTING STOCK USING PATTERNS
# ----------------------------------------
param bar_width > 0;          # width of raw bars [.dat]
set WIDTHS;                   # set of widths to be cut [.dat]
param maxRelax {WIDTHS};	  # ma relaxation percentage [.dat]
param orders {WIDTHS} > 0;    # number of each width to be cut [.dat]
param nPAT integer >= 0;      # number of patterns
set PATTERNS := 1..nPAT;      # set of patterns
param wfep {WIDTHS,PATTERNS} integer >= 0;	#widths for each pattern
				                            # defn of patterns: nbr[i,j] = number
				                            # of bars of width i in pattern j
                            
param rfep {WIDTHS,PATTERNS} integer >= 0;	#relax for each pattern
											#only for display purposes
var Cut {PATTERNS} integer >= 0;   # bars cut using each pattern
minimize Number:                   # minimize total raw bars cut
   sum {j in PATTERNS} Cut[j];
subj to Fill {i in WIDTHS}:
   sum {j in PATTERNS} wfep[i,j] * Cut[j] >= orders[i];
                                   # for each width, total
                                   # bars cut meets total orders
   
# ----------------------------------------
# KNAPSACK SUBPROBLEM WITH RELAXATION
# ----------------------------------------
param relax_cost default 0.00000001;
param price {WIDTHS} default 0.0;
var Use {WIDTHS} integer >= 0;
var Relax {WIDTHS} integer >= 0;

maximize Reduced_Cost:
   sum {i in WIDTHS} (price[i] * Use[i] - Relax[i] * relax_cost) - 1;
subj to Width_Limit:
   sum {i in WIDTHS} (i * Use[i] - Relax[i]) <= bar_width;
subj to Relax_Limit {i in WIDTHS}:
	Relax[i] <= maxRelax[i]*Use[i];