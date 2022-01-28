# Pandas Automated Lipidomics Single Point Quantification

Using Python and Pandas for data manipulation, calculates semi-quantitative single point quantification based on internal standard heights for CSH Lipidomics assay. User enters Excel sheet containing untargeted Lipidomics raw data and internal standards CSV file containing internal standards information. Program will return a results Excel file containing semi-quantified values in ng/mL or ng/mg based on sample extraction information.

# Metabolomics-Automate-Data-Reduction

Automate data reduction for Metabolomics untargeted LC-MS data and put reduced dataset through online MS-FLO software. Produces
tables to check data quality. Currates MS-Flo output to be used with single-point iSTD quant scripts after data curation.

# MS-Dial-Batch-Alignment

Takes different batches of excel sheets in the same folder as script from the same LC-MS run and combines
features into a new excel sheet called "results.xlsx". Features are aligned based on annotation name.

# Bootcamp Internal Standard Finder

Searches all .xlsx files in same directory as program and searches for matches to Fiehn lab internal standards.
Matches are based on accurate mass and retention time similarity to library references. User can choose between
Fiehn lab HILIC and CSH internal standards. Program will create new file called 'results.xlsx' compiling information
for all .xlsx files in the same directory as well as a count for how many internal standards have been found.

# Agilent Date Time Extractor

Extract date times from agilent file directory for sample ordering based on time of acquisition
