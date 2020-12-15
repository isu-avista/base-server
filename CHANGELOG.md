# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Removed

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