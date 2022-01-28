# MS-Dial-Batch-Alignment

Takes different batches of excel sheets in the same folder as script from the same LC-MS run and combines 
features into a new excel sheet called "results.xlsx".  Features are aligned based on annotation name.  

# Steps for getting matching annotation names:

* process initial batch with ~200 samples and all MSMS samples
* reduce this data export and make mzrt from remaining ~3000 features
* mzrt name will be in the format name_adduct_mz_rt
* process remaining data in batches using new mzrt and correcting retention times for each batch
* use python script to align data in "results.xlsx"

## Getting Started

Put script in folder with all excel files to align and run script.

### Prerequisites

Excel files in MS-Dial 3.90 export format or later.

## Authors

* **Bryan Roberts**

## Sources

* https://automatetheboringstuff.com/
* http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/
