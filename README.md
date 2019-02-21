# Introduction
PasteHunter2 is a general parser for websites like Pastebin. I tried to make it easy to implement new code for parsing different paste websites. For now, PasteHunter2 will generate reports every hours and send them to an email address. Furthermore, urgent paste will trigger an alert with a text messange on your phone.

# Deps
- Python 3
- clockwork [https://pypi.org/project/Clockwork/](clockwork)
- argparse
- configparser
- loggin

# Usage
The script reads a config file `config.ini`. Copy `config.sample.ini` to `config.ini` after editing the file. The fields are not checked for (yet!) so be careful when updating the config file. 

```
$ ./pastehunter2.py --help
02/21/2019 09:52:06 AM - INFO: Reading config.ini, fields are not checked!
usage: pastehunter2.py [-h] [-p PHONE] [-e EMAIL] [-r DELAYREPORT]
                       [--loadcsv CSV] [--add] [--type FTYPE] [--regex REGEX]
                       [--urgent URGENT] [--desc DESC]
                       filters

positional arguments:
  filters               json file with filters

optional arguments:
  -h, --help            show this help message and exit
  -p PHONE, --phone PHONE
                        Phone number to report urgent paste.
  -e EMAIL, --email EMAIL
                        Email address to report to.
  -r DELAYREPORT, --report DELAYREPORT
                        Delay between reports (in seconds)
  --loadcsv CSV         Update filter from CSV file. Exit when done.
  --add                 Add a filter to the list of filters. Exit when done.
  --type FTYPE          Type of filter (card, keyword, email, ...). Required
                        if --add is provided.
  --regex REGEX         Regex of filter. Required if --add is provided.
  --urgent URGENT       1 or 0. Required if --add is provided.
  --desc DESC           Very small description. Required if --add is provided.
```
# First
Before starting PasteHunter2 you need to generate the `json` file with all the filters.

## Format
A filter should include a filter type `ANYKEYWORD` with a small description `desc`, the corresponding `regex` and a `urgent` flag (0 or 1). When a filter with the urgent tag is detected in a paste, it triggers a text message.
```
{
    "ANYKEYWORD": [
        {
            "desc": ,
            "regex": ,
            "urgent": 
        },
        {
            "desc": ,
            "regex": ,
            "urgent": 
        }
    ]
}
```

## From CSV
Pasteunter2 is able to load a CSV file and format `filters.json` correctly.

Start PasteHunter2 with `--loadcsv CSVFILE` and the name of the json ouput file.
```
$ ./pastehunter2.py --loadcsv filters.sample.csv filters.json
```

Take a look at `filters.sample.csv`.

## From PasteHunter2
You can add filters to the file by calling PasteHunter2 with those parameters.

```
$ ./pastehunter2.py --add --type keywords --regex "test" --urgent 0 --desc "test filter" ./filters.json
```
# Licence
MIT

# Issues
Open a ticket :)