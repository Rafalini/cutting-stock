# ----------------------------------------
# CUTTING STOCK USING PATTERNS
# ----------------------------------------
param rawBarWidth > 0;        	# width of raw bars [.dat]
set ORDERS;                   	# set of widths to be cut [.dat]
param widths {ORDERS} > 0;		# width of ordered bars [.dat]
param barsNum {ORDERS} > 0;    	# number of each width to be cut [.dat]
param maxRelax {ORDERS};	  	# max relaxation percentage [.dat]
param nPAT integer >= 0;      	# number of patterns
set PATTERNS := 1..nPAT;      	# set of patterns
param wfep {ORDERS,PATTERNS} integer >= 0;	#widths for each pattern
				                            # defn of patterns: nbr[i,j] = number
				                            # of bars of width i in pattern j
param rfep {ORDERS,PATTERNS} integer >= 0;	#relax for each pattern
											#only for display purposes
var Cut {PATTERNS} integer >= 0;	# bars cut using each pattern
minimize Number:					# minimize total raw bars cut
	sum {j in PATTERNS} Cut[j];
subj to Fill {i in ORDERS}:			#bars cut meets total orders
	sum {j in PATTERNS} wfep[i,j] * Cut[j] >= barsNum[i];
							
   
# ----------------------------------------
# KNAPSACK SUBPROBLEM WITH RELAXATION
# ----------------------------------------
param relaxCost default 0.00000001;
param price {ORDERS} default 0.0;
var Use {ORDERS} integer >= 0;
var Relax {ORDERS} integer >= 0;

maximize ReducedCost:
   sum {i in ORDERS} (price[i] * Use[i] - Relax[i] * relaxCost) - 1;
subj to WidthLimit:
   sum {i in ORDERS} (widths[i] * Use[i] - Relax[i]) <= rawBarWidth;
subj to RelaxLimit {i in ORDERS}:
	Relax[i] <= maxRelax[i]*Use[i];