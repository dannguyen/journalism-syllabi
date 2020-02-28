#!/usr/bin/env python

from pathlib import Path
from string import Template
import rtyaml as ryaml
from sys import stderr, stdout
SRC_PATH = Path('some-syllabi.yaml')
DEST_PATH = Path('README.md')
DESC_LENGTH = 300
DEST_START_STR = '<!--tablehere-->'
TABLE_TEMPLATE = Template("""
There are currently <strong>${rowcount}</strong> courses listed; see [some-syllabi.yaml](some-syllabi.yaml) for more data fields.

<table>
    <thead>
        <tr>
            <th>Course</th>
            <th>Organization</th>
        </tr>
    </thead>
    <tbody>${rows}</tbody>
</table>""")

ROW_TEMPLATE = Template("""
    <tr>
        <td>
            <h5>${course} <br>
                ${links}
            </h5>
            ${description}
            ${teachers}
        </td>
        <td>
            ${organization}
        </td>
    </tr>""")

def main():
    entries = []
    data = ryaml.load(SRC_PATH.open())
    for d in data:
        course = '{0} | {1}'.format(d['title'], d['time_period']) if d.get('time_period') else d['title']
        if d.get('description'):
            desc = '<p><em>{0}</em></p>'.format(d['description'][:DESC_LENGTH] + '...' if len(d['description']) > DESC_LENGTH else d['description'])
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

        entries.append(d)

    # Let's try sorting by time period
    tablerows = []
    for d in sorted(entries, key=lambda r: str(r.get('time_period')), reverse=True):

        try:
            rowtxt = ROW_TEMPLATE.substitute(course=course, description=desc,
                                                     links=links, teachers=teachers,
                                                     organization=(d['org'] if d.get('org') else ''))
            tablerows.append(rowtxt)

        except Exception as err:
            stderr.write(f"Aborting due to: {err}\n\n")
            stderr.write(f"Entry that caused error:\n")
            stderr.write(d)

    tbltxt = TABLE_TEMPLATE.substitute(rows=''.join(tablerows), rowcount=len(tablerows))
    tbltxt = tbltxt.replace('\n', ' ')
    boilerplate_text = DEST_PATH.read_text().splitlines()

    try:
        with DEST_PATH.open('w') as f:
            for line in boilerplate_text:
                if line != DEST_START_STR:
                    # print(line)
                    f.write(line + "\n")
                else:
#                    print(DEST_START_STR)
                    f.write(DEST_START_STR + '\n\n')
#                    print(tbltxt)
                    # write all of the course list in one chunk
                    f.write(tbltxt)
                    print(f"Success: {len(tablerows)} courses listed")
                    break
    # worst error-handling code ever:
    except Exception as err:
        stderr.write(f"Aborting...Error: {err}\n")
        # lines = '\n'.join(readmetxt)
        # # stderr(lines)
        # with DEST_PATH.open('w') as f:
        #     f.writelines(lines)


if __name__ == '__main__':
    main()
