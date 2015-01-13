# phpsysinfo2cacti
Retrieves a web server's memory usage and load average through phpsysinfo and formats the measurements in a way that they can be consumed by cacti

## Usage
``python phpsysinfo2cacti.py --mode retrieveJSONByHTTP --url "http://domain.tld/phpsysinfo/xml.php?json"``
