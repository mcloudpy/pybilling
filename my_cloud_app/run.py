# -*- coding: utf8 -*-

from flask import Flask, render_template, flash, redirect, url_for

from billing import billing_3scale

app = Flask(__name__)
app.config["SECRET_KEY"] = "DevelopmentKey"
app.config.from_pyfile("../config.py")


# Inicializar la función de billing (facturación).
facturacion = billing_3scale.ThreescaleBilling(app.config["THREESCALE_PROVIDER_KEY"], app.config["THREESCALE_USER_KEY"])


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/use", methods=["GET", "POST"])
def use():

    # Reportar un solo uso de la aplicación
    facturacion.report_hits(1)

    # Reportar también un tiempo de utilización. No es necesario reportar hits y tiempo, pueden reportarse
    # indistintamente.
    facturacion.report_time(20)


    flash(u"Uso realizado! Ha sido reportado con éxito al sistema de facturación.")

    return redirect(url_for("index"))


app.run(debug=True, port=9999)
