from pathlib import Path
from string import Template
import ruamel_yaml as ryaml
SRC_PATH = Path('some-syllabi.yaml')
DESC_LENGTH = 200
DEST_PATH = Path('README.md')
DEST_START_STR = '<!--tablehere-->'

tbl = Template("""

There are currently <strong>${rowcount}</strong> courses listed; see [some-syllabi.yaml](some-syllabi.yaml) for more data fields.

<table>
    <thead>
        <tr>
            <th>Course</th>
            <th>Organization</th>
        </tr>
    </thead>
    <tbody>
       ${rows}
    </tbody>
</table>""")

row_template = Template("""
        <tr>
            <td>
                <h5>${course}</h5>
                <p>${links}</p>
                ${description}
            </td>
            <td>
                ${organization}
            </td>
        </tr>""")


tablerows = []
data = ryaml.load(SRC_PATH.open())
for d in data:
    course = '{0} | {1}'.format(d['title'], d['time_period']) if d.get('time_period') else d['title']


    if d.get('description'):
        desc = '<p><em>{0}</em></p>'.format(d['description'][:DESC_LENGTH] + '...' if len(d['description']) > DESC_LENGTH else d['description'])
    else:
        desc = ""


    if d.get('homepage') == d.get('syllabus'):
        links = """<a href="{0}">Homepage/Syllabus</a>""".format(d['homepage'])
    else:
        links = ' / '.join(["""\n<a href="{1}">{0}</a>""".format(n.capitalize(), d[n]) for n in ('homepage', 'syllabus') if d.get(n)])

    tablerows.append(row_template.substitute(course=course, description=desc, links=links, organization=(d['org'] if d.get('org') else '')))



tbltxt = tbl.substitute(rows=''.join(tablerows), rowcount=len(rows))


readmetxt = DEST_PATH.read_text().splitlines()

try:
    with DEST_PATH.open('w') as f:
        for line in readmetxt:
            if line != DEST_START_STR:
                print(line)
                f.write(line + "\n")
            else:
                print(DEST_START_STR)
                f.write(DEST_START_STR + '\n\n')
                print(tbltxt)
                f.write(tbltxt)
                break
# worst error-handling code ever:
except Exception as err:
    print("Aborting...Error:", err)
    lines = '\n'.join(readmetxt)
    print(lines)
    with DEST_PATH.open('w') as f:
        f.writelines(lines)
