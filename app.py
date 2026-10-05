from flask import Flask, request, send_file
import subprocess, tempfile, os

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile():
    code = request.json.get('code')
    if not code:
        return {'error': 'Nenhum código enviado'}, 400

    with tempfile.TemporaryDirectory() as tmpdir:
        script = os.path.join(tmpdir, 'script.py')
        with open(script, 'w') as f:
            f.write(code)

        result = subprocess.run(
            ['pyinstaller', '--onefile',
             '--distpath', tmpdir,
             '--workpath', os.path.join(tmpdir, 'build'),
             '--specpath', tmpdir,
             script],
            cwd=tmpdir,
            capture_output=True, text=True
        )

        exe = os.path.join(tmpdir, 'script')
        if not os.path.exists(exe):
            return {'error': result.stderr}, 500

        return send_file(exe, as_attachment=True,
                         download_name='output.exe')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
