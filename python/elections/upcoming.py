"""
Main module for the Upcoming Elections exercise.
"""

import functools, requests, datetime

from elections import utils # For OCD-ID generation, etc.
from elections.us_states import postal_abbreviations

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('address_form', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def search():
    """
    Take in an address and render the search result.

    The main feature of the exercise is to process a user's query and
    return a relevant list of upcoming elections based on their input.
    This method does exactly that, but not much more. :)
    """

    if request.method == 'POST':
        # Prepare the API call.
        api_url = 'https://api.turbovote.org/elections/upcoming'
        headers = {'Accept': 'application/json'}
        params  = {
            'district-divisions': utils.get_ocd_division_id(
                streetAddress=request.form['streetAddress'],
                extendedStreetAddress=request.form['extendedStreetAddress'],
                addressLocality=request.form['addressLocality'],
                addressRegion=request.form['addressRegion'],
                postalCode=request.form['postalCode'],
                addressCountry=request.form['addressCountry']
            )
        }

        # Perform the API call.
        response = requests.get(api_url, params=params, headers=headers)
        results  = response.json()
        flash('Upcoming elections: {0:d}'.format(len(results)))

        # Render the results.
        return render_template('election_results.html',
            states=postal_abbreviations,

            # Echo the user's input back into the search form fields.
            # TODO: Use Flask-WTF for form handling in the future?
            streetAddress=request.form['streetAddress'],
            extendedStreetAddress=request.form['extendedStreetAddress'],
            addressLocality=request.form['addressLocality'],
            addressRegion=request.form['addressRegion'],
            postalCode=request.form['postalCode'],

            # Also provide the results from the API query to render.
            results=results
        )

    # This was a GET request, so render the search template instead.
    return render_template('search.html', states=postal_abbreviations)
