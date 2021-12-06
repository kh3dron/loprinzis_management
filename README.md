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
## [0.3]
- Daily Management page:
  - visit creation button fails if user doesn't exist
  - pretty printing for current checkins
  - history section to show checkins who have checked out
## [0.4]
- more prettyprinting features for UI
- pass in query objects instead of strings to daily page
- added /visit and /vitis/{visit_id} helper endpoints
- CRUD method to upsate visits with checkout 
- checkin / checkout buttons work


[todo] remove none printing on history list
[todo] add on-page error for attempting to check in nonexistent user