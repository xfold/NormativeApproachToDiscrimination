
CONFIG = {
    'I': ['MaritalStatus', 'LegalStatus'],  
    'P': ['Sex_Code_Text', 'Ethnic_Code_Text'],                           
    'PNU': [],                                      
    'O': 'ScoreText'                                    
}


EXCEPTIONS = {
    'Explicit' : [],
    'Implicit' : [],
    'Indirect' : []
    
}
    

#this variable sets up the maximum combinations of columns that will be combined as a single new column to attest
#proxy correlations between input and output variables in ImplicitDiscrimination.
#suppose a dataset with Input (I) columns 'a', 'b' and 'c'. By setting '_max_proxy_colum_combo_size = 2', the system will only
#explore all combos of max size 2, i.e. 'a+b', 'a+c', 'b+c'
_ImplicitDiscrimination_max_proxy_combo_size = 3    
    
#proxy correlation threshold for normalized_mutual_info_score \in [0,1] (0 non-correlated, 1 correlated)
#this threshold indicates the threshold to consider if two sets of features are correlated or not, considering
#normalised MI
_ImplicitDiscrimination_min_corr = 0.6
#The value x ∈ [0, 1] is a constant representing the disproportion allowed in a particular domain
_IndirectDiscrimination_Threshold = 0.8
#Minimum p-value to consider any indirect discrimination findings. Only results with lower p-values will be considered
_IndirectDiscrimination_MinPValue = 0.05


