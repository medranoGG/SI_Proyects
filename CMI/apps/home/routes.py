# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# GENERAL IMPORTS
import datetime
from apps.home import blueprint
from flask import Flask, render_template, request, send_file
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
from apps.config import API_GENERATOR
from tratamiento.src.Graficos.get_top_ips import get_top_ips
from tratamiento.src.Graficos.get_most_dangerous import get_most_dangerous
from tratamiento.src.Graficos.get_most_vulned import get_most_vulned
from tratamiento.src.Graficos.get_alertas_temporal import get_alertas_temporal
from tratamiento.src.Graficos.get_alertas_temporal_prev import get_alertas_temporal_prev
from tratamiento.src.Graficos.get_alertas_temporal_next import get_alertas_temporal_next

import json

# PDF IMPORTS
from io import BytesIO
from tratamiento.src.Graficos.alertas_temporal import alertas_temporal
from tratamiento.src.Graficos.alerts_type import tipo_alerta
from tratamiento.src.Graficos.most_vulned import most_vulned
from tratamiento.src.Graficos.puertos_vulns import puertos_vulns
from tratamiento.src.Graficos.top import top_ips

pdf_file = None

@blueprint.route('/index', methods=['GET', 'POST'])
#@login_required
def index():

    number_ips_default = 10
    code_device_default = 0
    default_vulned = 10
    default_date_prev = "2022-07-03"
    default_date = "2022-07-04"
    default_date_next = "2022-07-05"

    if request.method == 'POST':
        number = request.form.get('ip-count', type = int)
        code_device = request.form.get('device-type', type = int) 
        vulned_num = request.form.get('vuln-number', type = int)
        date_vuln = request.form.get('date-d', type = str)
        chart_data_ips = get_top_ips(number)
        chart_data_dispo = get_most_dangerous(code_device)
        chart_data_vulned = get_most_vulned(vulned_num)
        chart_alerts_date = get_alertas_temporal(date_vuln)

    
        date_prev = "2022-07-03"
        date_next = "2022-07-05"
        """
        date_obj = datetime.strptime(date_vuln, "%Y-%m-%d")

        prev_day_obj = date_obj - datetime.timedelta(days=1)
        date_prev = prev_day_obj.strftime("%Y-%m-%d")

        next_day_obj = date_obj + datetime.timedelta(days=1)
        date_next = next_day_obj.strftime("%Y-%m-%d")
        """

        chart_alerts_date_prev = get_alertas_temporal_prev(date_prev)
        chart_alerts_date_next = get_alertas_temporal_next(date_next)
    else:
        chart_data_ips = get_top_ips(number_ips_default)
        chart_data_dispo = get_most_dangerous(code_device_default)
        chart_data_vulned = get_most_vulned(default_vulned)
        chart_alerts_date = get_alertas_temporal(default_date)
        chart_alerts_date_prev = get_alertas_temporal_prev(default_date_prev)
        chart_alerts_date_next = get_alertas_temporal_next(default_date_next)
        
    
    index = render_template('home/index.html', segment='index', API_GENERATOR=len(API_GENERATOR), 
                            chart_data=chart_data_ips, most_dangerous=chart_data_dispo, most_vulned = chart_data_vulned,
                            chart_alerts_previous = chart_alerts_date_prev,chart_alerts = chart_alerts_date,chart_alerts_next=chart_alerts_date_next)


    return index

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, API_GENERATOR=len(API_GENERATOR))

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

@blueprint.route('/cve')
@login_required
def CVE():
    
    
    response = requests.get('https://cve.circl.lu/api/last')

    if response.status_code == 200:
        vulnerabilities = response.json()[:10]  
      
        print(vulnerabilities)
    else:
        vulnerabilities = [{'error': 'Error al obtener las vulnerabilidades'}]
        print(vulnerabilities)
    
    data = json.dumps(vulnerabilities)

    return render_template('home/cve.html', data=data)


@blueprint.route('/download')
@login_required
def PDF_route():

    # Render the template with the JSON data
    return render_template('home/pdf.html')


@blueprint.route('/download/pdf', methods=['POST'])
@login_required
def PDF():

    grafico = request.form['grafico']

    if grafico == "alertas_temporal":
        pdf_buffer = alertas_temporal()
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, attachment_filename='temporary_alerts.pdf')
    if grafico == "alerts_type":
        pdf_buffer = tipo_alerta()
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, attachment_filename='type_alerts.pdf')
    if grafico == "most_vulned":
        pdf_buffer = most_vulned()
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, attachment_filename='vulnerable_devices.pdf')
    if grafico == "puertos_vulns":
        pdf_buffer = puertos_vulns()
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, attachment_filename='vulnerable_ports.pdf')
    if grafico == "top":
        pdf_buffer = top_ips()
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, attachment_filename='vulnerable_ips.pdf')
    
    




