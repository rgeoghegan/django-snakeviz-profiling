# Django Snakeviz Profiling

[![PyPI - Version](https://img.shields.io/pypi/v/django-snakeviz-profiling.svg)](https://pypi.org/project/django-snakeviz-profiling)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-snakeviz-profiling.svg)](https://pypi.org/project/django-snakeviz-profiling)

-----

Django Snakeviz Profiling integrates [snakeviz](https://pypi.org/project/snakeviz/)
along with a db query display into a django middleware that can show results inline in your application.

No migrations are required nor do any extra url routes need to be added to your application,
only requiring to install one piece of middleware.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
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

Add `django_snakeviz_profiling` to your installed apps:

    INSTALLED_APPS = [
        ...
        "django_snakeviz_profiling",
    ]

Finally, add the following config setting:

    SNAKEVIZ_PROFILING = "PLEASE_PROFILE_REQUESTS"

## Usage

On any request, add the following GET parameter to your url:

    SNAKEVIZ_PROFILING=PLEASE_PROFILE_REQUESTS

, and instead of the regular page, you will be presented with a profile output from the request.

Note that if `django_snakeviz_profiling` is used, individual requests will be dramatically slower,
so be careful using this in prod!

## License

`django-snakeviz-profiling` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
Parts of the code comes from the [Snakeviz Project](https://github.com/jiffyclub/snakeviz/) under
the BSD 3-Clause license, and is specifically identified as such.
