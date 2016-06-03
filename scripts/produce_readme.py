from pathlib import Path
import ruamel_yaml as ryaml
SRC_PATH = Path('some-syllabi.yaml')
DESC_LENGTH = 150
DEST_PATH = Path('README.md')
DEST_START_STR = '<!--tablehere-->'

tbl = """
<table>
    <thead>
        <tr>
            <th>Course</th>
            <th>Links</th>
            <th>Organization</th>
        </tr>
    </thead>
    <tbody>
       {rows}
    </tbody>
</table>"""

row_template = """
        <tr>
            <td>
                {course}
            </td>
            <td>
                {links}
            </td>
            <td>
                {organization}
            </td>
        </tr>"""


tablerows = []
data = ryaml.load(SRC_PATH.open())
for d in data:
    course = '<h4>{0}</h4>'.format(d['title'])
    if d.get('time_period'):
        course += '\n  {0}'.format(d['time_period'])
    if d.get('description'):
        desc = d['description'][:DESC_LENGTH] + '...' if len(d['description']) > DESC_LENGTH else d['description']
        course += '\n  <p><em>{0}</em></p>'.format(desc)

    if d.get('homepage') == d.get('syllabus'):
        links = """<a href="{0}">Homepage/Syllabus</a>""".format(d['homepage'])
    else:
        links = '/'.join(["""<a href="{1}">{0}</a>""".format(n.capitalize(), d[n]) for n in ('homepage', 'syllabus') if d.get(n)])

    tablerows.append(row_template.format(course=course, links=links, organization=d.get('org')))

tbltxt = tbl.format(rows=''.join(tablerows))


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
