#!/usr/bin/env python

from pathlib import Path
from string import Template
import re
import rtyaml as ryaml
from sys import stderr, stdout
BOIL_PATH = Path('BOILERPLATE.md')
SRC_PATH = Path('some-syllabi.yaml')

DEST_PATH = Path('README.md')
DESC_LENGTH = 300
# DEST_START_STR = '<!--tablehere-->'
SEASON_KEY = {'Spring': '03', 'Summer': '06', 'Fall': '09', 'Winter': '11'}

TABLE_TEMPLATE = Template("""

There are currently <strong>${rowcount}</strong> courses listed.

<table>
<thead>
    <tr>
        <th>Course</th>
    </tr>
</thead>
<tbody>
""")

ROW_TEMPLATE = Template("""
<tr>
<td>
<h5>${course} <br>
    <em>${organization}</em>
</h5>

<p>${links}</p>


<p>${description}</p>

${teachers}

</td>
</tr>""")


def sortfoo(record):
    timeval = str(record.get('time_period'))
    tx = re.match(r'^(\d{4}).*?(Spring|Summer|Fall|Winter)?\s*$', timeval)

    if tx:
        year, season = tx.groups()
        monthval = SEASON_KEY if season else "01"
        return f'{year}-{monthval}-{record["title"]}'
    else:
        return '0000-00-' + record['title']

def main():
    rawdata = ryaml.load(SRC_PATH.open())
    # Let's try sorting by time period
    data = sorted(rawdata, key=sortfoo, reverse=True)


    tablerows = []
    for d in data:
        course = '{0} » {1}'.format(d['title'], d['time_period']) if d.get('time_period') else d['title']
        if d.get('description'):
            desc = re.sub(r'\s+', ' ', d['description'])
            desc = desc[:DESC_LENGTH] + '...' if len(desc) >= DESC_LENGTH else desc
        else:
            desc = ""

        if d.get('instructors'):
            teachers = '<p>Instructors: {0}</p>'.format(', '.join(d['instructors']))
        else:
            teachers = ''

        if d.get('homepage') == d.get('syllabus'):
            links = """<a href="{0}">Homepage/Syllabus</a>""".format(d['homepage'])
        else:
            links = ' / '.join(["""\n<a href="{1}">{0}</a>""".format(n.capitalize(), d[n]) for n in ('homepage', 'syllabus') if d.get(n)])

        tablerows.append(ROW_TEMPLATE.substitute(course=course, description=desc,
                                                 links=links, teachers=teachers,
                                                 organization=(d['org'] if d.get('org') else '')))


    table_header = TABLE_TEMPLATE.substitute(rowcount=len(tablerows))
    boilerplate_text = BOIL_PATH.read_text()

    try:
        with DEST_PATH.open('w') as f:
            f.write(boilerplate_text)
            f.write(table_header)
            f.write("\n".join(tablerows))
            f.write("</tbody></table>")
            print(f"Success: {len(tablerows)} courses listed")

    # worst error-handling code ever:
    except Exception as err:
        stderr.write(f"Aborting...Error: {err}\n")
        # lines = '\n'.join(readmetxt)
        # # stderr(lines)
        # with DEST_PATH.open('w') as f:
        #     f.writelines(lines)


if __name__ == '__main__':
    main()
