# Complicated Badge Creator
The CBC creates badges (for e.g. conferences) by replacing names in a ```*.svg``
template using names from a ``*.csv`` file.

## Data Preparation
- Create a (graphical) template similar to ``template.svg``
- Create a attendee list similar to ``attendees.csv``
  - Name your column headers (1st row) w.r.t the template fields
  - Field names must start with # (e.g. ``#name``; ``#company``)
- NOTE: all files _must_ be ``UTF-8`` encoded
  - check them using notepad++ (e.g. Illustrator & Excel do not produce UTF-8
    encoded files)

## Running the
- Install ``Python 3.4``
- Open a command line and cd to the ``src``
- Call the CBC
```
cbc.py ..\data\template.svg ..\data\attendees.csv ..\badges --back 3
```

## Printing on Both Sides
- Choose ``--back`` with the number of columns
- When printing, choose ``Flip on Short Edge``

## Using ACM's RegOnline
- Export attendee list from ``RegOnline`` as ``xls``
  - Analyze -> Reports -> Registrant List
- Adjust columns
  - Name, Company, Role (Attendee)
- Save as ``Unicode Text (*.txt)``
- In notepad++
  - Replace: ``\t`` with ``;``
  - Replace: ``;;`` with ``;`` until there are only single semi-colons
