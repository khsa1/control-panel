import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests
    import json
    return json, mo, requests


@app.cell
def _(mo):
    mo.md(r"""# CTController Control Panel""")
    return


@app.cell
def _(mo):
    user_controller_ip = mo.ui.text(value=f'http://127.0.0.1:8080', label='CTController IP: ', full_width=True)
    user_controller_ip
    return (user_controller_ip,)


@app.cell
def _(user_controller_ip):
    #controller_ip = 'http://129.114.108.234:8080'
    controller_ip = user_controller_ip.value
    return (controller_ip,)


@app.cell
def _(controller_ip, requests):
    def get_request(endpoint):
        try:
            response = requests.get(f"{controller_ip}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return(f"Error fetching data from {endpoint}: {e}")
    return (get_request,)


@app.cell
def _(controller_ip, requests):
    def post_request(endpoint, payload={}):
        try:
            response = requests.post(f"{controller_ip}/{endpoint}", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return(f"Error posting data to {endpoint}: {e}")
    return (post_request,)


@app.cell
def _(controller_ip, requests):
    def file_get_request(endpoint):
        try:
            response = requests.get(f"{controller_ip}/{endpoint}")
            response.raise_for_status()
            return response.content.decode('utf-8')
        except requests.RequestException as e:
            return(f"Error fetching file from {endpoint}: {e}")
    return (file_get_request,)


@app.cell
def _(get_request):
    def check_health():
        return get_request('health')
    return


@app.cell
def _():
    default_config_payload = {
        "gpu": "false",
        "ckn_mqtt_broker": "10.169.143.160",
        "ct_version": "test",
        "mode": "demo",
        "model": "yolov5nu_ep120_bs32_lr0.001_0cfb1c03.pt",
        "inference_server": "false",
        "detection_thresholds": "{\"animal\": \"0.7\", \"image_store_save_threshold\": \"0\", \"image_store_reduce_save_threshold\": \"0\"}"
    }
    return (default_config_payload,)


@app.cell
def _(config_payload_box, json):
    config_payload = json.loads(config_payload_box.value)
    return (config_payload,)


@app.cell
def _(mo):
    startup_button = mo.ui.run_button(label='Startup')
    configure_button = mo.ui.run_button(label='Configure')
    run_button = mo.ui.run_button(label='Run')
    stop_button = mo.ui.run_button(label='Stop')
    shutdown_button = mo.ui.run_button(label='Shutdown')
    health_button = mo.ui.run_button(label='Check Health')
    dl_logs_button = mo.ui.run_button(label='Download Logs')
    dl_config_button = mo.ui.run_button(label='Download Config')
    return (
        configure_button,
        dl_config_button,
        dl_logs_button,
        health_button,
        run_button,
        shutdown_button,
        startup_button,
        stop_button,
    )


@app.cell
def _(
    configure_button,
    dl_config_button,
    dl_logs_button,
    health_button,
    mo,
    run_button,
    shutdown_button,
    startup_button,
    stop_button,
):
    mo.vstack([
    mo.hstack([startup_button, configure_button, run_button, stop_button, shutdown_button], justify='center', gap=1.5),
    mo.hstack([health_button, dl_logs_button, dl_config_button], justify='center', gap=1.5)
    ]
    )
    return


@app.cell
def _(default_config_payload, json, mo):
    config_payload_box = mo.ui.text_area(value=json.dumps(default_config_payload, indent=2), label='Configuration: ', full_width=True, rows=10)
    config_payload_box
    return (config_payload_box,)


@app.cell
def _(
    config_payload,
    configure_button,
    dl_config_button,
    dl_logs_button,
    file_get_request,
    get_request,
    health_button,
    post_request,
    run_button,
    shutdown_button,
    startup_button,
    stop_button,
):
    mapping = [
        (startup_button, lambda: post_request('startup')),
        (configure_button, lambda: post_request('configure', config_payload)),
        (run_button, lambda: post_request('run')),
        (stop_button, lambda: post_request('stop')),
        (shutdown_button, lambda: post_request('shutdown')),
        (dl_logs_button, lambda: file_get_request('dl_controller_logs')),
        (dl_config_button, lambda: file_get_request('dl_config')),
        (health_button, lambda: get_request('health'))
    ]
    return (mapping,)


@app.cell
def _(json, mapping):
    response_output = ''
    for button, fhandle in mapping:
        if button.value:
            result = fhandle()
            if isinstance(result, dict):
                response_output = json.dumps(result, indent=2)
            else:
                response_output = str(result)
    return (response_output,)


@app.cell
def _(mo, response_output):
    mo.ui.text_area(
            value=response_output,
            label="API Response",
            full_width=True,
            disabled=True,
            rows=10
        )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
