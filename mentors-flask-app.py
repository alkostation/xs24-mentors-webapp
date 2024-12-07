import os
from os.path import join

from flask import Flask, send_from_directory
from markupsafe import escape
from pymisp import PyMISP, MISPUser, MISPOrganisation, MISPSharingGroup
from dotenv import load_dotenv
import jinja2

global_context = {
    "app_title": "MISP mentor's events page",
    "org_professional_yt": "Professional YT",
    "org_mentor": "Default",
}

app = Flask(__name__)

file_loader = jinja2.FileSystemLoader(join(app.root_path, "templates"))
jinja_env = jinja2.Environment(loader=file_loader)


def render_template(template, context):
    return jinja_env.get_template(template).render(**context)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def hello_world():
    # Get all the events from the Default org
    events = misp.search()

    # professional yt org "Default"
    professional_yt_events = [
        event for event in events
        if event['Event']['Org']['name'] == global_context["org_professional_yt"] or
           event['Event']['Orgc']['name'] == global_context["org_professional_yt"]
    ]

    mentor_team_events = [
        event for event in events
        if event['Event']['Org']['name'] == "Default" or
           event['Event']['Orgc']['name'] == "Default"
    ]

    # events_page = '<h1>Events</h1>'
    #
    # events_page += '<li>'
    #
    # # Iterate through the events
    # for event in events:
    #     events_page += f'<p>' \
    #                    f'<a href="{escape(global_context["misp_url"])}events/view/{escape(event["Event"]["id"])}" target="_blank">' \
    #                    f'{escape(event["Event"]["info"])}' \
    #                    f'</a>' \
    #                    f'</p>'
    #
    # events_page += '</li>'

    professional_team_events_html = render_template("misp_events.html.jinja2", {**global_context, "events": professional_yt_events})
    mentor_team_events_html = render_template("misp_events.html.jinja2", {**global_context, "events": mentor_team_events})

    return render_template("page.html.jinja2",
                           {**global_context,
                            "events_html": professional_team_events_html,
                            "mentor_team_events_html": mentor_team_events_html})


if __name__ == '__main__':
    load_dotenv()
    global_context["misp_url"] = os.getenv("MISP_URL")
    global_context["misp_key"] = os.getenv("MISP_KEY")
    global_context["misp_verifycert"] = os.getenv("MISP_VERIFYCERT")

    # Initialize the MISP object
    misp = PyMISP(global_context["misp_url"],
                  global_context["misp_key"],
                  ssl=global_context['misp_verifycert'],
                  debug=True)

    app.run(debug=True, use_debugger=False, use_reloader=False)
