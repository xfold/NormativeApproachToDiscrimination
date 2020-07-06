
#
# DATASET
#
# All elements in the are string or lists of strings that correspond with the columns of the dataset.
# [I] : Input variables (non-protected variables)
# [P] : Protected columns  
# [PNU] : Protected variables Not Used in the system
# [O] : Output column
#
CONFIG = {
    'I': [],
    'P': [],                           
    'PNU': [],                                      
    'O': ''                                    
}


#
# EXCEPTIONS
#
# [Explicit]
# Name of the protected columns you want to ignore as explicit discrimination exceptions. 
# It should be a list of strings corresponding with the Protected columns to ignore.
# e.g.
#     >>Exceptions_Explicit = ['gender', 'ethnicity']   
# 
# [Implicit]
# Name of the Input column or columns which, alone or combined, you want to add as Exceptions for proxy input variables.
# That is, ignore any of the input variables (or combinations of them) that act as a proxy for an specific protected attribute.
#     >>Exceptions_Implicit (1 column)= 
#         [{'I':['input_column_1'], 'P'='protected_column_name' } ]
#     >>Exceptions_Implicit (2 columns)= 
#         [{'I':['input_column_1', 'input_column_2'], 'P'='protected_column_name' } ]
# e.g.
#     >>[{'I':['strength', 'age'], 'P'='gender' } ]
# 
# [Indirect]
# Indirect exceptions are defined as:
#     list< {'P': <str>, 'Pv':(<str>,<str>), 'O':<str>, 'Ov':<str>} > 
#     where:
#         P : protected variable (name of the column)
#         Pv:(<str>,<str>). Tuple with the values that define the two subpopulations from P, (values of column P to compare)
#         O : output variable (name of the column)
#         Ov: output value from O (value of the output O)
# e.g.
#     >>[{'P':'ethnicity', 'Pv':('white', 'caucasian'), 'O':'salary', 'Ov':'>50k']
# >>
EXCEPTIONS = {
    'Explicit' : [],
    'Implicit' : [],
    'Indirect' : []
    
}

#
# THRESHOLDS and CONFIG
#
# This variable sets up the maximum combinations of columns that will be combined as a single new column to attest
#proxy correlations between input and output variables in ImplicitDiscrimination.
#e.g. suppose a dataset with Input (I) columns 'a', 'b' and 'c'. By setting '_max_proxy_colum_combo_size = 2', the system will only
#explore all column combos of max size 2, i.e. 'a', 'b', 'c', 'a+b', 'a+c', 'b+c'
_ImplicitDiscrimination_max_proxy_combo_size = 3    

# Proxy correlation threshold for normalized_mutual_info_score \in [0,1] (0 non-correlated, 1 correlated)
#this threshold indicates the threshold to consider if two sets of features are correlated or not, considering
#normalised MI
_ImplicitDiscrimination_min_corr = 0.6

# The value x ∈ [0, 1] is a constant representing the disproportion allowed in a particular domain. Minim threshold for indirect discrimination
_IndirectDiscrimination_Threshold = 0.8

# Minimum p-value to consider any indirect discrimiantion findings. Results with higher p-values will be ignored.
_IndirectDiscrimination_MinPValue = 0.05


