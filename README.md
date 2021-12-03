# loprinzis_management
automation for gym member checkin

# CHANGELOG

## [0.0]
- added changelog
- copied sample database program
- added dump db page (items)
## [0.1]
- reshape users db to have proper columns
  - refactor all references to users -> members
- dumb shitty way of printing db entries on sample page
- API for member creation - now working with buttons
## [0.2]
- jinja templates for cleaner HTML documenting
- jinja templates for better printing of db results
- split functionality into seperate pages
- refactor members database to have just "name" instead of first and last
  - bug hunt: need to include POST function from script tags in jinja imported tempates, left it behind at first and forms died
- create new database: historic visits
  - new models.py with relationships between DBs
  - new schemas, new cruds
- page for daily management
- API to create visits - takes usernames, looks up member ID

### Pending 
## [0.4]
- button working for visit creation



### TODO
- check in / check out page
  - check in a user
  - display table of users currently in
  - button to check out a user that updated db
  - export today as CSV
- view all members page
  - pretty display all members
- analytics page
  - select day of entries
  - load from CSV
  - sample queries
