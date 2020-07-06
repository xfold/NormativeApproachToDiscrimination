# A Normative approach to Attest Digital Discrimination
This repository contains the source code of the original paper ['A Normative approach to Attest Digital Discrimination']() accepted in AI4EQ Workshop of ECAI 2020, and is part of the project [Discovering and Attesting Digital Discrimination (DADD)](http://dadd-project.org/). 

Abstract.
> Digital discrimination is a form of discrimination whereby users are automatically treated unfairly, unethically or just differently based on their personal data by a machine learning (ML) system. Examples of digital discrimination include low-income neighborhood’s targeted with high-interest loans or low credit scores, and women being undervalued by 21% in online marketing. Recently, different techniques and tools have been proposed to detect biases that may lead to digital discrimination. These tools often require technical expertise to be executed and for their results to be interpreted. To allow non-technical users to benefit from ML, simpler notions and concepts to represent and reason about digital discrimination are needed. In this paper, we use norms as an abstraction to represent different situations that may lead to digital discrimination. In particular, we formalise non-discrimination norms in the context of ML systems and propose an algorithm to check whether ML systems violate these norms.


## Setup
First, download or clone the repository. The repository contains the next folders:
* DatasetsClean/: Contains the two datasets used in the paper already discretised (using quantile discretization). Each dataset contains its own configuration file in which protected, input and output columns are specified.
* config_template.py: A configuration template for new datasets
* NormativeApproach.py: The normative approach library
* Run.py: A running file, ready to execute
* README.md: this file.
* requirements.txt: Requirements file

Once we have downloaded the repository we need to install all dependencies and libraries:
```python
pip install requirements.txt
```

Ready to run the experiments (Python 3):
```python
python3 Run.py
```

## Running experiments
To run the experiments, we only need to create a `NormativeApproachDiscrimination` object by passing the csv and the datase config file (see below) as parameters.
```python
na = daddna.NormativeApproachDiscrimination('DatasetsClean/adult_quantile/adult_quantile.csv', 
                                             'DatasetsClean/adult_quantile/config_adult_quantile.py', 
                                             verbose= False)
violations = na.Run()
pprint.pprint(violations)
```

Note that all values in the csv `'DatasetsClean/adult_quantile/adult_quantile.csv'` will be considered discrete values, so the dataset should be discretised beforehand (we used quantile discretizations in our experiments). Also, a configuration file that defines the input, output, protected variables and exceptions is needed to run the analysis `'DatasetsClean/adult_quantile/config_adult_quantile.py'`. After calling `Run()`, the system will identify all violatoins of the norms as defined in the configuration file.

Explanations on how to create a configuration file for a dataset can be found in `config_template.py` file.


## Contact
You can find us on our website on [Discovering and Attesting Digital Discrimination](http://dadd-project.org/), take a look at our [Language Bias Visualiser](https://xfold.github.io/WE-GenderBiasVisualisationWeb/)!

Created by [@xfold](https://github.com/xfold).

