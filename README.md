# HealthKit Data Processor

This script is designed to parse HealthKit data exported from an iOS device and calculate weekly totals with percent change from the previous week.

  

## Getting Started

### Prerequisites

- Python 3.x
- Tabulate 0.9.0


### Installation

 - Clone the repository: `git clone https://github.com/groenern/NASA-APOD-MySQL-Connector-Project.git`
 - Install tabulate `pip install -r requirements.txt`

  
### Usage

 1. Export your HealthKit data from your iOS device as an XML file (instructions can be found [here](https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios) - Share your health and fitness data in XML format)
 2. Place the export.xml file in the same directory as mileageTotals.py (or use absolute paths)
 3. Run the script `mileageTotals.py export.xml `


## Sample Output
![SampleOutput](https://user-images.githubusercontent.com/130081417/230970685-744d85da-e402-4409-ba1e-504089e89a7a.png)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
