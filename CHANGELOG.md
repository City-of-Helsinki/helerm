# Changelog

## [1.5.0](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.4.0...helerm-v1.5.0) (2025-11-12)


### Features

* Show uuid on Django admin ([bba2690](https://github.com/City-of-Helsinki/helerm/commit/bba26905f0d5bde1fea667828bfe4a408db94038))

## [1.4.0](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.3.3...helerm-v1.4.0) (2025-11-07)


### Features

* Allow dynamic sentry trace ignore paths ([9882452](https://github.com/City-of-Helsinki/helerm/commit/98824521774a95c4fe0b4adffa41860c7fa31ed0))
* Enable sentry logging for uWSGI ([911a23f](https://github.com/City-of-Helsinki/helerm/commit/911a23f2507b397fe1ab9ce9877fcea985265bed))


### Bug Fixes

* **dockerfile:** Resolve casing warning ([8ebf65d](https://github.com/City-of-Helsinki/helerm/commit/8ebf65de7cb5cdb2ec176409d9a9dd07b095103d))
* Remove InformatioSystem from JHS191 export ([3c4f9d7](https://github.com/City-of-Helsinki/helerm/commit/3c4f9d73fbb85331faa1f6917e882e43d772945b))


### Dependencies

* Bump django from 5.2.7 to 5.2.8 ([8cc9585](https://github.com/City-of-Helsinki/helerm/commit/8cc958563cfe54185d07f346521093d3fcc8f55c))
* Bump pip from 25.2 to 25.3 ([606a6ad](https://github.com/City-of-Helsinki/helerm/commit/606a6ad03d7cd5fe2ff9000eefda44b26f5e5118))

## [1.3.3](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.3.2...helerm-v1.3.3) (2025-10-27)


### Bug Fixes

* Update uwsgi-config for Sentry ([fff11f6](https://github.com/City-of-Helsinki/helerm/commit/fff11f6e28f90d4dc3dede8d2893f3a10f188cb7))

## [1.3.2](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.3.1...helerm-v1.3.2) (2025-10-13)


### Dependencies

* Bump social-auth-app-django from 5.5.1 to 5.6.0 ([9c919af](https://github.com/City-of-Helsinki/helerm/commit/9c919af098ba3149e2f13db5f6a525838a2dfb84))

## [1.3.1](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.3.0...helerm-v1.3.1) (2025-10-10)


### Bug Fixes

* Add missing cors headers for sentry ([57296ca](https://github.com/City-of-Helsinki/helerm/commit/57296ca19a04a89a20c9ff4c5f9466992877546e))

## [1.3.0](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.2.2...helerm-v1.3.0) (2025-10-09)


### Features

* **sentry:** Update sentry configuration ([714557e](https://github.com/City-of-Helsinki/helerm/commit/714557ef8d1f0ec6a736fe6e98a13da6b03d039c))


### Dependencies

* Bump django from 5.2.6 to 5.2.7 ([97d1e67](https://github.com/City-of-Helsinki/helerm/commit/97d1e6778284c1311e3ec6a050a87786438794ad))
* Bump sentry-sdk from 2.35.1 to 2.40.0 ([1827e11](https://github.com/City-of-Helsinki/helerm/commit/1827e11ec74e464a7d6514989914c29bb5fafce4))

## [1.2.2](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.2.1...helerm-v1.2.2) (2025-09-10)


### Dependencies

* Bump django from 5.2.5 to 5.2.6 ([1881fe4](https://github.com/City-of-Helsinki/helerm/commit/1881fe4fadeb86ee82f25110455d432386806f43))

## [1.2.1](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.2.0...helerm-v1.2.1) (2025-09-03)


### Dependencies

* Use psycopg with c dependency ([e6959fa](https://github.com/City-of-Helsinki/helerm/commit/e6959fa640f8d476e7b797ee3beaa5be0fd36b60))

## [1.2.0](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.1.4...helerm-v1.2.0) (2025-09-01)


### Features

* Use TunnistamoOIDCSerializer ([283227e](https://github.com/City-of-Helsinki/helerm/commit/283227ea196be000f38eabbf5c771debc1d988eb))


### Dependencies

* Generate hashes for requirements ([dd6087a](https://github.com/City-of-Helsinki/helerm/commit/dd6087a530812dab8939ea180f49462fc8371f6a))
* Remove drf-oidc-auth ([06272ae](https://github.com/City-of-Helsinki/helerm/commit/06272ae69b9a871acb2e4953874296378ea707e5))
* Remove pytz ([f86ab39](https://github.com/City-of-Helsinki/helerm/commit/f86ab39520ccc35381fbd50c66ca38f9ab043bb7))
* Replace psycopg2 with psycopg ([778c814](https://github.com/City-of-Helsinki/helerm/commit/778c814d0127c37f5bab1ffb933dbbd53b03de04))
* Upgrade dependencies ([ecc8627](https://github.com/City-of-Helsinki/helerm/commit/ecc8627b9208b98b4d898ce21abb93b8d456f7a1))
* Upgrade dev dependencies ([5d864d4](https://github.com/City-of-Helsinki/helerm/commit/5d864d426c9fa8c419df594821722af4bc2f52b7))
* Upgrade pip-tools to 7.5.0 ([fbd9faa](https://github.com/City-of-Helsinki/helerm/commit/fbd9faa15dcc77cbc3a3ea3a731d9b72831ce5c1))
* Upgrade to django 5.2 ([c9ccab0](https://github.com/City-of-Helsinki/helerm/commit/c9ccab02d6f1dfa6cc309e7565e77a6f5ef63aaf))
* Upgrade to python 3.12 ([52b6958](https://github.com/City-of-Helsinki/helerm/commit/52b6958bd5eff35207a371681f31497ab92fd95d))

## [1.1.4](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.1.3...helerm-v1.1.4) (2025-08-12)


### Dependencies

* Bump urllib3 from 2.2.2 to 2.5.0 ([71f8959](https://github.com/City-of-Helsinki/helerm/commit/71f89597049b4a5c3bd93bdd19e076b47de57cac))
* Replace black, flake8, isort with ruff ([b9b317f](https://github.com/City-of-Helsinki/helerm/commit/b9b317fc7cead46518a515688d2749c0d28952bd))


### Documentation

* Ruff and pre-commit ([22b32f6](https://github.com/City-of-Helsinki/helerm/commit/22b32f6655d6aa34834cd473ee5f855375f63292))

## [1.1.3](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.1.2...helerm-v1.1.3) (2025-06-13)


### Dependencies

* Bump django from 4.2.22 to 4.2.23 ([c89fcf2](https://github.com/City-of-Helsinki/helerm/commit/c89fcf23f450e42741e57187bca3ec647e9a60ec))
* Bump requests from 2.32.3 to 2.32.4 ([4dbdadb](https://github.com/City-of-Helsinki/helerm/commit/4dbdadbebbe41837ea9cf575f48e6cade3396a61))

## [1.1.2](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.1.1...helerm-v1.1.2) (2025-06-10)


### Dependencies

* Bump django from 4.2.21 to 4.2.22 ([6aa3ddc](https://github.com/City-of-Helsinki/helerm/commit/6aa3ddc5f80bdfc3eab3158f194ab6b20cc05c83))

## [1.1.1](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.1.0...helerm-v1.1.1) (2025-05-14)


### Dependencies

* Bump django from 4.2.18 to 4.2.21 ([fff2ff8](https://github.com/City-of-Helsinki/helerm/commit/fff2ff8313944f6a35d67dc470a60829d8981c0d))

## [1.1.0](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.0.3...helerm-v1.1.0) (2025-03-07)


### Features

* Hide all information_system attributes from es search ([#415](https://github.com/City-of-Helsinki/helerm/issues/415)) ([5035c8f](https://github.com/City-of-Helsinki/helerm/commit/5035c8f2a51c7102eecb99896859c0b8f8dfd29a))
* Hide information_system from unauthenticated users ([#413](https://github.com/City-of-Helsinki/helerm/issues/413)) ([5b24268](https://github.com/City-of-Helsinki/helerm/commit/5b242687d570f82b14ac111db5b77e69de173de1))
* Restrict filtering for information system for unauth users ([#414](https://github.com/City-of-Helsinki/helerm/issues/414)) ([2e38472](https://github.com/City-of-Helsinki/helerm/commit/2e384720b853559acca8b7204ee3bbe6fb36db5e))
* Restrict information_system from facets for unauthenticated ([#416](https://github.com/City-of-Helsinki/helerm/issues/416)) ([70b0448](https://github.com/City-of-Helsinki/helerm/commit/70b0448fca1cd642255f515cacc65bf75aaf4a38))


### Dependencies

* Bump cryptography from 43.0.1 to 44.0.1 ([#419](https://github.com/City-of-Helsinki/helerm/issues/419)) ([145463d](https://github.com/City-of-Helsinki/helerm/commit/145463d5fae5032347f77f97dc198f8eb419f45f))
* Bump django from 4.2.16 to 4.2.17 ([7ba5dd7](https://github.com/City-of-Helsinki/helerm/commit/7ba5dd74d47981d200518fed404a2e449211e8f3))
* Bump django from 4.2.17 to 4.2.18 ([0d9d673](https://github.com/City-of-Helsinki/helerm/commit/0d9d67308a17cdd2b84713fbb4b8f309e176e057))
* Bump python-jose from 3.3.0 to 3.4.0 ([0ddcb3d](https://github.com/City-of-Helsinki/helerm/commit/0ddcb3dec91dd314c0e959d8aa391576d33e107a))
* Bump virtualenv from 20.26.2 to 20.26.6 ([a91d884](https://github.com/City-of-Helsinki/helerm/commit/a91d8841763e99f2d94da46ecb6bb84a55446797))

## [1.0.3](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.0.2...helerm-v1.0.3) (2024-11-08)


### Dependencies

* Bump cryptography from 42.0.8 to 43.0.1 ([#407](https://github.com/City-of-Helsinki/helerm/issues/407)) ([a79d37a](https://github.com/City-of-Helsinki/helerm/commit/a79d37ac2044ade0e19686c9ed589ac86b70be9b))
* Bump django from 4.2.15 to 4.2.16 ([d5679e8](https://github.com/City-of-Helsinki/helerm/commit/d5679e8aa99109210f822efda13e752372991757))
* Bump django-cors-headers from 4.3.1 to 4.4.0 ([7149807](https://github.com/City-of-Helsinki/helerm/commit/714980729ade7d672ad59facdeb84be5cd52dc19))
* Bump django-filter from 24.2 to 24.3 ([74567fe](https://github.com/City-of-Helsinki/helerm/commit/74567feca1304a42151ce612fa2377af66318043))
* Bump flake8-bugbear from 24.4.26 to 24.8.19 ([1458e76](https://github.com/City-of-Helsinki/helerm/commit/1458e769bf2d149453b22f0a4d71d60479fe46ce))
* Bump pytest from 8.2.2 to 8.3.2 ([761cb48](https://github.com/City-of-Helsinki/helerm/commit/761cb4894e0cbfc1a5ea93b5487cffb9b0515dd2))
* Bump sentry-sdk from 2.4.0 to 2.13.0 ([3328bbd](https://github.com/City-of-Helsinki/helerm/commit/3328bbdd1e375aa091d239689ef715bf67b96035))

## [1.0.2](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.0.1...helerm-v1.0.2) (2024-08-08)


### Dependencies

* Bump certifi from 2024.6.2 to 2024.7.4 ([d0302c1](https://github.com/City-of-Helsinki/helerm/commit/d0302c1565988d2e59f4542ffba9d23fea5b894b))
* Bump django from 4.2.13 to 4.2.15 ([aefbbdb](https://github.com/City-of-Helsinki/helerm/commit/aefbbdb193b2b125348e88022376eff1ed7faa35))
* Bump djangorestframework from 3.15.1 to 3.15.2 ([4d83cf1](https://github.com/City-of-Helsinki/helerm/commit/4d83cf10870aa2a00b3d91269ccad78cdb1f7149))
* Bump urllib3 from 2.2.1 to 2.2.2 ([fee9ea6](https://github.com/City-of-Helsinki/helerm/commit/fee9ea6d14217cf422513956acb25b3e33a544eb))

## [1.0.1](https://github.com/City-of-Helsinki/helerm/compare/helerm-v1.0.0...helerm-v1.0.1) (2024-08-07)


### Bug Fixes

* Increase uWSGI harakiri timeout ([9ae8a16](https://github.com/City-of-Helsinki/helerm/commit/9ae8a167bac412a2b451a752eafca797d8908ee1))

## [1.0.0](https://github.com/City-of-Helsinki/helerm/compare/v0.4.13...helerm-v1.0.0) (2024-06-06)

First release to run on Platta.
