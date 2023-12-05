The project is created in IntelliJ, folders /.idea /__pycache__ and /venv are created by IntelliJ

1.FarSideAR.py is a data model class, it contains one far side active region attributes

2.DownloadARListToCSVFile.py downloads all far side region data from 'http://jsoc.stanford.edu/data/farside/AR_Lists/' to
  far_side_active_region_JSOC.csv file

3. You may skip running DownloadARListToCSVFile.py to generate far_side_active_region_JSOC.csv. YOu may run ProcessImageFiles.py
  with existing Data/far_side_active_region_JSOC.csv. ProcessImageFiles.py generates far_side_ar_nnnnn.csv file for every year data,
  then combine all far_side_ar_nnnnn.csv files into far_side_ar_all.csv file. 




