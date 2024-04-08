The project is created in IntelliJ, folders /.idea /__pycache__ and /venv are created by IntelliJ

Data sets:
1. Data/matched_fs_ns_ar.csv is the result file that contains both far side active region and near side active region information

2. Data/far_side_active_region_JSOC.csv is the basic far side active region information file.
It is generated by DownloadARListToCSVFile.py that downloads from http://jsoc.stanford.edu/data/farside/AR_Lists

3. Data/far_side_ar_all.csv is generated by ProcessImageFiles.py. It takes Data/far_side_active_region_JSOC.csv file, then adds min/max
X/Y data after processing image files

4. Data/MU_noaa_ars_plages.csv is near-side active region data. It was provided by Dr. Aydin

Python Files:
1. To match far-side active region data with near side active region data, all you have to run is Match_Farside_Nearside_AR.py.
It takes far-side active region file Data/far_side_ar_all.csv and matches it with near-side active region file Data/MU_noaa_ars_plages.csv
All other python files are data preparation files.

2.FarSideAR.py is a data model class, it contains one far side active region attributes.

3.DownloadARListToCSVFile.py downloads all far side region data from 'http://jsoc.stanford.edu/data/farside/AR_Lists/' to
  far_side_active_region_JSOC.csv file

4. You may skip running DownloadARListToCSVFile.py to generate far_side_active_region_JSOC.csv. You may run ProcessImageFiles.py
  that takes existing Data/far_side_active_region_JSOC.csv file to find far-side active region min/max longtitude/latitude boundary.
 It generates far_side_ar_nnnnn.csv file for every year data, then combine all far_side_ar_nnnnn.csv files into far_side_ar_all.csv file.
