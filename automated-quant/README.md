# Pandas Automated Lipidomics Single Point Quantification

## Authors

* **Bryan Roberts**

## Description: 

Using Python and Pandas for data manipulation, calculates semi-quantitative single point quantification based on internal standard heights for CSH Lipidomics assay.  User enters Excel sheet containing untargeted Lipidomics raw data and internal standards CSV file containing internal standards information.  Program will return a results Excel file containing semi-quantified values in ng/mL or ng/mg based on sample extraction information.

## Calculation

* single point quant in ng/mL or ng/mg - ((native peak height / matching iSTD peak height) * ng iSTD extracted) / amount sample extracted (mL or mg)
* ng iSTD extracted = ng/mL in QC Mix * mL added during extraction

## Standards CSV File Format:

* Header Column A: iSTD Name
* Header Column B: ng iSTD extracted
* Starting from row 2, input iSTD being used for single point quant
* iSTD name must match exactly with iSTD name in excel file

## Excel File Format:

* Format generally follows raw ouput of MS-Dial with addition of iSTD Matching Number
* Row 1 column headers must be in the following order:
   * [Sample Meta Information Columns] ... [Sample Columns]
   * Within Sample Meta Information Columns, you must include the two following column headers:
   * iSTD Matching Number: must include "Number" in header string                
   * iSTD match number should match the iSTD with native annotations of the same compound class and matching adduct.  For example, if the number is 1 for 1_CE 22:1; iSTD  then all CE annotations must have 1.
   * Annotation Name: must include "Name" in header string
   * You can include as many other meta information header as needed in the Sample Meta Information Columns section.
   * Which header goes into which column does not matter, as long as all meta information columns are to the left of the sample columns.
   * Recommended to only include the single highest abundance adduct for each compound class.  Native adduct must match exactly with adduct used for iSTD.
   * Do not compare combined adducts with uncombined adducts.  For example, never compare the [M+H]+ species with a combined [M+H]+ [M+Na]+ species.  Peak heights are being compared and combining adducts skew the peak height ratios of the iSTD and native species.
* The sample names must be in the following format:
   * "SampleNameAndNum_MXNum_Mode_SampleId-Num"
   * Ex. "Biorec001_MX123456_posCSH_p1-001"
   * Sample ordering does not matter
* First compound must start in row 2

   
   ## Sources

* https://automatetheboringstuff.com/
* http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/
