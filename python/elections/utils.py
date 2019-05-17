"""
Common utility functions, filters, etcetera.

This module stores shared routines that are generic to the project.

Its documentation loosely conforms to the Google Python style guide:

    https://google.github.io/styleguide/pyguide.html#381-docstrings

Utility methods contain Python doctest tests. Run the tests for this
module as follows:

    python3 -m doctest /path/to/elections/utils.py

No output is good. :)
"""
import jinja2, flask, datetime

bp = flask.Blueprint('filters', __name__)

def get_ocd_division_id(**kwargs: str) -> str:
    """
    Constructs a OCD-conformant Division ID from address input.

    The input needs to be valid for OCD, i.e., ISO-3166 alpha-2 country codes.

    For more information about OCD-IDs, see the
    `Open Civic Data data types documentation https://opencivicdata.readthedocs.io/en/latest/data/datatypes.html`_.

    Args:
        **kwargs: Keyword arguments for an address. Use Schema.org's
            ``PostalAddress`` property names to denote values, e.g.,
            ``streetAddress`` or ``addressLocality``.

    Returns:
        A string of one or more OCD Division IDs, separated by commas.

    >>> get_ocd_division_id(addressLocality="Provincetown", addressRegion="MA", addressCountry="US")
    'ocd-division/country:us/state:ma,ocd-division/country:us/state:ma/place:provincetown'
    """

    ocd_id  = 'ocd-division' # All of these IDs will be Divisions.
    ocd_ids = []             # We may end up with multiple OCD-IDs!

    # Check keywords in this specific order.
    # TODO: Check other address properties like county, etc?
    if 'addressCountry' in kwargs:
        ocd_id = ocd_id + '/country:' + kwargs['addressCountry'].lower()

    if 'addressRegion' in kwargs:
        ocd_id = ocd_id + '/state:' + kwargs['addressRegion'].lower()
        ocd_ids.append(ocd_id) # Save a copy of the State OCD-ID.

    if 'addressLocality' in kwargs:
        ocd_id = ocd_id + '/place:' + kwargs['addressLocality'].lower().replace(' ', '_')
        ocd_ids.append(ocd_id) # Save the city OCD-ID as well.

    # Return a string of the OCD-IDs we ended up with.
    return ','.join(ocd_ids)

@jinja2.contextfilter
@bp.app_template_filter('iso8601_to_datetime')
def ISO8601toDateTime(context, dt_string: str) -> datetime:
    """
    Converts an ISO-8601 formatted string into a Python datetime object.

    Args:
        context: The Jinja template context.
        dt_string: The ISO-8601 formatted datetime string.

    >>> ISO8601toDateTime(None, '2019-05-10T03:12:45Z') 
    datetime.datetime(2019, 5, 10, 3, 12, 45)
    """

    return datetime.datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%SZ')
