# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Removed

## [v0.3.6](https://github.com/isu-avista/base-server/releases/tag/v0.3.6) - 2021-02-17
### Added

### Changed
* Modified service create app to allow CORS across all domains and for all routes

### Removed

## [v0.3.5](https://github.com/isu-avista/base-server/releases/tag/v0.3.5) - 2021-02-16
### Added

### Changed
* removed python 3.6 from travis ci build

### Removed

## [v0.3.4](https://github.com/isu-avista/base-server/releases/tag/v0.3.4) - 2021-02-16
### Added

### Changed
* Updated the test-data configurations
* travis ci specification so that it correctly tests and builds the system
* updated the requirement.txt to include additional libraries and to fix the import of avista_data
* updated the tests so that they all pass

### Removed
* Removed the "test.db" from the avista_base module

## [v0.3.3](https://github.com/isu-avista/base-server/releases/tag/v0.3.3) - 2021-02-15
### Added

### Changed
* Fixed minor mistake in service.py

### Removed

## [v0.3.2](https://github.com/isu-avista/base-server/releases/tag/v0.3.2) - 2021-02-15
### Added

### Changed
* Fixed minor bug in the database setting generation code

### Removed

## [v0.3.1](https://github.com/isu-avista/base-server/releases/tag/v0.3.1) - 2021-02-14
### Added

### Changed
* Added code to extract the correct database settings from the configuration files

### Removed

## [v0.3.0](https://github.com/isu-avista/base-server/releases/tag/v0.3.0) - 2021-02-11
### Added
* AvistaApp which sets up the use of Gunicorn for production

### Changed
* Reverted service back to it prior implementation while also removing any server (Flask or Gunicorn) operational details
* Moved the basic flask operation, for testing, into the MockService under the test director
* Updated documentation

## [v0.2.0](https://github.com/isu-avista/base-server/releases/tag/v0.2.0) - 2021-02-06
### Added
* Service now inherits from `gunicorn.app.BaseApplication`

### Changed
* `Service.start()` no longer creates a new `Process()` for the flask application,
  Service.start() instead calls `gunicorn.app.BaseApplication.run()`
* `Service.init()` is now called `Service.initialize()` as to not override `BaseApplication.init()`
* `Service.start()` no longer calls `Service.initialize()` because inheriting classes may need
  to do work in between `initialize()` and `start()`

## [v0.1.6](https://github.com/isu-avista/base-server/releases/tag/v0.1.6) - 2020-12-15
### Added

### Changed
* Minor change to fix get_log()

### Removed

## [v0.1.5](https://github.com/isu-avista/base-server/releases/tag/v0.1.5) - 2020-12-15
### Added
* New BaseTest base for both api and service tests

### Changed
* removed redundant calls to the service.init() method
* refactored call to db.create_all()

### Removed

## [v0.1.4](https://github.com/isu-avista/base-server/releases/tag/v0.1.4) - 2020-12-15
### Added
* Service api component and tests

### Changed

### Removed

## [v0.1.3](https://github.com/isu-avista/base-server/releases/tag/v0.1.3) - 2020-12-15
### Added

* API components for both authentication (i.e. login)
* API components for adding/removing users
* API components for manipulating the service configuration (but not the flask config)
* Tests for each of the API components

### Changed

* Updated the Service class to finally be ready to serve as the base for the portal and the IoT
* Updated tests for the service

### Deleted

## [v0.1.2](https://github.com/isu-avista/base-server/releases/tag/v0.1.2) - 2020-12-13
### Added

### Changed
- Added app_context to service
- Updated service to use data_manager from data module
- Updated tests

### Deleted

## [v0.1.1](https://github.com/isu-avista/base-server/releases/tag/v0.1.1) - 2020-12-06
### Added

### Changed
- Added sphinx documentation for the entire system
- Updated code documentation for entire system
- Improved tests to reach 100% coverage

### Deleted

## [v0.1.0](https://github.com/isu-avista/base-server/releases/tag/v0.1.0) - 2020-11-16
### Added
- Added initial project structure
- Updated this file
- Implemented basic classes
- Implemented initial tests

### Changed
- None

### Removed
- None
