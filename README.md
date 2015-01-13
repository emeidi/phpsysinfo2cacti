# phpsysinfo2cacti
Retrieves a web server's memory usage and load average through phpsysinfo and formats the measurements in a way that they can be consumed by cacti

## Usage
### HTTP
``python phpsysinfo2cacti.py --mode retrieveJSONByHTTP --url "http://domain.tld/phpsysinfo/xml.php?json"``
``Used:8048672768 Free:203681792 One:2.61 Five:2.38 Fifteen:2.41``

### Local JSON dump
(Mainly for testing purposes)

``python phpsysinfo2cacti.py --mode retrieveJSONFromFile --file phpsysinfo.json``
``Used:8048672768 Free:203681792 One:2.61 Five:2.38 Fifteen:2.41``
