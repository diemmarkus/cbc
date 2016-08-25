# Complicated Badge Creator
The CBC creates badges (for e.g. conferences) by replacing names in a ```*.svg``
template using names from a ``*.csv`` file.

## Data Preparation
- Create a (graphical) template similar to ``template.svg``
- Create a attendee list similar to ``attendees.csv``
  - Name your column headers (1st row) w.r.t the template fields
  - Field names must start with # (e.g. ``#name``; ``#company``)

## Using ACM's RegOnline
- Export attendee list from ``RegOnline`` as ``xls``
  - Analyze -> Reports -> Registrant List
- Adjust columns
  - Name, Company, Role (Attendee)
- Save as ``Unicode Text (*.txt)``
- In notepad++
  - Replace: ``\t`` with ``;``
  - Replace: ``;;`` with ``;`` until there are only single semi-colons
