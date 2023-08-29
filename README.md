# Django Snakeviz Profiling

[![PyPI - Version](https://img.shields.io/pypi/v/django-snakeviz-profiling.svg)](https://pypi.org/project/django-snakeviz-profiling)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-snakeviz-profiling.svg)](https://pypi.org/project/django-snakeviz-profiling)

-----

Django Snakeviz Profiling integrates [snakeviz](https://pypi.org/project/snakeviz/)
into a django middleware that can show results inline in your application.

No migrations are required nor do any extra url routes need to be added to your application,
only requiring to install one piece of middleware.

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install django-snakeviz-profiling
```

In your settings file, add the following middleware as close to the top as
possible to cover as much code as possible:

    MIDDLEWARE = [
        "django_snakeviz_profiling.SnakevizProfilingMiddleware",
        ...
    ]

And also add the following config setting:

    SNAKEVIZ_PROFILING = "PLEASE_PROFILE_REQUESTS"

## Usage

On any request, add the following GET parameter to your url:

    SNAKEVIZ_PROFILING=PLEASE_PROFILE_REQUESTS

, and instead of the regular page, you will be presented with a profile output from the request.

## License

`django-snakeviz-profiling` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
Parts of the code comes from the [Snakeviz Project](https://github.com/jiffyclub/snakeviz/) under
the BSD 3-Clause license, and is specifically identified as such.
