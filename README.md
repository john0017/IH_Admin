# Property Portfolio Data-Quality Review

A Flask and Selenium automation prototype for reviewing property records in a browser-based portfolio system and identifying missing information.

## Overview

The project automates navigation through property records, maps table entries to their detail pages, checks configured form fields, and produces a browser report showing which values are missing for each property.

## Workflow

```text
Portfolio property list
          |
          v
Map addresses to record identifiers
          |
          v
Open each property detail page
          |
          v
Check configured form fields
          |
          v
Report missing values by property
```

## Features

- Runs Chrome in headless mode through Selenium
- Searches and iterates through portfolio property records
- Maps displayed addresses to internal record identifiers
- Uses a JSON field map to drive validation
- Detects blank, unset, zero, or unselected values
- Groups missing fields by property address
- Displays results through a Flask and Bootstrap interface

## Technology

- Python
- Flask
- Selenium WebDriver
- Flask-Bootstrap
- JSON
- HTML templates
- ChromeDriver

## Main Components

- `app.py` — browser automation, validation logic, and Flask route
- `id_map.json` — mapping between business fields and page element identifiers
- `templates/` — results interface
- `chromedriver` — browser-driver binary used by the prototype

## Project Status

This is a historical internal-tool prototype. Page selectors, browser-driver compatibility, and target-system URLs may have changed and should be reviewed before running it.

## Security Notice

Do not deploy this repository as-is. Authentication details, application configuration, and internal URLs should be removed from source code, rotated where necessary, and supplied through environment variables or an approved secrets manager. Only run browser automation against systems you are authorized to access.
