# Complicated Badge Creator
The CBC creates badges (for e.g. conferences) by replacing names in a ```*.svg``
template using names from a ``*.csv`` file.

## Data Preparation
- Create a (graphical) template similar to ``template.svg``
- Create an attendee list similar to ``attendees.csv``
  - Name your column headers (1st row) w.r.t the template fields
  - Field names must start with # (e.g. ``#name``; ``#company``)
- NOTE: all files _must_ be ``UTF-8`` encoded
  - check them using i.e. notepad++ (e.g. Illustrator & Excel do not produce UTF-8
    encoded files)

## Running the CBC
- Install ``Python 3``
- Open a command line and cd to this folder, then:
```
python src/cbc.py ./data/template.svg ./data/attendees.csv ./print
```

## Printing on Both Sides
- Choose ``--back`` with the number of columns
- When printing, choose ``Flip on Short Edge``

## Create PDFs
Adding the option `--pdf` outputs the badges as pdf. You need to add the svglib package:
````bash
pip install svglib 
````
NOTE: some fonts are not supported when converting to pdf.

## Using ACM's RegOnline
- Export attendee list from ``RegOnline`` as ``xls``
  - Analyze -> Reports -> Registrant List
- Adjust columns
  - Name, Company, Role (Attendee)
- Save as ``Unicode Text (*.txt)``
- In notepad++
  - Replace: ``\t`` with ``;``
  - Replace: ``;;`` with ``;`` until there are only single semi-colons
