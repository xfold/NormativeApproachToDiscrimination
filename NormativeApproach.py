#ignore sklearn future warnings
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd
import numpy as np
import importlib.util
from sklearn.metrics.cluster import normalized_mutual_info_score
from itertools import combinations
import itertools
from scipy import stats
import pprint

class NormativeApproachDiscrimination():
    def __init__(self, csv_path_dataset, config_py_path, verbose = False):
        '''
        Initialise a NormativeApproachDiscrimination object.
        Input:
        csv_path_dataset : <str> . csv dataset, in which the first row are the columns
        config_py_path : <str> . python configuration file for the dataset
        verbose : <bool> . 
        '''
        self.df  = pd.read_csv(csv_path_dataset,sep=',', header=0)
        self.verbose = verbose
        
        #import the specified config py file
        spec = importlib.util.spec_from_file_location("module.name", config_py_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        self.config = config.CONFIG
        self.exceptions = config.EXCEPTIONS
        #minimum correlation for a variable to be considered a proxy
        self._ImplicitDiscrimination_min_corr = config._ImplicitDiscrimination_min_corr
        self._ImplicitDiscrimination_Max_proxy_combo_size = config._ImplicitDiscrimination_max_proxy_combo_size
        self._IndirectDiscrimination_min_prop = config._IndirectDiscrimination_Threshold
        self._IndirectDiscrimination_min_pvalue = config._IndirectDiscrimination_MinPValue
        
        
    def CheckExplicitDiscrimination(self, df, P, E):
        '''
        Checks for cases of explicit discrimination, given a set of I, P and Exceptions E
        
        Input:
        df: dataset dataframe
        P : list<str> . protected attributes as column names
        E : list<str> . Set of exceptions consisting in protected column names
        Returns:
        candidate_explicit_errors : list<str> . List of explicit discrimination violations
        '''
        candidate_explicit_errors = list( set(P) - set(E))
        return candidate_explicit_errors
    
    def _CoveredByImplicitException(self, implicit_candidate_case, E_Implicit):
        '''
        Checks whether the candidate for implicit discrimination tuple is covered
        by any of the explicit discrimination exceptions. If it is, returns True; returns False otherwise
        
        Input:
        implicit_candidate_case : candidate case of implicit discrimination, of the form
            {'I': list<str>, 'P': str, 'value': int }
            where:
                I : List of inputs columns related with possible implicit discrimination
                P : protected column related with possible implicit discrimination
                value : unused 
        E : List of implicit exceptions, [{'I': list<str>, 'P'=str }]
        Returns:
        True, if an exception covers the possible case of implict discrimination;
        False, otherwise
        '''
        for ex in E_Implicit:
            if(implicit_candidate_case['I'] == ex['I'] and implicit_candidate_case['P'] == ex['P']):
                return True
        return False
            
    
    def CheckImplicitDiscrimination(self, df, I, P, E, proxy_corr_threshold, max_comb_size = None):
        '''
        This function checks implicit discrimination between dataframe protected columns P and input columns I,
        that is not covered by the defined exceptions.
        If any correlation above the set threshold 'proxy_corr_threshold' is found, it returns a warning/error
        Input:
        df: dataset dataframe
        I : list<str> . input attributes as column names
        P : list<str> . protected attributes as column names
        E : list<str> . Set of exceptions consisting in protected column names
        proxy_corr_threshold : float \in [0,1] . Defines the min threshold to consider proxy correlation
        Returns:
        candidate_implicit_errors : list<{'I': list<str>, 'P': <str>, 'value': <float>}> . 
            List of explicit discrimination violations, where value is the strength of the correaltion between I and P
        '''
        #first set the maximum size for combination of columns if it's not been set already
        if(max_comb_size is None):
            max_comb_size = len(I)+1
        else:
            if(max_comb_size > len(I)):
                max_comb_size = len(I)
            max_comb_size+=1
            
        
        #generate combined proxy columns and update the df
        newcols = sum([list(map(list, combinations(I, i))) for i in range(max_comb_size)], [])   
        newcols = [x for x in newcols if len(x)>1]
        df_aux = df.copy()
        for newcol in newcols:
            df_aux['+'.join(newcol)] = df_aux[newcol].agg('_'.join, axis=1)

        #consider new created columns as new inputs to check whether they are proxies for protected variables
        I = I+['+'.join(newcol) for newcol in newcols]
        factors_paired = [(i,j) for i in I for j in P] 
        nmi_values =[]
        for f in factors_paired:
            if f[0] != f[1]:
                res = normalized_mutual_info_score(df_aux[f[0]].tolist(), df_aux[f[1]].tolist()) 
                nmi_values.append(res)
            else:      
                nmi_values.append(0)
                
        nmi_values = np.array(nmi_values).reshape( (len(I), len(P)) ) # shape it as a matrix
        nmi_values = pd.DataFrame(nmi_values, index = I, columns=P)   # then to a df for convenience  
        
        if(self.verbose):
            print('[Mutual Information correlation between Input and Protected columns:]')
            print('implicit correlation threshold: {}'.format(proxy_corr_threshold))
            print(nmi_values)
            print()
        
        #collect all index, column pairs that satisfy the min proxy proxy_corr_threshold threshold
        candidate_implicit_errors = []
        for index, row in nmi_values.iterrows():
            p_corr_c = row[row.gt(proxy_corr_threshold)]
            if(len(p_corr_c) == 0):
                continue
            for case in list(zip(p_corr_c.index.tolist(), p_corr_c.tolist())): 
                index_t = index.split('+')
                implicit_candidate_case =  {'I':index_t, 
                                            'P':case[0], 
                                            'corr':round(case[1], 4)}
                if( not(self._CoveredByImplicitException(implicit_candidate_case, E)) ):
                    candidate_implicit_errors.append( implicit_candidate_case )
            
        return candidate_implicit_errors
    
    def _CoveredByIndirectException(self, indirect_candidate_discr, E_Indirect):
        '''
        Checks whether the candidate for indirect discrimination tuple is covered
        by any of the indirect discrimination exceptions. If it is, returns True; returns False otherwise
        
        Input:
        indirect_candidate_discr : candidate case of indirect discrimination, of the form
            list< {'P': <str>, 'Pv':(<str>,<str>), 'O':<str>, 'Ov':<str>, 'ratio':<float>} > 
            (see below)
        E : list< {'P': <str>, 'Pv':(<str>,<str>), 'O':<str>, 'Ov':<str>} > 
            where:
                P : protected variable
                Pv:(<str>,<str>) . Tuple with the values that define the two subpopulations from P
                O : output variable
                Ov: output value from O
        Returns:
        True, if an exception covers the possible case of implict discrimination;
        False, otherwise
        '''
        for ex in E_Indirect:
            if(indirect_candidate_discr['P'] == ex['P'] and \
               indirect_candidate_discr['Pv'] == ex['Pv'] and \
               indirect_candidate_discr['O'] == ex['O'] and \
               indirect_candidate_discr['Ov'] == ex['Ov']):
                return True
        return False
    
    
    def CheckIndirectDiscrimination(self, df, P, O, E, ID_proportion, ID_minpval = 0.05):
        '''
        This function checks for indirect discrimination between dataframe protected columns P and output column O,
        that is not covered by the defined exceptions.
        If any correlation above the set threshold 'proxy_corr_threshold' is found, it returns a warning/error
        Input:
        df: dataset dataframe        
        P : list<str> . protected attributes as column names
        O : <str> . output column name
        E : list< {'P': <str>, 'Pv':(<str>,<str>), 'O':<str>, 'Ov':<str>} > 
            where:
                P : protected variable
                Pv:(<str>,<str>) . Tuple with the values that define the two subpopulations from P
                O : output variable
                Ov: output value from O
        ID_proportion : float \in [0,1] . Defines the min proportion to consider ID
        Returns:
        candidate_indirect_errors : list<{'P': <str>, 
                                        'Pv': (<str>, <str>), 
                                        'O' : <str>,
                                        'Ov': <str>,
                                        'ratio': <float> (or Inf)
                                        }>
            List of explicit indirect discrimination violations, where P is the protected column name
            Pv the two subpoulations extracted from P values, O is the output column name,
            Ov is the output column value from which both subpopulations where compared,
            and ratio is the proportion between how many persons obtained output Ov between Pv1 and Pv2.
        '''
        #prepare all possible outputs to compare
        o_df_values = list(set(df[O].tolist()))  

        #check, for every protected variable, if there exist disparate impact with any of the possible  
        #combinations of the output
        candidate_indirect_errors = []
        for p in P:
            #prepare all sets and possible combinations of populations and outputs to check
            p_df_values = list(set(df[p].tolist()))
            p_df_values_comb = list(itertools.combinations(p_df_values, 2))
            for sub1, sub2 in p_df_values_comb:
                for o_df_value in o_df_values:
                    v1a = len(df[ (df[p] == sub1) & (df[O] == o_df_value) ]) / len(df[df[p] == sub1])
                    v2a = len(df[ (df[p] == sub2) & (df[O] == o_df_value) ]) / len(df[df[p] == sub2])
                    if( v1a*ID_proportion > v2a ):
                        #chi2 comparing both subgroups for all output values O to obtain 
                        #explanation on how significant are findings
                        npd = df[(df[p].isin([sub1, sub2]))]
                        contingency_table = pd.crosstab(npd[p],npd[O],margins = True)
                        c1 = contingency_table.iloc[0][0:len(contingency_table.columns)-1].values
                        c2 = contingency_table.iloc[1][0:len(contingency_table.columns)-1].values
                        f_obs = np.array([c1,c2])
                        chi2, p_value, degrees_freedom = stats.chi2_contingency(np.array(f_obs))[:3]
                        
                        if(p_value < ID_minpval):
                            indirect_candidate_discr = {
                                'P' : p.strip(),
                                'Pv': (sub1.strip(), sub2.strip()),
                                'O' : O.strip(),
                                'Ov': o_df_value.strip(),
                                'ratio': np.Inf if v2a==0 else round(v1a/v2a, 4),
                                'chi2': {'pvalue': p_value, 'chi2':chi2, 'degrees_freedom': degrees_freedom}
                            }
                            if( not(self._CoveredByIndirectException(indirect_candidate_discr, E)) ):
                                candidate_indirect_errors.append(indirect_candidate_discr)

        return candidate_indirect_errors
            
    
    def Run(self):
        '''
        Main function for the normative approach, checks the dataset and information set up when configuring the 
        main object and returns a dictionary of the different violations of discrimination rules, if any.
        
        returns:
        dictionary of discrimination violations:
        {
            'Ve': Explicit Discimirnation violations,
            'Vi': Implicit violations,
            'Vd': IndirectDiscrimination violations
        }
        '''
        #input sanity check
        require_columns = self.config['I'] + self.config['P'] + [self.config['O']]
        if( len(set(self.config['I'])) != len(self.config['I']) or \
           len(set(self.config['P'])) != len(self.config['P'])):
            raise ValueError('I and/or P variables contain duplicated columns')
        if(len(set(require_columns)) != len(require_columns)):
            raise ValueError('I,P,O variables contain repeated columns')
        if(not( set(require_columns).issubset(set(self.df.columns)) )):
            raise ValueError('Dataset column names do not correspond with I,P,O variables set in config {}'.format(require_columns))
        if(len(self.config['I']) > 5):
            print('''
        [!] Warning, the dataset contains many columns, please beware it may take a long time generating combinations of 
        columns to identify proxies between Input and Protected variables to attest Implicit Discrimination. 
        Consider setting 'max_comb_size' to a small number (e.g. 3 or smaller).
                ''')
        
        
        tor = {'Ve': [], 'Vi':[], 'Vd':[]}
        #Attesting Direct Discrimination (protected variables used as input P)
        tor['Ve'] = self.CheckExplicitDiscrimination(self.df, 
                                                     self.config['P'], 
                                                     self.exceptions['Explicit'])
        
        #Attesting Implicit Discrimination (proxy variables in I vs P)
        tor['Vi'] = self.CheckImplicitDiscrimination(self.df, 
                                                     self.config['I'], 
                                                     self.config['P'], 
                                                     self.exceptions['Implicit'], 
                                                     self._ImplicitDiscrimination_min_corr,
                                                     max_comb_size = self._ImplicitDiscrimination_Max_proxy_combo_size)
            
        #Attesting Indirect Discrimination (disparate impact)
        tor['Vd'] = self.CheckIndirectDiscrimination(self.df, 
                                                     self.config['P'], 
                                                     self.config['O'], 
                                                     self.exceptions['Indirect'], 
                                                     self._IndirectDiscrimination_min_prop,
                                                     self._IndirectDiscrimination_min_pvalue)
        
        if(self.verbose):
            pprint.pprint(tor)
        return tor