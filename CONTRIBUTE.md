# How to contribute

If you have a suggestion for a course to add, it's as easy as [creating an issue](https://github.com/dannguyen/journalism-syllabi/issues) and pasting a URL that I can visit myself and gather the course info from.

> Note: The purpose of this site is to provide guidance and inspiration to other data journalism instructors, so *generally*, suggested courses should have a publicly-viewable syllabus. 


## Filling out course info yourself

If you feel the need to be more helpful, or want to write the course info yourself, it's as easy as filling out the fields in this YAML template:

```yaml
- title: _____
  course_listing: _____
  org: _____
  time_period: "_____" 
  homepage: _____
  syllabus: _____

  description: |
    _____

  instructors:
      - _____



title: "Human Readable Name of the Course"
course_listing: "DEPT 123" # if applicable; not all courses listed are from college
org: "The full name of the University"
time_period: "20XX" # year is fine, if there's a session, delimit it with a semicolon, e.g. Fall; 2019
homepage: https://the-landing-page-of-the
syllabus: https://if-the-homepage-is-not-the-syllabus/provide/direct/link/to/syllabus

description: |
    Descriptive blurb about the course. I usually just copy-paste from the catalog if possible. Gets auto-truncated to 300 characters.

instructors:
    - FirstName LastName
    - Mabe Theres-Multiple Teachers
```

Here's an example:

```yaml
title: Data Journalism
course_listing: JOUR 407
org: University of Nebraska-Lincoln
time_period: 2014
homepage: https://github.com/mattwaite/JOUR407-Data-Journalism/tree/601b51dafb0690ff9679861258683d943449312e
syllabus: https://github.com/mattwaite/JOUR407-Data-Journalism/blob/601b51dafb0690ff9679861258683d943449312e/syllabus.md
description: |
The best reporters harness the right tools to get the story. In this class, we’ll use brainpower and software to look at raw data -- not summarized and already reported information -- to do investigative reporting. We’re going to get our hands dirty with spreadsheets, databases, maps, some basic stats and, time permitting, some stuff I’ll call “serious future s**t.” And in the end, we’ve got a project to produce. So buckle up and hold on.
instructors:
    - Matt Waite
```

Again, you can create an issue and just paste the YAML you've written, and I'll add it to [some-syllabi.yaml](some-syllabi.yaml)


## Doing a pull request

If you feel the need to do the full open-source thing, I won't stop you from cloning the repo and submitting a pull request.

To have your course entry show up on the main [course listing](README.md#the-course-list), make a new YAML entry as previously above and add it to the bottom of [some-syllabi.yaml](some-syllabi.yaml). 

How do the YAML entries get added to the [course listing](README.md#the-course-list)? Via the crude Python script in: [scripts/produce_courselist.py](scripts/produce_courselist.py)

To run that script, you can use the following `make` command:

```sh
$ make
```

If all goes well, the [README.md](README.md) file will be updated (or rather, rewritten via my sloppy Python script), and you can push the changes to [README.md](README.md) and [some-syllabi.yaml](some-syllabi.yaml) to Github for me to merge. 
