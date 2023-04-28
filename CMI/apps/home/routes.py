# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# GENERAL IMPORTS
from apps.home import blueprint
from flask import Flask, render_template, request, send_file
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
from apps.config import API_GENERATOR
from tratamiento.src.Graficos.top_ips import get_top_ips
from tratamiento.src.Graficos.peligroso import get_most_vulned
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
@login_required
def index():

    number_ips_default = 10
    code_device_default = 0

    if request.method == 'POST':
        number = request.form.get('ip-count', type = int)
        code_device = request.form.get('device-type', type = int) 
        chart_data_ips = get_top_ips(number)
        chart_data_dispo = get_most_vulned(code_device)
    else:
        chart_data_ips = get_top_ips(number_ips_default)
        chart_data_dispo = get_most_vulned(code_device_default)
    
    index = render_template('home/index.html', segment='index', API_GENERATOR=len(API_GENERATOR), chart_data=chart_data_ips, most_vulned=chart_data_dispo)


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
        # Analizar la respuesta JSON de la API para obtener la información de las vulnerabilidades
        vulnerabilities = response.json()[:10]  # Obtener las primeras 10 vulnerabilidades
        # Note: here we access the entire list returned by the API, hence there is no key specified

        # Do something with the vulnerabilities list here
        print(vulnerabilities)
    else:
        # Si hay un error al hacer la solicitud, muestra un mensaje de error
        vulnerabilities = [{'error': 'Error al obtener las vulnerabilidades'}]
        print(vulnerabilities)
    
    data = json.dumps(vulnerabilities)

    # Render the template with the JSON data
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
    if grafico == "alerts_type":
        pdf_buffer = tipo_alerta()
    if grafico == "most_vulned":
        pdf_buffer = most_vulned()
    if grafico == "puertos_vulns":
        pdf_buffer = puertos_vulns()
    if grafico == "top":
        pdf_buffer = top_ips()
    
    return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, attachment_filename='alerts_per_day.pdf')





