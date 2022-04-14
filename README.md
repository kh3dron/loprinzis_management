# loprinzis_management
automation for gym member checkin
run with:
  uvicorn sql_app.main:app --reload
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
## [0.5]
- remembered that HTML has a table element - no more bullet lists for objects
- CSS for table objects
- general big facelift
- fixed double checkin bug: no longer allowed 
- timeout bug patched - python and js time functions incompatible, now only use JS time for simplification
- added pricing chart to registration page
- member creation now has complete membership option:
  - select a date or a punch card, either will be stored in member data
## [0.6]
- autocomplete member names when typing into checkin page finally working
- checkout refresh issue solved (buttons work best from in forms)
- edit member form added to registration
  - member lookup is not dynamic, aaron is the only member you can look up right now
- needed more CRUD APIs:
  - set punches, name, address, expiration by ID 
## [0.7]
- lifetime historic visits on Queries page 
- CRUD to get visits by a datestring
- only show today's visits on daily Management
- update user fields implemented on register/edit page
- can now search for users to update (update page done)

### logging project
*Done*
- use structlog 
- format as json
- add timestamps
- add nested dictionaries for meta tags 

*Todo*
- abstract into seperate file callable with minimal lines
- pull uvicorn / fastapi logging into structlog logger - should be catching everything
- add to main:
  - level
  - logger name
  - line number

[todo] 
- member directory: 
  - check membership date OR auto-decrement punches upon checkin
- daily management
  - decrement punches when check in / check out
  - indicate error when checking in member without membership or punches
- more features
  - add visible error messages:
    - double checkin forbidden
  - queries page
    - queries: 
      - all members with 0 remaining punches / expired membership
      - others?


# Talk with Bob, Dec 13 
- members table should have phone #, comments field
- Needs to look simpler / easier to use
- Way to manually change checkin / checkout times on daily page
- Worried about teaching all staf to use the application. Needs to be simple. Need to use CSS to simplify & collapse pages, forms look too dense with text. 
- Punch cards: 
  - keep track of dates when they're used - maybe not automatic integration in check in manager

Possible reorganization for main menu: 

- Members
  - View all member details
  - Update a member's details
- Payments
  - Register a new member
  - extend a member's membership
- Front desk view: Check in 