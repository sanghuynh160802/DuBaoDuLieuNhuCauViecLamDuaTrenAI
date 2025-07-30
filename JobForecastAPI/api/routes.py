# api/routes.py
from flask import jsonify, request, Response, stream_with_context
from db_handler import fetch_all_job_urls, fetch_all_jobs
import subprocess
import os
from threading import Lock

def init_routes(app, model_handler, job_counts, unique_cities):
    @app.route('/api/top-jobs', methods=['GET'])
    def get_top_jobs():
        top_jobs_data = job_counts.reset_index().to_dict(orient='records')
        return jsonify(top_jobs_data)

    @app.route('/api/cities', methods=['GET'])
    def get_cities():
        return jsonify(unique_cities)

    @app.route('/api/predict', methods=['POST'])
    def handle_predict():
        # Get the data from the request
        data = request.get_json()
        print("\n🔹 Received prediction request data:")
        print(data)  # Debug: Print the incoming JSON payload

        # Extract inputs from the request
        city_name = data.get('city')
        job_name = data.get('job')
        start_date = data.get('time')
        steps = data.get('step', 12)  # Default to 12 steps if not provided

        # Debug: Print extracted inputs
        print("\n🔹 Extracted inputs:")
        print(f"City: {city_name}")
        print(f"Job: {job_name}")
        print(f"Start Date: {start_date}")
        print(f"Steps: {steps}")

        # Call the prediction function
        predictions = model_handler.predict_future(city_name, job_name, start_date, steps=steps)

        # Debug: Print predictions
        print("\n🔹 Predictions:")
        print(predictions)

        # Convert and round predictions to integers
        predictions = [int(round(float(p))) for p in predictions]

        # Prepare the response data
        response_data = {"message": "Prediction successful", "predictions": predictions}

        # Debug: Print the response JSON
        print("\n🔹 Response JSON:")
        print(response_data)

        # Return the predictions
        return jsonify(response_data)
    
    @app.route("/api/job-urls", methods=["GET"])  # ✅ Correct
    def get_job_urls():
        job_urls = fetch_all_job_urls()
        return jsonify([url for (url,) in job_urls])
    
    @app.route("/api/all-jobs", methods=["GET"])
    def get_all_jobs():
        df = fetch_all_jobs()
        jobs_list = df.to_dict(orient="records")
        return jsonify(jobs_list)

    @app.route('/api/run-script/crawl-job-urls-vieclam24h', methods=['POST'])
    def crawl_job_urls_script_vieclam24h():
        script_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\crawler\vieclam24h\adding_jobUrls_vieclam24h.py"
        venv_python = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\venv\Scripts\python.exe"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        def generate():
            try:
                process = subprocess.Popen(
                    [venv_python, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env
                )
                running_processes['crawl_job_urls_script_vieclam24h'] = process

                for line in process.stdout:
                    print(line, end='')  # Print to server console
                    yield line  # Stream back to client

                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    yield f"\n❌ Script exited with return code {return_code}\n"

            except Exception as e:
                yield f"\n❌ Error running script: {str(e)}\n"

        return Response(stream_with_context(generate()), mimetype='text/plain')


    @app.route('/api/run-script/crawl-job-info-vieclam24h', methods=['POST'])
    def crawl_job_info_script_vieclam24h():
        script_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\crawler\vieclam24h\collect_job_info_vieclam24h.py"
        venv_python = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\venv\Scripts\python.exe"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        def generate():
            try:
                process = subprocess.Popen(
                    [venv_python, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env
                )
                running_processes['crawl-job-info-vieclam24h'] = process

                for line in process.stdout:
                    print(line, end='')  # Server-side logging
                    cleaned_line = line.encode("ascii", "ignore").decode("utf-8")
                    yield cleaned_line  # API response stream

                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    yield f"\n❌ Script exited with return code {return_code}\n"
            except Exception as e:
                yield f"\n❌ Error running script: {str(e)}\n"

        return Response(stream_with_context(generate()), mimetype='text/plain')
    
    @app.route('/api/run-script/crawl-job-urls-itviec', methods=['POST'])
    def crawl_job_urls_script_itviec():
        script_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\crawler\itviec\adding_joblinks_itviec.py"
        venv_python = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\venv\Scripts\python.exe"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        def generate():
            try:
                process = subprocess.Popen(
                    [venv_python, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    bufsize=1,
                    env=env
                )
                running_processes['crawl-job-urls-itviec'] = process

                for line in process.stdout:
                    print(line, end='')  # Print to server console
                    yield line  # Stream back to client

                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    yield f"\n❌ Script exited with return code {return_code}\n"

            except Exception as e:
                yield f"\n❌ Error running script: {str(e)}\n"

        return Response(stream_with_context(generate()), mimetype='text/plain')


    @app.route('/api/run-script/crawl-job-info-itviec', methods=['POST'])
    def crawl_job_info_script_itviec():
        script_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\crawler\itviec\extract_itviec_jobs_for_testing.py"
        venv_python = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\venv\Scripts\python.exe"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        def generate():
            try:
                process = subprocess.Popen(
                    [venv_python, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    env=env
                )
                running_processes['crawl-job-info-itviec'] = process

                for line in process.stdout:
                    print(line, end='')  # Server-side logging
                    cleaned_line = line.encode("ascii", "ignore").decode("utf-8")
                    yield cleaned_line  # API response stream

                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    yield f"\n❌ Script exited with return code {return_code}\n"
            except Exception as e:
                yield f"\n❌ Error running script: {str(e)}\n"

        return Response(stream_with_context(generate()), mimetype='text/plain')

    @app.route('/api/run-script/crawl-job-urls-topdev', methods=['POST'])
    def crawl_job_urls_script_topdev():
        script_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\crawler\topdev\adding_new_topdev_joblinks.py"
        venv_python = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\venv\Scripts\python.exe"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        def generate():
            try:
                process = subprocess.Popen(
                    [venv_python, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    bufsize=1,
                    env=env
                )
                running_processes['crawl-job-urls-topdev'] = process

                for line in process.stdout:
                    print(line, end='')  # Print to server console
                    yield line  # Stream back to client

                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    yield f"\n❌ Script exited with return code {return_code}\n"

            except Exception as e:
                yield f"\n❌ Error running script: {str(e)}\n"

        return Response(stream_with_context(generate()), mimetype='text/plain')


    @app.route('/api/run-script/crawl-job-info-topdev', methods=['POST'])
    def crawl_job_info_script_topdev():
        script_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\crawler\topdev\get_topdev.py"
        venv_python = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\venv\Scripts\python.exe"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        def generate():
            try:
                process = subprocess.Popen(
                    [venv_python, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env,
                    encoding='utf-8',  # Ensures proper decoding
                    errors='replace'   # Replace malformed characters
                )
                running_processes['crawl-job-info-topdev'] = process

                for line in process.stdout:
                    print(line, end='')  # Server-side logging
                    yield line  # Just stream it directly

                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    yield f"\n❌ Script exited with return code {return_code}\n"
            except Exception as e:
                yield f"\n❌ Error running script: {str(e)}\n"

        return Response(stream_with_context(generate()), mimetype='text/plain')
    
    # Dictionary to store running processes and a lock for thread safety
    running_processes = {}
    process_lock = Lock()

    @app.route('/api/stop-script/<script_key>', methods=['POST'])
    def stop_script(script_key):
        with process_lock:
            process = running_processes.get(script_key)
            if process is None:
                return jsonify({"error": "No running process found for this script"}), 404

            if process.poll() is not None:
                # Process has already finished
                running_processes.pop(script_key, None)
                return jsonify({"message": "Process already finished"}), 200

            # Stop the process
            process.terminate()  # Graceful termination first

            try:
                process.wait(timeout=5)  # Wait for process to terminate
            except subprocess.TimeoutExpired:
                process.kill()  # Force kill if not terminating

            running_processes.pop(script_key, None)
            return jsonify({"message": f"Process {script_key} stopped successfully"}), 200