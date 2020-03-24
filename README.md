# sentinel-1-pipeline

Processing pipeline for creation RTC Sentinel - 1 SAR imagery and ingestion into Google Earth Engine. 

### General steps:
* Download GRD scenes, define slave scenes (*slaves.csv*), set up database
* Populate metadata for images to be processed (*get_metadata.py*)
* Update databse with slave image metadata (*update-slave-images.py*), then process them (*process_slaves_gpt.py*)
* Process all other images then co register with matching slaves (*process_with_gpt.py*)
* Create manifest files (*writeManifest.py*) then sync outputs to CSB
* 
