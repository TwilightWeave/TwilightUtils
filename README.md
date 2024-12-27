# Twilight utilities

Utilities most of the python developers copy into each new project. Why do you want to do it ever damn time? Let's
keep them in a single place as a collection of useful tools and utilities which we can share with each other! Less
boilerplate, more fun!

Repository: https://github.com/TwilightWeave/TwilightUtils
Documentation: https://twilightweave.github.io/TwilightUtils/twilight_utils.html

## Warning

This project is in progres, and it's not ready for production use. I decided to publish it to PyPi earlier to improve
dependency management in my other projects depending on this one. You can use it if you want, but be aware that the API,
library structure, and even behaviour can change in the future without deprecation notice.

In the future, project will use [Semantic Versioning](https://semver.org/), and will track backward compatibility
changes properly, but for now even a `fix` release can provide breaking changes. Bug fixes will be associated with
a `patch` release, like `0.0.1.1` to avoid confusion.

After I feel project is ready for beta release, it will get a public 0.1.0 release and will follow semver rules after
that.

## Requirements:

* Python 3.13 or higher. Support for lower versions will be added in the future releases.


### Development requirements:

* Rye is used as a project dependency and package managing tool. See official
  [installation guide](https://rye.astral.sh/guide/installation/) for more details for your system.


## Contributing

Project is an Open Source under BSD-3-Clause license. You can contribute to the project by creating issues,
pull requests, or by any other way you find useful.

Project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit
messages. Please follow it when contributing to the project.